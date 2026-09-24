"""
Contract Agent.
Specializes in enterprise vendor contracts, Master Service Agreements (MSAs),
Service Level Agreements (SLAs), compliance obligations, and operational restrictions.
"""

from typing import Dict, Any, List
from backend.database.repositories import ContractRepository
from backend.rag.retriever import get_retriever


class ContractAgent:
    def __init__(self):
        self.name = "Contract Agent"
        self.purpose = "Analyzes corporate agreements, vendor SLAs, data sovereignty, and legal restrictions."
        self.repo = ContractRepository()
        self.retriever = get_retriever()

    def execute(self, query: str, user_role: str = "employee") -> Dict[str, Any]:
        """Search contracts across database and permission-filtered vector store."""
        q_lower = query.lower()
        matched_contract = None

        # 1. Search database records
        all_contracts = self.repo.get_all()
        for cnt in all_contracts:
            v_name = cnt.get("vendor_name", "").lower()
            if any(k in q_lower for k in ["vendor abc", "abc"]) and "vendor abc" in v_name:
                matched_contract = cnt
                break
            elif any(k in q_lower for k in ["tpa", "mediclaim", "global health"]) and "mediclaim" in v_name:
                matched_contract = cnt
                break
            elif any(k in q_lower for k in ["delta", "logistics", "fleet"]) and "delta" in v_name:
                matched_contract = cnt
                break
            elif any(k in q_lower for k in ["legal", "morrison", "counsel"]) and "morrison" in v_name:
                matched_contract = cnt
                break
            elif any(k in q_lower for k in ["zenith", "secops", "soc"]) and "zenith" in v_name:
                matched_contract = cnt
                break
            elif any(k in q_lower for k in ["ceo", "compensation", "executive"]) and "executive" in v_name:
                matched_contract = cnt
                break

        # 2. Retrieve vector store documentation with permission awareness
        retrieval_res = self.retriever.search_contracts(query=query, k=3, user_role=user_role)
        vector_chunks = retrieval_res["chunks"]
        denied_sources = retrieval_res["denied_sources"]
        is_permission_denied = retrieval_res["is_permission_denied"]

        citations = []
        for v in vector_chunks:
            citations.append({
                "document_name": v.get("document_name", "Vendor Contract"),
                "file_name": v.get("file_name", ""),
                "section": v.get("section", ""),
                "department": "Procurement & Legal",
                "version": v.get("version", "v1.0"),
                "last_updated": v.get("last_updated", "2026-08-01"),
                "similarity_score": v.get("similarity_score", 0.8),
                "rerank_score": v.get("rerank_score", 0.8),
                "content_preview": v.get("content", "")[:280]
            })

        return {
            "success": not is_permission_denied and (matched_contract is not None or len(vector_chunks) > 0),
            "agent": self.name,
            "contract_record": matched_contract if not is_permission_denied else None,
            "documentation_chunks": vector_chunks,
            "citations": citations,
            "denied_sources": denied_sources,
            "is_permission_denied": is_permission_denied,
            "summary": (
                f"Contract: {matched_contract['vendor_name']} ({matched_contract['contract_type']}) | "
                f"SLA: {matched_contract['sla_uptime']} | "
                f"Governing Law: {matched_contract['governing_law']} | "
                f"Status: {matched_contract['status']}"
            ) if matched_contract and not is_permission_denied else (
                "Permission Denied: Access to restricted executive agreement is prohibited."
                if is_permission_denied else f"Retrieved {len(vector_chunks)} contractual clauses."
            )
        }


# Singleton
_contract_agent = None

def get_contract_agent() -> ContractAgent:
    global _contract_agent
    if _contract_agent is None:
        _contract_agent = ContractAgent()
    return _contract_agent
