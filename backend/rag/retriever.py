"""
Enterprise Retriever with Hybrid Retrieval, Permission Filtering, and Self-Correction.
Supports semantic vector search, metadata filtering, hybrid reranking, and RBAC enforcement.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from backend.rag.vectorstore import get_vector_store
from backend.rag.ingestion import get_ingestion_pipeline
from backend.rag.reranker import get_reranker
from backend.tools.permission_tool import get_permission_tool


class EnterpriseRetriever:
    def __init__(self):
        self.vector_store = get_vector_store()
        self.reranker = get_reranker()
        self.permission_tool = get_permission_tool()
        
        # Ensure ingestion is initialized
        pipeline = get_ingestion_pipeline()
        if not self.vector_store.documents:
            pipeline.ingest_all_sources()

    def search(
        self,
        query: str,
        k: int = 5,
        doc_type: Optional[str] = None,
        department: Optional[str] = None,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """
        Execute Hybrid Retrieval with Permission Enforcement.
        Unauthorized chunks are filtered out BEFORE returning.
        """
        filter_dict = {}
        if doc_type:
            filter_dict["document_type"] = doc_type
        if department:
            filter_dict["department"] = department

        # Step 1: Initial Vector + Keyword Retrieval (fetch candidate pool)
        candidates = self.vector_store.search(
            query=query,
            k=max(k * 2, 8),
            filter_dict=filter_dict if filter_dict else None
        )

        # Step 2: Permission-Aware Filter (Unauthorized documents MUST NOT reach LLM)
        authorized_candidates, denied_sources = self.permission_tool.filter_chunks_for_user(
            candidates, user_role=user_role
        )

        # Check if the query specifically targeted a denied document (e.g. CEO compensation)
        q_lower = query.lower()
        specifically_targeted_denied = False
        restricted_keywords = ["ceo", "executive compensation", "ceo contract", "ceo compensation", "chief executive"]
        if any(k in q_lower for k in restricted_keywords):
            for d in denied_sources:
                d_name = d.get("document_name", "").lower()
                if "ceo" in d_name or "compensation" in d_name:
                    specifically_targeted_denied = True
                    break

        # Generalised RBAC rule: if the single best match for the question is a document this role may not
        # read, the person is asking about that restricted document, so answer "access denied" instead of
        # quietly substituting weaker matches.
        top_match_restricted = False
        if candidates and denied_sources:
            top = candidates[0]
            top_roles = top.get("access_roles") or top.get("metadata", {}).get("access_roles", [])
            if (top.get("similarity_score", 0) >= 0.30
                    and not self.permission_tool.check_document_access(top_roles, user_role)):
                top_match_restricted = True

        is_permission_denied = (
            specifically_targeted_denied
            or top_match_restricted
            or (len(authorized_candidates) == 0 and len(denied_sources) > 0)
        )

        if is_permission_denied:
            return {
                "query": query,
                "chunks": [],
                "total_found": 0,
                "denied_sources": denied_sources,
                "is_permission_denied": True
            }

        # Step 3: Hybrid Reranking on authorized candidates
        reranked = self.reranker.rerank(query=query, chunks=authorized_candidates, top_n=k)

        return {
            "query": query,
            "chunks": reranked,
            "total_found": len(reranked),
            "denied_sources": denied_sources,
            "is_permission_denied": False
        }

    def search_with_self_correction(
        self,
        query: str,
        k: int = 4,
        doc_type: Optional[str] = None,
        user_role: str = "employee",
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Self-Correcting RAG loop:
        If evidence retrieved has low confidence or insufficient depth,
        rewrites the search query and re-retrieves (capped at 2 retries).
        """
        attempt = 0
        current_query = query
        retrieval_history = []

        while attempt <= max_retries:
            res = self.search(
                query=current_query,
                k=k,
                doc_type=doc_type,
                user_role=user_role
            )
            retrieval_history.append({
                "attempt": attempt + 1,
                "query": current_query,
                "chunks_found": len(res["chunks"]),
                "denied_count": len(res["denied_sources"])
            })

            # If permission is denied, stop immediately - do not retry
            if res["is_permission_denied"]:
                res["retrieval_history"] = retrieval_history
                return res

            # Check if sufficient evidence was found. Require stronger evidence than a weak semantic match.
            chunks = res["chunks"]
            if chunks:
                top = chunks[0]
                top_score = top.get("rerank_score", top.get("similarity_score", 0.0))
                top_text = f"{top.get('document_name', '')} {top.get('section', '')} {top.get('content', '')}".lower()
                query_terms = [t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2]
                generic_terms = {
                    "what", "when", "where", "which", "show", "how", "tell", "the", "this", "that", "from",
                    "with", "into", "about", "your", "their", "there", "here", "best", "employee", "employees",
                    "company", "people", "document", "documents", "answer", "question", "policy", "policies",
                    "please", "can", "you", "me", "our", "for", "are", "is", "do", "does", "not",
                }
                specific_terms = [t for t in query_terms if t not in generic_terms]
                term_matches = sum(1 for t in specific_terms if t in top_text)
                has_strong_evidence = top_score >= 0.38 or (top_score >= 0.24 and term_matches >= max(1, min(3, len(specific_terms))))
                is_vague_or_unrelated = (
                    not specific_terms
                    or (top_score < 0.45 and term_matches == 0 and len(specific_terms) >= 1)
                    or (len(query.strip()) > 8 and len(specific_terms) == 0)
                )
            else:
                has_strong_evidence = False
                specific_terms = []
                term_matches = 0
                is_vague_or_unrelated = True

            if is_vague_or_unrelated:
                res["chunks"] = []
                res["total_found"] = 0
                res["insufficient_evidence"] = True
                res["retrieval_history"] = retrieval_history
                return res

            if has_strong_evidence or attempt == max_retries:
                res["retrieval_history"] = retrieval_history
                return res

            # Re-query conservatively so we do not drift toward unrelated enterprise documents.
            attempt += 1
            current_query = self._rewrite_query(query, attempt)

        res["retrieval_history"] = retrieval_history
        return res

    def _rewrite_query(self, query: str, attempt: int) -> str:
        """Conservative query refinement: preserve the user's actual subject to avoid broad drift."""
        clean = query.strip()
        if not clean:
            return clean

        q_lower = clean.lower()
        if "product x" in q_lower or "health shield" in q_lower:
            return "Corporate Health Shield product eligibility documentation requirements"
        elif "product y" in q_lower or "cyber risk" in q_lower:
            return "Cyber Risk Elite security requirements product underwriting documentation"
        elif "product z" in q_lower or "term life" in q_lower:
            return "Term Life Pro product benefits eligibility documentation"
        elif "remote work" in q_lower:
            return "remote work policy eligibility tenure rating approval hybrid model POL-HR-042"
        elif "vendor abc" in q_lower or "cloud hosting" in q_lower:
            return "Vendor ABC cloud hosting agreement data sovereignty SLA subcontractor restrictions"
        elif "annual leave" in q_lower:
            return "annual sick casual statutory leave policy entitlements carry forward lapse"
        elif "contract" in q_lower:
            return f"{clean} contractual restrictions compliance obligations"

        words = re.sub(r'\b(what|is|are|can|show|me|the|our|for|does|do|about|please|tell|give)\b', '', q_lower, flags=re.IGNORECASE)
        words = re.sub(r'\s+', ' ', words).strip()
        if attempt == 1:
            return f"{words} policy document" if words else clean
        return f"{clean} policy requirements evidence"

    def search_policies(self, query: str, k: int = 4, user_role: str = "employee") -> Dict[str, Any]:
        return self.search_with_self_correction(query=query, k=k, doc_type="policy", user_role=user_role)

    def search_products(self, query: str, k: int = 4, user_role: str = "employee") -> Dict[str, Any]:
        return self.search_with_self_correction(query=query, k=k, doc_type="product", user_role=user_role)

    def search_contracts(self, query: str, k: int = 4, user_role: str = "employee") -> Dict[str, Any]:
        return self.search_with_self_correction(query=query, k=k, doc_type="contract", user_role=user_role)


# Singleton
_retriever = None

def get_retriever() -> EnterpriseRetriever:
    global _retriever
    if _retriever is None:
        _retriever = EnterpriseRetriever()
    return _retriever
