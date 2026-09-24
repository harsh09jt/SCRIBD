"""
Upload Service.
Validates an uploaded file, converts it to a normalised markdown document, stores it under
data/uploads/<category>/, records it in the database and re-indexes the knowledge base so the
agents can answer questions from it immediately.
"""

import os
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from backend.database.repositories import UploadedDocumentRepository
from backend.rag.document_loader import extract_text, split_title_and_body, get_extension, UnsupportedFileError
from backend.rag.ingestion import get_ingestion_pipeline, UPLOADS_DIR

ALL_ROLES = ["employee", "manager", "hr", "legal", "admin"]
VALID_CATEGORIES = ("policy", "product", "contract")
CATEGORY_LABELS = {"policy": "Policy", "product": "Product", "contract": "Contract / SLA"}


class UploadError(ValueError):
    """A user-facing validation problem."""


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:40] or "document"


def _clean_line(text: str, max_len: int = 120) -> str:
    """Single-line, header-safe string (newlines removed so text can never forge extra metadata lines)."""
    return re.sub(r"\s+", " ", text).strip()[:max_len]


def normalise_roles(roles: Optional[List[str]]) -> List[str]:
    if not roles:
        return list(ALL_ROLES)
    cleaned = []
    for r in roles:
        r = str(r).lower().strip()
        if r in ALL_ROLES and r not in cleaned:
            cleaned.append(r)
    if not cleaned:
        raise UploadError("Choose at least one valid access role.")
    if "admin" not in cleaned:
        cleaned.append("admin")   # administrators can always read every document
    return cleaned


def save_upload(
    filename: str,
    data: bytes,
    category: str = "policy",
    title: str = "",
    department: str = "",
    access_roles: Optional[List[str]] = None,
    uploaded_by_role: str = "employee",
) -> Dict[str, Any]:
    category = (category or "policy").lower()
    if category not in VALID_CATEGORIES:
        raise UploadError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}.")
    roles = normalise_roles(access_roles)

    try:
        text = extract_text(filename, data)
    except UnsupportedFileError as exc:
        raise UploadError(str(exc))

    detected_title, body = split_title_and_body(text)
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", os.path.basename(filename or "document"))
    final_title = _clean_line(title) or _clean_line(detected_title) or _clean_line(stem.replace("_", " ").replace("-", " ").title())
    final_dept = _clean_line(department) or "Uploaded Documents"

    if not re.match(r"\s*##?\s", body):
        body = "## Document Content\n" + body

    doc_id = f"UPL-{uuid.uuid4().hex[:8].upper()}"
    today = datetime.now().strftime("%Y-%m-%d")
    document = (
        f"# {final_title}\n"
        f"Document ID: {doc_id}\n"
        f"Version: v1.0\n"
        f"Last Updated: {today}\n"
        f"Department: {final_dept}\n"
        f"Owner: Uploaded by {uploaded_by_role.upper()} via Upload Center\n"
        f"Access Roles: {', '.join(roles)}\n"
        f"Source File: {_clean_line(os.path.basename(filename or 'upload'), 80)}\n\n"
        f"{body}\n"
    )

    folder = os.path.join(UPLOADS_DIR, category)
    os.makedirs(folder, exist_ok=True)
    stored_name = f"{doc_id}_{_slugify(final_title)}.md"
    stored_path = os.path.join(folder, stored_name)
    with open(stored_path, "w", encoding="utf-8") as fh:
        fh.write(document)

    repo = UploadedDocumentRepository()
    try:
        repo.create(
            doc_id=doc_id, original_filename=os.path.basename(filename or "upload"), stored_path=stored_path,
            title=final_title, doc_type=category, department=final_dept, access_roles=roles,
            size_bytes=len(data), uploaded_by_role=uploaded_by_role,
        )
        pipeline = get_ingestion_pipeline()
        pipeline.ingest_all_sources()
    except Exception:
        # Never leave a half-registered file behind
        repo.delete(doc_id)
        if os.path.exists(stored_path):
            os.remove(stored_path)
        get_ingestion_pipeline().ingest_all_sources()
        raise

    entry = next((m for m in pipeline.ingested_manifest if m["filename"] == stored_name), None)
    chunk_count = entry["chunks_count"] if entry else 0
    repo.update_chunk_count(doc_id, chunk_count)

    return {
        "doc_id": doc_id,
        "title": final_title,
        "category": category,
        "department": final_dept,
        "access_roles": roles,
        "chunks_count": chunk_count,
        "size_bytes": len(data),
        "extension": get_extension(filename),
        "filename": stored_name,
    }


def delete_upload(doc_id: str, user_role: str) -> Dict[str, Any]:
    """Remove an uploaded document. Only admins or the role that uploaded it may delete it."""
    repo = UploadedDocumentRepository()
    record = repo.get(doc_id)
    if not record:
        raise UploadError("That uploaded document does not exist.")
    if user_role != "admin" and record["uploaded_by_role"] != user_role:
        raise PermissionError("Only an administrator or the uploader's role can delete this document.")

    if os.path.exists(record["stored_path"]):
        os.remove(record["stored_path"])
    repo.delete(doc_id)
    get_ingestion_pipeline().ingest_all_sources()
    return {"deleted": True, "doc_id": doc_id, "title": record["title"]}
