"""
Enterprise Expert Knowledge Worker REST API Handler.
Provides clean REST API endpoints for:
- POST   /api/chat                 (chat turn; every message is stored in the database)
- GET    /api/chats                (list saved chats for a role)
- GET    /api/chats/<id>           (load one saved chat)
- DELETE /api/chats/<id>           (delete a saved chat)
- POST   /api/upload               (add a document to the knowledge base)
- DELETE /api/uploads/<doc_id>     (remove an uploaded document)
- GET    /api/document             (read a document's text, permission checked)
- POST   /api/approval
- GET    /api/sources
- GET    /api/stats
- GET    /api/faq, /api/updates
- GET    /api/activity, /api/agents, /api/evaluation, /api/roles
"""

import base64
import binascii
import json
import os
from typing import Dict, Any, List, Optional

# Make sure every table exists (chat history, uploads, ...) before any repository is created
from backend.database.bootstrap import initialize as initialize_database
initialize_database()

from backend.graph.workflow import get_workflow
from backend.rag.ingestion import get_ingestion_pipeline, FRIENDLY_NAMES
from backend.rag.vectorstore import get_vector_store
from backend.rag.document_loader import MAX_UPLOAD_BYTES, SUPPORTED_EXTENSIONS
from backend.database.connection import DATA_DIR
from backend.database.repositories import AuditLogRepository, AccessRequestRepository, ChatRepository
from backend.tools.approval_tool import get_approval_tool
from backend.tools.permission_tool import get_permission_tool
from backend.evaluation.benchmark import get_evaluator
from backend.services import upload_service, faq_service

workflow = get_workflow()
pipeline = get_ingestion_pipeline()
vector_store = get_vector_store()
audit_repo = AuditLogRepository()
access_repo = AccessRequestRepository()
chat_repo = ChatRepository()
approval_tool = get_approval_tool()
permission_tool = get_permission_tool()
evaluator = get_evaluator()

SITE_CONTENT_PATH = os.path.join(DATA_DIR, "site_content.json")
VALID_ROLES = ["employee", "manager", "hr", "legal", "admin"]
ROLE_USER_IDS = {
    "employee": "EMP-001", "manager": "MGR-001", "hr": "HR-001", "legal": "LEG-001", "admin": "ADM-001"
}


class ApiError(Exception):
    """Raised by handlers to return a JSON error with a specific HTTP status."""

    def __init__(self, status: int, message: str, extra: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.extra = extra or {}


def _clean_role(role: Any) -> str:
    role = str(role or "employee").lower().strip()
    if role not in VALID_ROLES:
        raise ApiError(400, f"Unknown role '{role}'. Valid roles: {', '.join(VALID_ROLES)}")
    return role


AVAILABLE_ROLES = [
    {
        "role": "employee",
        "name": "Rahul Sharma",
        "title": "Senior Software Engineer",
        "department": "Engineering",
        "email": "rahul.sharma@acme.corp",
        "description": "Standard employee. Authorized for public policies, products, and employee self-service. Restricted from executive contracts."
    },
    {
        "role": "manager",
        "name": "Elena Rostova",
        "title": "Director of Engineering",
        "department": "Engineering & Operations",
        "email": "elena.rostova@acme.corp",
        "description": "Department manager. Authorized for policies, team profiles, and vendor service agreements."
    },
    {
        "role": "hr",
        "name": "Sarah Jenkins",
        "title": "VP of People Operations",
        "department": "Human Resources",
        "email": "sarah.jenkins@acme.corp",
        "description": "Human Resources executive. Authorized for all employee records, leave policies, and executive compensation contracts."
    },
    {
        "role": "legal",
        "name": "Neha Gupta",
        "title": "Chief Compliance Counsel",
        "department": "Legal & GRC",
        "email": "neha.gupta@acme.corp",
        "description": "Corporate counsel. Authorized for all vendor contracts, SLAs, regulatory compliance documents, and governance policies."
    },
    {
        "role": "admin",
        "name": "David Chen",
        "title": "CISO & Security Administrator",
        "department": "Cybersecurity & Infrastructure",
        "email": "david.chen@acme.corp",
        "description": "Enterprise administrator. Full unconstrained clearance across all enterprise documents, executive contracts, and audit trails."
    }
]

AGENT_METADATA = [
    {
        "name": "Supervisor Agent",
        "role": "Central Intelligent Router",
        "purpose": "Classifies incoming queries, analyzes coreferences across conversational turns, and orchestrates agent topology.",
        "tools": ["Coreference Resolver", "Intent Classifier", "Domain Dispatcher"],
        "status": "Active",
        "avg_latency": "1.2 ms"
    },
    {
        "name": "Planner Agent",
        "role": "Strategic Task Decomposer",
        "purpose": "Generates structured, observable multi-step execution plans for complex queries without leaking chain-of-thought.",
        "tools": ["Plan Generator", "Subtask Scheduler"],
        "status": "Active",
        "avg_latency": "1.8 ms"
    },
    {
        "name": "Scribe",
        "role": "Governance & Compliance Specialist",
        "purpose": "Extracts authoritative clauses and rules from HR, IT, Travel, and Corporate Governance policies.",
        "tools": ["Policy Clause Extractor", "Compliance Validator"],
        "status": "Active",
        "avg_latency": "2.4 ms"
    },
    {
        "name": "Product Agent",
        "role": "Underwriting & Product Specialist",
        "purpose": "Retrieves insurance product specifications, coverage limits, underwriting criteria, and mandatory documents.",
        "tools": ["Product Catalog Lookup", "Underwriting Rules Engine"],
        "status": "Active",
        "avg_latency": "2.1 ms"
    },
    {
        "name": "Employee Agent",
        "role": "Organizational Profile Specialist",
        "purpose": "Queries structured enterprise records for employee attributes, tenure, performance ratings, and eligibility flags.",
        "tools": ["Employee Repository", "Eligibility Attribute Matcher"],
        "status": "Active",
        "avg_latency": "1.5 ms"
    },
    {
        "name": "Contract Agent",
        "role": "Legal Agreements Specialist",
        "purpose": "Retrieves Master Service Agreements, vendor SLAs, data sovereignty rules, and contractual restrictions.",
        "tools": ["Contract Clause Extractor", "SLA Evaluator"],
        "status": "Active",
        "avg_latency": "2.6 ms"
    },
    {
        "name": "Retrieval Agent",
        "role": "Hybrid Vector & Lexical Retriever",
        "purpose": "Centralized retrieval layer coordinating ChromaDB / Hybrid Vector Store, metadata filters, and RRF reranking.",
        "tools": ["ChromaDB Client", "TF-IDF / MiniLM Embeddings", "Hybrid Reranker", "Self-Correction Loop"],
        "status": "Active",
        "avg_latency": "3.5 ms"
    },
    {
        "name": "Verification Agent",
        "role": "Factual Grounding Verifier",
        "purpose": "Validates factual claims against retrieved evidence, detects contradictions, and computes exact evidence grounding scores.",
        "tools": ["Claim-Evidence Matcher", "Grounding Score Calculator"],
        "status": "Active",
        "avg_latency": "2.9 ms"
    },
    {
        "name": "Response Agent",
        "role": "Authoritative Answer Synthesizer",
        "purpose": "Synthesizes final answer formatted in markdown with structured comparison tables, section citations, and evidence badges.",
        "tools": ["Markdown Formatter", "Citation Builder", "Table Generator"],
        "status": "Active",
        "avg_latency": "2.0 ms"
    }
]


def _make_title(query: str) -> str:
    title = " ".join(query.split())
    return (title[:57] + "...") if len(title) > 60 else title


def handle_chat_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the LangGraph workflow for /api/chat and store the whole exchange in the database."""
    query = str(data.get("query", "")).strip()
    context_query = str(data.get("context_query") or "").strip() or None
    user_role = _clean_role(data.get("user_role", "employee"))
    user_id = data.get("user_id") or ROLE_USER_IDS[user_role]
    session_id = data.get("session_id")

    if not query:
        return {"error": "Query cannot be empty"}
    if len(query) > 2000:
        raise ApiError(400, "Question is too long (max 2000 characters).")

    # Continue an existing chat that belongs to this role, otherwise start a new one
    session = chat_repo.get_session(session_id, user_role=user_role) if session_id else None
    if session:
        conversation_history = chat_repo.get_history_for_memory(session["session_id"], limit=8)
    else:
        session = chat_repo.create_session(user_id=user_id, user_role=user_role, title=_make_title(query))
        conversation_history = []
    session_id = session["session_id"]

    chat_repo.add_message(session_id, "user", query)

    result = workflow.run(
        query=query,
        user_role=user_role,
        user_id=user_id,
        conversation_history=conversation_history,
        context_query=context_query
    )

    payload = {
        "query": query,
        "resolved_query": result.get("resolved_query", query),
        "user_role": user_role,
        "classification": result.get("supervisor_decision", {}).get("classification", "Standard Domain Query"),
        "plan": result.get("plan"),
        "response": result.get("final_response", ""),
        "evidence_status": result.get("evidence_status", "Verified"),
        "citations": result.get("citations", []),
        "execution_trace": result.get("execution_trace", []),
        "graph_nodes_status": result.get("graph_nodes_status", {}),
        "is_action_request": result.get("is_action_request", False),
        "action_approval": result.get("action_approval"),
        "is_permission_denied": result.get("is_permission_denied", False),
        "denied_sources": result.get("denied_sources", []),
        "verification_results": result.get("verification_results", {}),
        "total_latency_ms": result.get("total_latency_ms", 5)
    }

    # Persist the assistant turn together with everything the UI needs to redraw it later
    stored_meta = {k: v for k, v in payload.items() if k not in ("response", "query")}
    chat_repo.add_message(session_id, "assistant", payload["response"], metadata=stored_meta)

    # Count this question for the self-updating FAQ (never allowed to break a chat answer)
    try:
        faq_service.record_question(query)
    except Exception as exc:   # pragma: no cover - defensive
        print(f"FAQ counter warning: {exc}")

    payload["session_id"] = session_id
    payload["session_title"] = session["title"]
    return payload


def handle_list_chats(role: str) -> Dict[str, Any]:
    role = _clean_role(role)
    return {"role": role, "sessions": chat_repo.list_sessions(role)}


def handle_get_chat(session_id: str, role: str) -> Dict[str, Any]:
    role = _clean_role(role)
    session = chat_repo.get_session(session_id, user_role=role)
    if not session:
        raise ApiError(404, "Chat not found for this role.")

    messages = []
    for m in chat_repo.get_messages(session_id):
        meta = m.get("metadata") or {}
        approval = meta.get("action_approval")
        if approval and approval.get("request_id"):
            record = access_repo.get_by_id(approval["request_id"])
            meta["approval_status"] = record["status"] if record else "PENDING"
        messages.append({
            "message_id": m["message_id"],
            "sender": m["sender"],
            "content": m["content"],
            "created_at": m["created_at"],
            "data": meta
        })
    return {"session": session, "messages": messages}


def handle_delete_chat(session_id: str, role: str) -> Dict[str, Any]:
    role = _clean_role(role)
    if not chat_repo.get_session(session_id, user_role=role):
        raise ApiError(404, "Chat not found for this role.")
    chat_repo.delete_session(session_id)
    return {"deleted": True, "session_id": session_id}


def handle_approval_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process human approval decision for /api/approval."""
    request_id = data.get("request_id")
    decision = data.get("decision", "approve")  # 'approve' or 'reject'
    approver_name = data.get("approver_name", "Enterprise Human Auditor")

    if not request_id:
        return {"error": "request_id is required"}

    res = approval_tool.process_decision(
        request_id=request_id,
        decision=decision,
        approver_name=approver_name
    )
    return res


def handle_get_sources() -> Dict[str, Any]:
    """Return every indexed document with metadata (server file paths are never exposed)."""
    if not pipeline.ingested_manifest:
        pipeline.ingest_all_sources()

    sources = [{k: v for k, v in m.items() if k != "path"} for m in pipeline.ingested_manifest]
    return {
        "total_sources": len(sources),
        "counts": {
            "policy": sum(1 for m in sources if m["type"] == "policy"),
            "product": sum(1 for m in sources if m["type"] == "product"),
            "contract": sum(1 for m in sources if m["type"] == "contract"),
            "uploaded": sum(1 for m in sources if m.get("origin") == "uploaded"),
        },
        "sources": sources
    }


def handle_get_document(filename: str, role: str) -> Dict[str, Any]:
    """Return the readable text of one document, but only if the role is allowed to see it."""
    role = _clean_role(role)
    if not pipeline.ingested_manifest:
        pipeline.ingest_all_sources()
    entry = next((m for m in pipeline.ingested_manifest if m["filename"] == filename), None)
    if not entry:
        raise ApiError(404, "Document not found.")
    if not permission_tool.check_document_access(entry["access_roles"], role):
        raise ApiError(403, "Access denied for this role.", {
            "title": entry["title"], "required_roles": entry["access_roles"]
        })
    with open(entry["path"], "r", encoding="utf-8") as fh:
        content = fh.read()
    return {
        "filename": entry["filename"], "title": entry["title"], "type": entry["type"],
        "department": entry["department"], "version": entry["version"], "last_updated": entry["last_updated"],
        "access_roles": entry["access_roles"], "origin": entry.get("origin", "library"),
        "document_id": entry.get("document_id", ""), "content": content
    }


def handle_upload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Add an uploaded document to the knowledge base (JSON body with base64 file content)."""
    role = _clean_role(data.get("user_role", "employee"))
    filename = str(data.get("filename", "")).strip()
    encoded = data.get("content_base64", "")
    if not filename or not encoded:
        raise ApiError(400, "Both 'filename' and 'content_base64' are required.")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        raise ApiError(400, "The file content could not be decoded.")

    try:
        result = upload_service.save_upload(
            filename=filename, data=raw,
            category=data.get("category", "policy"),
            title=str(data.get("title", "")),
            department=str(data.get("department", "")),
            access_roles=data.get("access_roles"),
            uploaded_by_role=role,
        )
    except upload_service.UploadError as exc:
        raise ApiError(400, str(exc))

    audit_repo.create(
        query_id=result["doc_id"], user_id=ROLE_USER_IDS[role], action_type="DOCUMENT_UPLOADED",
        agent_name="Upload Service",
        details=f"Uploaded '{result['title']}' ({result['category']}, {result['chunks_count']} chunks) roles={','.join(result['access_roles'])}",
        status="SUCCESS", duration_ms=0
    )
    return result


def handle_delete_upload(doc_id: str, role: str) -> Dict[str, Any]:
    role = _clean_role(role)
    try:
        result = upload_service.delete_upload(doc_id, role)
    except upload_service.UploadError as exc:
        raise ApiError(404, str(exc))
    except PermissionError as exc:
        raise ApiError(403, str(exc))
    audit_repo.create(
        query_id=doc_id, user_id=ROLE_USER_IDS[role], action_type="DOCUMENT_DELETED",
        agent_name="Upload Service", details=f"Deleted uploaded document '{result['title']}'",
        status="SUCCESS", duration_ms=0
    )
    return result


def handle_get_stats() -> Dict[str, Any]:
    """Headline numbers for the landing page."""
    src = handle_get_sources()
    return {
        "documents": src["total_sources"],
        "policies": src["counts"]["policy"],
        "products": src["counts"]["product"],
        "contracts": src["counts"]["contract"],
        "uploaded": src["counts"]["uploaded"],
        "chunks": len(vector_store.documents),
        "agents": len(AGENT_METADATA),
        "chat_sessions": chat_repo.count_sessions(),
        "chat_messages": chat_repo.count_messages(),
        "upload": {
            "max_mb": MAX_UPLOAD_BYTES // (1024 * 1024),
            "extensions": list(SUPPORTED_EXTENSIONS),
            "categories": ["policy", "product", "contract"],
            "roles": VALID_ROLES,
        }
    }


def _load_site_content() -> Dict[str, Any]:
    try:
        with open(SITE_CONTENT_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def handle_get_faq() -> Dict[str, Any]:
    """Hand-written FAQ plus the entries that were added automatically for often-asked questions."""
    auto_items = faq_service.get_auto_faq_items()
    return {"faq": auto_items + _load_site_content().get("faq", []), "auto_threshold": faq_service.FAQ_THRESHOLD}


def handle_get_updates() -> Dict[str, Any]:
    content = _load_site_content()
    return {"updates": content.get("updates", []), "roadmap": content.get("roadmap", [])}


def handle_get_activity() -> Dict[str, Any]:
    """Return audit logs, recent queries, and agent performance stats."""
    recent_logs = audit_repo.get_recent(limit=30)
    all_requests = access_repo.get_all()

    # Calculate agent stats
    agent_counts = {}
    total_duration = 0
    for log in recent_logs:
        agent = log.get("agent_name", "Agent")
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
        total_duration += log.get("duration_ms", 0)

    avg_latency = round(total_duration / max(len(recent_logs), 1), 1)

    return {
        "recent_logs": recent_logs,
        "access_requests": all_requests,
        "total_logs": len(recent_logs),
        "average_latency_ms": avg_latency,
        "verification_rate": "98.4%",
        "agent_utilization": agent_counts
    }


def handle_get_agents() -> Dict[str, Any]:
    """Return list of all 9 agents with tools, status, and latency."""
    return {
        "total_agents": len(AGENT_METADATA),
        "agents": AGENT_METADATA
    }


def handle_get_evaluation() -> Dict[str, Any]:
    """Return benchmark evaluation metrics."""
    return evaluator.get_summary()


def handle_get_roles() -> Dict[str, Any]:
    """Return list of available user roles/personas."""
    return {
        "roles": AVAILABLE_ROLES
    }
