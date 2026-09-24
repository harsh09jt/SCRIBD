"""
Retrieval Agent.
Centralized retrieval layer coordinating ChromaDB / Hybrid Vector Store,
metadata filtering, reciprocal rank fusion reranking, and self-correcting query rewrites.
"""

from typing import Dict, Any, List, Optional
from backend.rag.retriever import get_retriever


class RetrievalAgent:
    def __init__(self):
        self.name = "Retrieval Agent"
        self.purpose = "Centralized retrieval layer executing hybrid vector + lexical search, metadata filtering, and reranking."
        self.retriever = get_retriever()

    def execute(
        self,
        query: str,
        doc_type: Optional[str] = None,
        department: Optional[str] = None,
        k: int = 4,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """Execute centralized hybrid retrieval."""
        res = self.retriever.search_with_self_correction(
            query=query,
            k=k,
            doc_type=doc_type,
            user_role=user_role
        )

        chunks = res.get("chunks", [])
        denied_sources = res.get("denied_sources", [])
        is_permission_denied = res.get("is_permission_denied", False)
        retrieval_history = res.get("retrieval_history", [])

        citations = []
        for c in chunks:
            citations.append({
                "document_name": c.get("document_name", "Enterprise Document"),
                "file_name": c.get("file_name", ""),
                "section": c.get("section", ""),
                "department": c.get("department", "Enterprise"),
                "version": c.get("version", "v1.0"),
                "last_updated": c.get("last_updated", "2026-08-01"),
                "access_roles": c.get("access_roles", ["employee", "admin"]),
                "similarity_score": c.get("similarity_score", 0.75),
                "rerank_score": c.get("rerank_score", 0.8),
                "content_preview": c.get("content", "")[:300]
            })

        return {
            "success": not is_permission_denied and len(chunks) > 0,
            "agent": self.name,
            "chunks": chunks,
            "citations": citations,
            "denied_sources": denied_sources,
            "is_permission_denied": is_permission_denied,
            "retrieval_history": retrieval_history,
            "summary": (
                f"Retrieved {len(chunks)} relevant chunk(s) across enterprise knowledge base."
                if not is_permission_denied else
                f"Blocked access to {len(denied_sources)} restricted document(s) due to RBAC policy."
            )
        }


# Singleton
_retrieval_agent = None

def get_retrieval_agent() -> RetrievalAgent:
    global _retrieval_agent
    if _retrieval_agent is None:
        _retrieval_agent = RetrievalAgent()
    return _retrieval_agent
