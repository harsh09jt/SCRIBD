import re
from typing import Any, Dict, List, Optional

from backend.llm.gemini_client import get_gemini_client
from backend.rag.retriever import get_retriever


class AgenticSupervisor:
    def decide(self, query: str, user_role: str = "employee") -> str:
        q = query.lower()
        if any(k in q for k in ["remote work", "leave", "annual leave", "sick", "maternity", "vacation", "travel", "expense", "performance", "manager", "recruitment", "hiring"]) :
            return "hr"
        if any(k in q for k in ["privacy", "gdpr", "security", "acceptable use", "compliance", "audit", "access control", "vendor", "contract", "sla", "data sovereignty", "risk"]):
            return "compliance"
        return "policy"


class PolicyAgent:
    def __init__(self):
        self.name = "Policy Agent"
        self.retriever = get_retriever()
        self.client = get_gemini_client()

    def answer(self, query: str, user_role: str = "employee", chunks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        source_chunks = chunks or self.retriever.search_policies(query=query, k=4, user_role=user_role).get("chunks", [])
        evidence = self._prepare_citations(source_chunks)
        prompt = self.client.build_policy_prompt(query, source_chunks, user_role) if self.client.enabled else ""
        llm_answer = self.client.generate(prompt) if self.client.enabled else ""

        answer = llm_answer.strip() if llm_answer else self._fallback_summary(query, source_chunks)
        return {"agent": self.name, "answer": answer, "citations": evidence}

    def _prepare_citations(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {
                "document_name": c.get("document_name", "Policy Document"),
                "section": c.get("section", "Overview"),
                "version": c.get("version", "v1.0"),
                "last_updated": c.get("last_updated", "n/a"),
                "content_preview": (c.get("content", "")[:220]).strip(),
            }
            for c in chunks[:6]
        ]

    def _fallback_summary(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "I could not find a policy document in the enterprise knowledge base that directly answers this question."
        top = chunks[0]
        content = top.get("content", "").strip()
        doc = top.get("document_name", "Corporate Policy")
        return f"Based on the retrieved {doc} guidance, the relevant answer is: {content[:600]}"


class ComplianceAgent:
    def __init__(self):
        self.name = "Compliance Agent"
        self.retriever = get_retriever()
        self.client = get_gemini_client()

    def answer(self, query: str, user_role: str = "employee", chunks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        source_chunks = chunks or self.retriever.search(query=query, k=5, user_role=user_role).get("chunks", [])
        evidence = [
            {
                "document_name": c.get("document_name", "Compliance Document"),
                "section": c.get("section", "Overview"),
                "version": c.get("version", "v1.0"),
                "last_updated": c.get("last_updated", "n/a"),
                "content_preview": (c.get("content", "")[:220]).strip(),
            }
            for c in source_chunks[:6]
        ]
        prompt = self.client.build_policy_prompt(query, source_chunks, user_role) if self.client.enabled else ""
        llm_answer = self.client.generate(prompt) if self.client.enabled else ""
        answer = llm_answer.strip() if llm_answer else self._fallback_summary(query, source_chunks)
        return {"agent": self.name, "answer": answer, "citations": evidence}

    def _fallback_summary(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "I do not have enough policy evidence to answer the compliance question without guessing."
        return "The applicable compliance requirement is supported by the retrieved enterprise documents and should be interpreted using the cited sections below."


class HRAgent:
    def __init__(self):
        self.name = "HR Agent"
        self.retriever = get_retriever()
        self.client = get_gemini_client()

    def answer(self, query: str, user_role: str = "employee", chunks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        source_chunks = chunks or self.retriever.search_policies(query=query, k=5, user_role=user_role).get("chunks", [])
        evidence = [
            {
                "document_name": c.get("document_name", "HR Policy Document"),
                "section": c.get("section", "Overview"),
                "version": c.get("version", "v1.0"),
                "last_updated": c.get("last_updated", "n/a"),
                "content_preview": (c.get("content", "")[:220]).strip(),
            }
            for c in source_chunks[:6]
        ]
        prompt = self.client.build_policy_prompt(query, source_chunks, user_role) if self.client.enabled else ""
        llm_answer = self.client.generate(prompt) if self.client.enabled else ""
        answer = llm_answer.strip() if llm_answer else self._fallback_summary(query, source_chunks)
        return {"agent": self.name, "answer": answer, "citations": evidence}

    def _fallback_summary(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return "I could not confirm the employee policy answer from the current enterprise documents."
        return "The relevant HR guidance is present in the retrieved policy sections listed below."


class AgenticRAGPipeline:
    def __init__(self):
        self.supervisor = AgenticSupervisor()
        self.policy_agent = PolicyAgent()
        self.compliance_agent = ComplianceAgent()
        self.hr_agent = HRAgent()

    def _is_meaningful_query(self, query: str) -> bool:
        terms = [
            t for t in re.findall(r"[a-z0-9]+", query.lower())
            if len(t) > 2 and t not in {
                "what", "when", "where", "which", "show", "how", "tell", "the", "this", "that",
                "from", "with", "into", "about", "your", "their", "there", "here", "can", "you", "me",
                "our", "for", "are", "is", "do", "does", "not", "best", "employee", "employees",
                "company", "people", "document", "documents", "answer", "question", "policy", "policies",
                "please"
            }
        ]
        return bool(terms)

    def answer(self, query: str, state: Dict[str, Any]) -> Dict[str, Any]:
        role = state.get("user_role", "employee")
        route = self.supervisor.decide(query, role)
        chunks = state.get("retrieved_chunks", [])

        if not self._is_meaningful_query(query):
            return {
                "agent": "Policy Agent",
                "answer": "",
                "citations": state.get("citations", []),
                "route": route,
                "grounded": False,
                "model": "local-rag-fallback",
            }

        # If Gemini is not configured, do not override the proven grounded workflow.
        if not self.policy_agent.client.enabled:
            return {
                "agent": "Policy Agent",
                "answer": "",
                "citations": state.get("citations", []),
                "route": route,
                "grounded": bool(chunks),
                "model": "local-rag-fallback",
            }

        if not chunks:
            retriever = get_retriever()
            if route == "hr":
                res = retriever.search_policies(query=query, k=4, user_role=role)
            elif route == "compliance":
                res = retriever.search(query=query, k=5, user_role=role)
            else:
                res = retriever.search_policies(query=query, k=4, user_role=role)
            chunks = res.get("chunks", [])

        if route == "hr":
            agent_output = self.hr_agent.answer(query, role, chunks)
        elif route == "compliance":
            agent_output = self.compliance_agent.answer(query, role, chunks)
        else:
            agent_output = self.policy_agent.answer(query, role, chunks)

        return {
            "agent": agent_output["agent"],
            "answer": agent_output["answer"],
            "citations": agent_output["citations"],
            "route": route,
            "grounded": bool(chunks) and self._is_meaningful_query(query),
            "model": "gemini-2.5-flash",
        }


def get_agentic_rag_pipeline() -> AgenticRAGPipeline:
    return AgenticRAGPipeline()
