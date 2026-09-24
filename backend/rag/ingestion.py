"""
Enterprise Ingestion Pipeline.
Extracts, cleans, chunks, generates rich metadata, and indexes documents into the vector store.
Preserves access_roles, document_name, document_type, section, version, and last_updated.
"""

import hashlib
import os
import re
from typing import List, Dict, Any, Optional
from backend.rag.vectorstore import get_vector_store

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")

# Sections longer than this are split into smaller chunks so retrieval stays precise
MAX_CHUNK_CHARS = 900

FRIENDLY_NAMES = {
    "remote_work_policy.md": "Remote Work Policy",
    "health_insurance_claim_procedure.md": "Health Insurance Claim Procedure",
    "travel_and_expense_policy.md": "Travel and Expense Policy",
    "paternity_and_maternity_leave_policy.md": "Parental Leave Policy",
    "data_privacy_and_gdpr_policy.md": "Data Privacy & GDPR Policy",
    "code_of_conduct_and_ethics.md": "Code of Conduct & Ethics",
    "equipment_and_byod_policy.md": "Equipment & BYOD Policy",
    "overtime_and_oncall_policy.md": "On-Call & Incident Standby Policy",
    "whistleblower_protection_policy.md": "Whistleblower Protection Policy",
    "information_security_and_access_policy.md": "Information Security & Access Control Policy",
    "severance_and_exit_procedure.md": "Severance & Exit Procedure",
    "backup_policy.md": "Backup & Disaster Recovery Policy",
    "vendor_management_policy.md": "Vendor Management Policy",
    "employee_handbook.md": "Employee Handbook",
    "corporate_health_shield.md": "Corporate Health Shield (Product X)",
    "term_life_pro.md": "Term Life Pro (Product Z)",
    "cyber_risk_elite.md": "Cyber Risk Elite (Product Y)",
    "keyman_insurance.md": "Keyman Insurance",
    "executive_disability_income.md": "Executive Long-Term Disability Shield",
    "commercial_fleet_cover.md": "Commercial Fleet Cover",
    "group_gratuity_plan.md": "Group Gratuity Plan",
    "directors_and_officers_liability.md": "Directors & Officers Liability",
    "property_and_casualty_umbrella.md": "Property & Casualty Umbrella",
    "marine_cargo_international.md": "Global Marine Cargo",
    "vendor_abc_cloud_hosting_sla.md": "Vendor ABC Cloud Hosting Agreement",
    "global_health_tpa_msa.md": "Global Health TPA Master Services Agreement",
    "delta_logistics_fleet_sla.md": "Delta Logistics Transport SLA",
    "acme_legal_advisory_retainer.md": "Legal Advisory Retainer Agreement",
    "zenith_secops_agreement.md": "Zenith SecOps Agreement",
    "ceo_compensation_contract.md": "CEO Compensation Contract"
}


class DocumentIngestionPipeline:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.ingested_manifest: List[Dict[str, Any]] = []

    def friendly_title_for(self, filename: str, text: str) -> str:
        """Curated name if we have one, else the document's own H1 title, else a prettified filename."""
        if filename in FRIENDLY_NAMES:
            return FRIENDLY_NAMES[filename]
        h1 = self.extract_h1_title(text)
        if h1:
            return h1
        return re.sub(r"\.(md|txt)$", "", filename).replace("_", " ").title()

    def clean_text(self, text: str) -> str:
        """Clean and normalize raw text."""
        cleaned = re.sub(r'\r\n', '\n', text)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        return cleaned.strip()

    def parse_metadata_header(self, text: str) -> Dict[str, Any]:
        """
        Extract metadata from the header block (the lines right below the H1 title).
        Parsing stops at the first blank line or the first '##' section, so body text
        can never overwrite metadata such as access roles.
        """
        meta: Dict[str, Any] = {}
        for idx, line in enumerate(text.split("\n")[:20]):
            stripped = line.strip()
            if idx > 0 and (not stripped or stripped.startswith("##")):
                break
            if ":" in line and not stripped.startswith("#"):
                key, val = line.split(":", 1)
                clean_key = key.strip().lower().replace(" ", "_")
                clean_val = val.strip()
                if clean_key == "access_roles":
                    roles = [r.strip().lower() for r in clean_val.split(",") if r.strip()]
                    meta[clean_key] = roles
                else:
                    meta[clean_key] = clean_val
        return meta

    @staticmethod
    def extract_h1_title(text: str) -> Optional[str]:
        """Return the first '# Title' line of a markdown document, if any."""
        for line in text.split("\n")[:5]:
            if line.startswith("# "):
                return line[2:].strip()
        return None

    def split_long_body(self, body: str, limit: int = MAX_CHUNK_CHARS) -> List[str]:
        """Split an over-long section body into readable parts of at most ~limit characters."""
        if len(body) <= limit:
            return [body]

        pieces: List[str] = []
        for line in body.split("\n"):
            if len(line) <= limit:
                pieces.append(line)
                continue
            # A single very long line: break on sentence boundaries, then hard-cut as a last resort
            for sentence in re.split(r"(?<=[.!?])\s+", line):
                while len(sentence) > limit:
                    pieces.append(sentence[:limit])
                    sentence = sentence[limit:]
                if sentence:
                    pieces.append(sentence)

        parts: List[str] = []
        current = ""
        for piece in pieces:
            candidate = f"{current}\n{piece}" if current else piece
            if len(candidate) > limit and current:
                parts.append(current.strip())
                current = piece
            else:
                current = candidate
        if current.strip():
            parts.append(current.strip())
        return [p for p in parts if p]

    def chunk_document(
        self,
        file_path: str,
        doc_type: str,
        department: str,
        overrides: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Parse document into semantic chunks by headers and sections with rich metadata.
        `overrides` (title, department, access_roles) comes from the database for uploaded files
        and always wins over anything written inside the file itself.
        """
        overrides = overrides or {}
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        clean_content = self.clean_text(raw_text)
        filename = os.path.basename(file_path)
        header_meta = self.parse_metadata_header(clean_content)

        friendly_title = overrides.get("title") or self.friendly_title_for(filename, clean_content)
        doc_version = header_meta.get("version", "v1.0")
        last_updated = header_meta.get("last_updated", "2026-08-01")
        doc_dept = overrides.get("department") or header_meta.get("department", department)

        # Determine access_roles
        if overrides.get("access_roles"):
            access_roles = [r.lower() for r in overrides["access_roles"]]
        elif "access_roles" in header_meta and isinstance(header_meta["access_roles"], list):
            access_roles = header_meta["access_roles"]
        elif "ceo" in filename.lower():
            access_roles = ["admin", "hr"]
        elif doc_type == "contract":
            # Standard vendor contracts accessible to employee, manager, legal, admin
            access_roles = ["employee", "manager", "hr", "legal", "admin"]
        else:
            access_roles = ["employee", "manager", "hr", "legal", "admin"]

        # Split on markdown headers ##
        sections = re.split(r'\n(?=##?\s+)', clean_content)
        chunks = []

        for sec_idx, sec_text in enumerate(sections):
            lines = sec_text.strip().split("\n")
            if not lines:
                continue

            first_line = lines[0].strip()
            if first_line.startswith("#"):
                section_title = first_line.lstrip("#").strip()
                body = "\n".join(lines[1:]).strip()
            else:
                section_title = "Overview & Preamble"
                body = sec_text.strip()

            if not body:
                continue

            parts = self.split_long_body(body)
            for part_idx, part_body in enumerate(parts):
                part_title = section_title if len(parts) == 1 else f"{section_title} (part {part_idx + 1})"
                # Deterministic id: re-ingesting the same file never creates duplicate vectors
                digest = hashlib.sha1(f"{filename}|{sec_idx}|{part_idx}".encode("utf-8")).hexdigest()[:8].upper()
                chunk_id = f"CHK-{digest}"
                chunk_metadata = {
                    "document_name": friendly_title,
                    "file_name": filename,
                    "document_type": doc_type,
                    "department": doc_dept,
                    "section": part_title,
                    "source": file_path,
                    "version": doc_version,
                    "last_updated": last_updated,
                    "access_roles": access_roles
                }

                chunks.append({
                    "chunk_id": chunk_id,
                    "document_name": friendly_title,
                    "file_name": filename,
                    "document_type": doc_type,
                    "department": doc_dept,
                    "section": part_title,
                    "content": part_body,
                    "version": doc_version,
                    "last_updated": last_updated,
                    "access_roles": access_roles,
                    "metadata": chunk_metadata
                })

        return chunks

    def _uploaded_overrides(self) -> Dict[str, Dict[str, Any]]:
        """Database-controlled metadata for uploaded files, keyed by stored file name."""
        try:
            from backend.database.repositories import UploadedDocumentRepository
            rows = UploadedDocumentRepository().get_all()
        except Exception:
            return {}
        overrides: Dict[str, Dict[str, Any]] = {}
        for row in rows:
            overrides[os.path.basename(row["stored_path"])] = {
                "doc_id": row["doc_id"],
                "title": row["title"],
                "department": row["department"],
                "access_roles": [r for r in row["access_roles"].split(",") if r],
                "uploaded_by_role": row["uploaded_by_role"],
            }
        return overrides

    def ingest_all_sources(self) -> int:
        """Scan data directories (built-in library + uploads) and index policies, products and contracts."""
        self.vector_store.reset()
        self.ingested_manifest.clear()

        all_chunks = []
        uploaded_meta = self._uploaded_overrides()

        # (folder, doc_type, default department, is_uploaded)
        source_dirs = [
            (os.path.join(DATA_DIR, "policies"), "policy", "Human Resources & Governance", False),
            (os.path.join(DATA_DIR, "products"), "product", "Insurance Underwriting", False),
            (os.path.join(DATA_DIR, "contracts"), "contract", "Procurement & Legal", False),
            (os.path.join(UPLOADS_DIR, "policy"), "policy", "Uploaded Documents", True),
            (os.path.join(UPLOADS_DIR, "product"), "product", "Uploaded Documents", True),
            (os.path.join(UPLOADS_DIR, "contract"), "contract", "Uploaded Documents", True),
        ]

        for folder, doc_type, default_dept, is_uploaded in source_dirs:
            if not os.path.exists(folder):
                continue
            for fname in sorted(os.listdir(folder)):
                if not fname.endswith((".md", ".txt")):
                    continue
                fpath = os.path.join(folder, fname)
                overrides = uploaded_meta.get(fname) if is_uploaded else None
                if is_uploaded and overrides is None:
                    # Orphan file with no database record: never index files we cannot attribute
                    continue
                chunks = self.chunk_document(fpath, doc_type, default_dept, overrides)
                all_chunks.extend(chunks)
                with open(fpath, "r", encoding="utf-8") as fh:
                    header = self.parse_metadata_header(self.clean_text(fh.read()))
                self.ingested_manifest.append({
                    "filename": fname,
                    "document_id": (overrides or {}).get("doc_id") or header.get("document_id", ""),
                    "title": chunks[0]["document_name"] if chunks else self.friendly_title_for(fname, ""),
                    "type": doc_type,
                    "department": chunks[0]["department"] if chunks else default_dept,
                    "chunks_count": len(chunks),
                    "access_roles": chunks[0]["access_roles"] if chunks else ["employee", "admin"],
                    "version": chunks[0]["version"] if chunks else "v1.0",
                    "last_updated": chunks[0]["last_updated"] if chunks else "2026-08-01",
                    "origin": "uploaded" if is_uploaded else "library",
                    "uploaded_by_role": (overrides or {}).get("uploaded_by_role", ""),
                    "path": fpath
                })

        self.vector_store.add_documents(all_chunks)
        print(f"Ingestion complete: Indexed {len(all_chunks)} chunks across {len(self.ingested_manifest)} enterprise documents.")
        return len(all_chunks)


# Singleton
_pipeline = None

def get_ingestion_pipeline() -> DocumentIngestionPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = DocumentIngestionPipeline()
    return _pipeline
