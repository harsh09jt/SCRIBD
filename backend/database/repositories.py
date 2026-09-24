"""
Data Access Layer and Repositories for Enterprise Expert Knowledge Worker.
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from backend.database.connection import get_db


def _now_precise() -> str:
    """Timestamp with microseconds so that messages in one second keep their order."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class EmployeeRepository:
    def __init__(self):
        self.db = get_db()

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query(
            "SELECT * FROM employees WHERE LOWER(name) LIKE LOWER(?) OR LOWER(name) LIKE LOWER(?) LIMIT 1",
            (f"%{name}%", f"{name}%")
        )
        return rows[0] if rows else None

    def get_by_id(self, employee_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query("SELECT * FROM employees WHERE employee_id = ? LIMIT 1", (employee_id,))
        return rows[0] if rows else None

    def search(self, term: str) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            "SELECT * FROM employees WHERE LOWER(name) LIKE ? OR LOWER(department) LIKE ? OR LOWER(role) LIKE ? LIMIT 10",
            (f"%{term.lower()}%", f"%{term.lower()}%", f"%{term.lower()}%")
        )

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM employees ORDER BY name ASC")


class ProductRepository:
    def __init__(self):
        self.db = get_db()

    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query(
            "SELECT * FROM products WHERE LOWER(product_name) LIKE LOWER(?) LIMIT 1",
            (f"%{name}%",)
        )
        return rows[0] if rows else None

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM products ORDER BY product_name ASC")


class ContractRepository:
    def __init__(self):
        self.db = get_db()

    def get_by_vendor(self, vendor: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query(
            "SELECT * FROM contracts WHERE LOWER(vendor_name) LIKE LOWER(?) LIMIT 1",
            (f"%{vendor}%",)
        )
        return rows[0] if rows else None

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM contracts ORDER BY vendor_name ASC")


class PolicyRepository:
    def __init__(self):
        self.db = get_db()

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM policies ORDER BY title ASC")

    def insert_if_missing(self, policy_id: str, title: str, department: str, version: str,
                          last_updated: str, file_path: str) -> bool:
        """Register a policy in the catalogue table without touching existing rows."""
        existing = self.db.execute_query("SELECT policy_id FROM policies WHERE policy_id = ?", (policy_id,))
        if existing:
            return False
        self.db.execute_commit(
            "INSERT INTO policies (policy_id, title, department, version, last_updated, file_path) VALUES (?, ?, ?, ?, ?, ?)",
            (policy_id, title, department, version, last_updated, file_path)
        )
        return True


class AccessRequestRepository:
    def __init__(self):
        self.db = get_db()

    def create(
        self,
        employee_id: str,
        employee_name: str,
        product_or_system: str,
        reason: str,
        risk_level: str,
        requested_operation: str,
        request_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if not request_id:
            req_id = f"REQ-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        else:
            req_id = request_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute_commit("""
            INSERT INTO access_requests 
            (request_id, employee_id, employee_name, product_or_system, reason, risk_level, status, requested_operation, approved_by, request_timestamp, approval_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING', ?, NULL, ?, NULL)
        """, (req_id, employee_id, employee_name, product_or_system, reason, risk_level, requested_operation, timestamp))
        return {
            "request_id": req_id,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "product_or_system": product_or_system,
            "reason": reason,
            "risk_level": risk_level,
            "status": "PENDING",
            "requested_operation": requested_operation,
            "request_timestamp": timestamp
        }

    def get_by_id(self, request_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query("SELECT * FROM access_requests WHERE request_id = ?", (request_id,))
        return rows[0] if rows else None

    def update_status(self, request_id: str, status: str, approved_by: str) -> bool:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_affected = self.db.execute_commit("""
            UPDATE access_requests 
            SET status = ?, approved_by = ?, approval_timestamp = ?
            WHERE request_id = ?
        """, (status, approved_by, timestamp, request_id))
        return rows_affected > 0

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM access_requests ORDER BY request_timestamp DESC")


class AuditLogRepository:
    def __init__(self):
        self.db = get_db()

    def create(
        self,
        query_id: str,
        user_id: str,
        action_type: str,
        agent_name: str,
        details: str,
        status: str = "SUCCESS",
        duration_ms: int = 0
    ) -> str:
        log_id = f"LOG-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute_commit("""
            INSERT INTO audit_logs 
            (log_id, query_id, timestamp, user_id, action_type, agent_name, details, status, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (log_id, query_id, timestamp, user_id, action_type, agent_name, details, status, duration_ms))
        return log_id

    def get_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            "SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
        )


class ChatRepository:
    """Persists every chat session and message so conversations survive restarts."""

    def __init__(self):
        self.db = get_db()

    # --- sessions ---
    def create_session(self, user_id: str, user_role: str, title: str = "New chat") -> Dict[str, Any]:
        session_id = f"CHT-{uuid.uuid4().hex[:12].upper()}"
        now = _now_precise()
        self.db.execute_commit(
            "INSERT INTO chat_sessions (session_id, user_id, user_role, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (session_id, user_id, user_role, title[:120], now, now)
        )
        return {"session_id": session_id, "user_id": user_id, "user_role": user_role,
                "title": title[:120], "created_at": now, "updated_at": now}

    def get_session(self, session_id: str, user_role: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Fetch a session. When user_role is given the session must belong to that role."""
        rows = self.db.execute_query("SELECT * FROM chat_sessions WHERE session_id = ?", (session_id,))
        if not rows:
            return None
        if user_role is not None and rows[0]["user_role"] != user_role:
            return None
        return rows[0]

    def list_sessions(self, user_role: str, limit: int = 50) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            """
            SELECT s.session_id, s.title, s.user_role, s.created_at, s.updated_at,
                   (SELECT COUNT(*) FROM chat_messages m WHERE m.session_id = s.session_id) AS message_count
            FROM chat_sessions s
            WHERE s.user_role = ?
            ORDER BY s.updated_at DESC
            LIMIT ?
            """,
            (user_role, limit)
        )

    def rename_session(self, session_id: str, title: str) -> bool:
        return self.db.execute_commit(
            "UPDATE chat_sessions SET title = ? WHERE session_id = ?", (title[:120], session_id)
        ) > 0

    def delete_session(self, session_id: str) -> bool:
        self.db.execute_commit("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        return self.db.execute_commit("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,)) > 0

    def count_sessions(self) -> int:
        return self.db.execute_query("SELECT COUNT(*) AS n FROM chat_sessions")[0]["n"]

    def count_messages(self) -> int:
        return self.db.execute_query("SELECT COUNT(*) AS n FROM chat_messages")[0]["n"]

    # --- messages ---
    def add_message(self, session_id: str, sender: str, content: str,
                    metadata: Optional[Dict[str, Any]] = None) -> str:
        message_id = f"MSG-{uuid.uuid4().hex[:12].upper()}"
        now = _now_precise()
        self.db.execute_commit(
            "INSERT INTO chat_messages (message_id, session_id, sender, content, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (message_id, session_id, sender, content, json.dumps(metadata) if metadata else None, now)
        )
        self.db.execute_commit("UPDATE chat_sessions SET updated_at = ? WHERE session_id = ?", (now, session_id))
        return message_id

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        rows = self.db.execute_query(
            "SELECT * FROM chat_messages WHERE session_id = ? ORDER BY created_at ASC, rowid ASC", (session_id,)
        )
        for r in rows:
            try:
                r["metadata"] = json.loads(r["metadata"]) if r.get("metadata") else {}
            except ValueError:
                r["metadata"] = {}
        return rows

    def get_history_for_memory(self, session_id: str, limit: int = 8) -> List[Dict[str, str]]:
        """Return the last N user/assistant turns in the shape the Supervisor expects."""
        rows = self.db.execute_query(
            """
            SELECT sender, content FROM chat_messages
            WHERE session_id = ? AND sender IN ('user', 'assistant')
            ORDER BY created_at DESC, rowid DESC LIMIT ?
            """,
            (session_id, limit)
        )
        return [{"role": r["sender"], "content": r["content"]} for r in reversed(rows)]


class UploadedDocumentRepository:
    """Catalogue of files uploaded through the UI."""

    def __init__(self):
        self.db = get_db()

    def create(self, doc_id: str, original_filename: str, stored_path: str, title: str, doc_type: str,
               department: str, access_roles: List[str], size_bytes: int, uploaded_by_role: str,
               chunk_count: int = 0) -> Dict[str, Any]:
        uploaded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute_commit(
            """
            INSERT INTO uploaded_documents
            (doc_id, original_filename, stored_path, title, doc_type, department, access_roles,
             size_bytes, uploaded_by_role, uploaded_at, chunk_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (doc_id, original_filename, stored_path, title, doc_type, department, ",".join(access_roles),
             size_bytes, uploaded_by_role, uploaded_at, chunk_count)
        )
        return self.get(doc_id)

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        rows = self.db.execute_query("SELECT * FROM uploaded_documents WHERE doc_id = ?", (doc_id,))
        return rows[0] if rows else None

    def get_all(self) -> List[Dict[str, Any]]:
        return self.db.execute_query("SELECT * FROM uploaded_documents ORDER BY uploaded_at DESC")

    def update_chunk_count(self, doc_id: str, chunk_count: int) -> None:
        self.db.execute_commit("UPDATE uploaded_documents SET chunk_count = ? WHERE doc_id = ?", (chunk_count, doc_id))

    def delete(self, doc_id: str) -> bool:
        return self.db.execute_commit("DELETE FROM uploaded_documents WHERE doc_id = ?", (doc_id,)) > 0


class FaqRepository:
    """Counters and published entries for the self-updating FAQ."""

    def __init__(self):
        self.db = get_db()

    def increment(self, question_key: str) -> Dict[str, Any]:
        """Count one more ask of this question and return its row."""
        now = _now_precise()
        updated = self.db.execute_commit(
            "UPDATE faq_candidates SET ask_count = ask_count + 1, last_asked = ? WHERE question_key = ?",
            (now, question_key)
        )
        if not updated:
            self.db.execute_commit(
                "INSERT INTO faq_candidates (question_key, ask_count, first_asked, last_asked) VALUES (?, 1, ?, ?)",
                (question_key, now, now)
            )
        return self.db.execute_query("SELECT * FROM faq_candidates WHERE question_key = ?", (question_key,))[0]

    def mark_published(self, question_key: str, question: str, answer: str, sources: List[Dict[str, Any]],
                       source_titles: List[str], evaluated_count: int) -> None:
        self.db.execute_commit(
            """
            UPDATE faq_candidates
            SET status = 'published', skip_reason = NULL, display_question = ?, answer = ?, sources = ?,
                source_titles = ?, last_evaluated_count = ?, published_at = ?
            WHERE question_key = ?
            """,
            (question, answer, json.dumps(sources), json.dumps(source_titles), evaluated_count,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), question_key)
        )

    def mark_skipped(self, question_key: str, reason: str, evaluated_count: int) -> None:
        self.db.execute_commit(
            "UPDATE faq_candidates SET status = 'skipped', skip_reason = ?, last_evaluated_count = ? WHERE question_key = ?",
            (reason, evaluated_count, question_key)
        )

    def get_published(self) -> List[Dict[str, Any]]:
        return self.db.execute_query(
            "SELECT * FROM faq_candidates WHERE status = 'published' ORDER BY ask_count DESC, published_at DESC"
        )
