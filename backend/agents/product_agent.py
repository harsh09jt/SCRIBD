"""
Product Agent.
Specializes in enterprise insurance products, coverage limits,
eligibility prerequisites, and mandatory documentation.
"""

from typing import Dict, Any, List
from backend.database.repositories import ProductRepository
from backend.rag.retriever import get_retriever


class ProductAgent:
    def __init__(self):
        self.name = "Product Agent"
        self.purpose = "Retrieves product specifications, underwriting rules, and required onboarding/claim documentation."
        self.repo = ProductRepository()
        self.retriever = get_retriever()

    def execute(self, query: str, user_role: str = "employee") -> Dict[str, Any]:
        """Search products across database and vector store."""
        # 1. Check DB structured record
        q_lower = query.lower()
        matched_prod = None

        all_products = self.repo.get_all()
        for prod in all_products:
            p_name = prod["product_name"].lower()
            if p_name in q_lower or (p_name.split()[0] in q_lower and len(p_name.split()[0]) > 4):
                matched_prod = prod
                break

        # Fallback keyword match for "Product X" -> Corporate Health Shield
        if not matched_prod and ("product x" in q_lower or "health shield" in q_lower):
            matched_prod = self.repo.get_by_name("Corporate Health Shield")
        elif not matched_prod and ("product y" in q_lower or "cyber risk" in q_lower):
            matched_prod = self.repo.get_by_name("Cyber Risk Elite")
        elif not matched_prod and ("product z" in q_lower or "term life" in q_lower):
            matched_prod = self.repo.get_by_name("Term Life Pro")

        # 2. Retrieve vector store documentation
        retrieval_res = self.retriever.search_products(query=query, k=3, user_role=user_role)
        vector_chunks = retrieval_res.get("chunks", [])

        citations = []
        for v in vector_chunks:
            citations.append({
                "document_name": v.get("document_name", "Product Specification"),
                "file_name": v.get("file_name", ""),
                "section": v.get("section", ""),
                "department": "Insurance Underwriting",
                "version": v.get("version", "v1.0"),
                "last_updated": v.get("last_updated", "2026-08-01"),
                "similarity_score": v.get("similarity_score", 0.8),
                "rerank_score": v.get("rerank_score", 0.8),
                "content_preview": v.get("content", "")[:280]
            })

        return {
            "success": matched_prod is not None or len(vector_chunks) > 0,
            "agent": self.name,
            "product_record": matched_prod,
            "documentation_chunks": vector_chunks,
            "citations": citations,
            "summary": (
                f"Product: {matched_prod['product_name']} ({matched_prod['category']}) | "
                f"Eligibility: {matched_prod['eligibility']} | "
                f"Requirements: {matched_prod['requirements']} | "
                f"Price: {matched_prod['price']} | "
                f"Underwriter: {matched_prod['underwriter']}"
            ) if matched_prod else f"Retrieved {len(vector_chunks)} product documentation sections."
        }


# Singleton
_product_agent = None

def get_product_agent() -> ProductAgent:
    global _product_agent
    if _product_agent is None:
        _product_agent = ProductAgent()
    return _product_agent
