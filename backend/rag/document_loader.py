"""
Document Loader.
Turns an uploaded file (txt, md, csv, json, docx, pdf) into clean text / markdown
so it can flow through the same chunking and indexing pipeline as the built-in library.

Only the Python standard library is required. PDF support uses the optional `pypdf` package.
"""

import csv
import io
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import Tuple

MAX_UPLOAD_BYTES = 5 * 1024 * 1024          # 5 MB per file
MAX_EXTRACTED_CHARS = 1_500_000             # safety cap for extracted text
MAX_CSV_ROWS = 5000

SUPPORTED_EXTENSIONS = (".md", ".txt", ".log", ".csv", ".json", ".docx", ".pdf")


class UnsupportedFileError(ValueError):
    """Raised when a file cannot be turned into text (bad type, empty, scanned PDF, ...)."""


def get_extension(filename: str) -> str:
    match = re.search(r"(\.[A-Za-z0-9]+)$", filename or "")
    return match.group(1).lower() if match else ""


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return data.decode(encoding)
        except (UnicodeDecodeError, UnicodeError):
            continue
    return data.decode("utf-8", errors="replace")


def _csv_to_text(data: bytes) -> str:
    text = _decode_text(data)
    try:
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(text), dialect)
    rows = list(reader)
    if not rows:
        return ""
    header = [h.strip() or f"Column {i + 1}" for i, h in enumerate(rows[0])]
    lines = []
    for row in rows[1:MAX_CSV_ROWS + 1]:
        pairs = [f"{header[i] if i < len(header) else f'Column {i + 1}'}: {cell.strip()}"
                 for i, cell in enumerate(row) if cell.strip()]
        if pairs:
            lines.append("- " + "; ".join(pairs))
    return "\n".join(lines) if lines else "\n".join(", ".join(r) for r in rows)


def _json_to_text(data: bytes) -> str:
    text = _decode_text(data)
    try:
        return json.dumps(json.loads(text), indent=2, ensure_ascii=False)
    except ValueError:
        return text


_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _docx_paragraph_text(p: ET.Element) -> str:
    parts = []
    for node in p.iter():
        if node.tag == f"{_W_NS}t" and node.text:
            parts.append(node.text)
        elif node.tag == f"{_W_NS}tab":
            parts.append("\t")
        elif node.tag == f"{_W_NS}br":
            parts.append("\n")
    return "".join(parts).strip()


def _docx_to_text(data: bytes) -> str:
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
        info = archive.getinfo("word/document.xml")
    except (zipfile.BadZipFile, KeyError):
        raise UnsupportedFileError("This .docx file could not be opened. Please re-save it from Word and try again.")
    if info.file_size > 40 * 1024 * 1024:
        raise UnsupportedFileError("The .docx content is too large to process safely.")

    root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(f"{_W_NS}body")
    if body is None:
        return ""

    lines = []
    for child in body:
        if child.tag == f"{_W_NS}p":
            text = _docx_paragraph_text(child)
            if not text:
                lines.append("")
                continue
            style = child.find(f"{_W_NS}pPr/{_W_NS}pStyle")
            style_val = ((style.get(f"{_W_NS}val") if style is not None else "") or "").lower()
            if style_val.startswith(("heading", "title")):
                # A leading Title / Heading 1 becomes the document title, everything else a section heading
                is_document_title = not any(l.strip() for l in lines) and style_val in ("title", "heading1")
                lines.append(f"# {text}" if is_document_title else f"\n## {text}")
            else:
                lines.append(text)
        elif child.tag == f"{_W_NS}tbl":
            for row in child.iter(f"{_W_NS}tr"):
                cells = []
                for cell in row.findall(f"{_W_NS}tc"):
                    cells.append(" ".join(_docx_paragraph_text(p) for p in cell.iter(f"{_W_NS}p")).strip())
                if any(cells):
                    lines.append("- " + " | ".join(cells))
    return "\n".join(lines)


def _pdf_to_text(data: bytes) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise UnsupportedFileError(
            "PDF support needs the optional 'pypdf' package. Run: pip install pypdf  (then restart the server), "
            "or upload the document as .docx / .txt / .md."
        )
    try:
        reader = PdfReader(io.BytesIO(data))
        if reader.is_encrypted:
            raise UnsupportedFileError("This PDF is password protected. Please upload an unlocked copy.")
        pages = []
        for idx, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(f"## Page {idx}\n{text}")
    except UnsupportedFileError:
        raise
    except Exception:
        raise UnsupportedFileError("This PDF could not be read. It may be corrupted.")
    if not pages:
        raise UnsupportedFileError(
            "No selectable text was found in this PDF (it looks like a scanned image). "
            "Please upload a text-based PDF or run OCR first."
        )
    return "\n\n".join(pages)


def extract_text(filename: str, data: bytes) -> str:
    """Extract clean text from an uploaded file. Raises UnsupportedFileError with a friendly message."""
    ext = get_extension(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileError(
            f"'{ext or 'this file type'}' is not supported. Allowed types: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    if not data:
        raise UnsupportedFileError("The file is empty.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise UnsupportedFileError(f"The file is larger than the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit.")

    if ext in (".md", ".txt", ".log"):
        text = _decode_text(data)
    elif ext == ".csv":
        text = _csv_to_text(data)
    elif ext == ".json":
        text = _json_to_text(data)
    elif ext == ".docx":
        text = _docx_to_text(data)
    else:
        text = _pdf_to_text(data)

    # Remove control characters that would confuse the text pipeline, normalise newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        raise UnsupportedFileError("No readable text was found in this file.")
    return text[:MAX_EXTRACTED_CHARS]


def split_title_and_body(text: str) -> Tuple[str, str]:
    """If the text starts with a markdown '# Title', return (title, remaining body)."""
    lines = text.split("\n")
    for idx, line in enumerate(lines[:3]):
        if line.startswith("# "):
            return line[2:].strip(), "\n".join(lines[:idx] + lines[idx + 1:]).strip()
    return "", text
