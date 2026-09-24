"""
Policy Agent.
Searches corporate governance, HR, and compliance policy documents,
extracts authoritative clauses, and returns structured section citations.
"""

from typing import Dict, Any, List
from backend.rag.retriever import get_retriever


class PolicyAgent:
    def __init__(self):
        self.name = "Policy Agent"
        self.purpose = "Extracts authoritative clauses and rules from HR, IT, and compliance governance policies."
        self.retriever = get_retriever()

    def execute(self, query: str, user_role: str = "employee") -> Dict[str, Any]:
        """Search policies and return relevant clauses with citations."""
        res = self.retriever.search_policies(query=query, k=3, user_role=user_role)
        results = res.get("chunks", [])
        denied = res.get("denied_sources", [])
        is_denied = res.get("is_permission_denied", False)

        citations = []
        snippets = []

        for r in results:
            cit = {
                "document_name": r.get("document_name", "Corporate Policy"),
                "file_name": r.get("file_name", ""),
                "section": r.get("section", ""),
                "department": r.get("department", "Governance"),
                "version": r.get("version", "v1.0"),
                "last_updated": r.get("last_updated", "2026-08-01"),
                "similarity_score": r.get("similarity_score", 0.8),
                "rerank_score": r.get("rerank_score", 0.8),
                "content_preview": r.get("content", "")[:280]
            }
            citations.append(cit)
            snippets.append(f"[{r.get('document_name')} - {r.get('section')}]: {r.get('content')[:250]}...")

        return {
            "success": not is_denied and len(results) > 0,
            "agent": self.name,
            "retrieved_policies": results,
            "citations": citations,
            "denied_sources": denied,
            "is_permission_denied": is_denied,
            "summary": f"Retrieved {len(results)} authoritative policy section(s)." if not is_denied else "Access Denied.",
            "snippets": snippets
        }


# Singleton
_policy_agent = None

def get_policy_agent() -> PolicyAgent:
    global _policy_agent
    if _policy_agent is None:
        _policy_agent = PolicyAgent()
    return _policy_agent
