"""
Policy lookup and clause extraction tool.
"""

from typing import List, Dict, Any
from backend.rag.retriever import get_retriever


class PolicyTool:
    def __init__(self):
        self.retriever = get_retriever()

    def get_policy_clauses(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve policy sections matching query with citations."""
        return self.retriever.search_policies(query=query, k=k)


# Singleton
_policy_tool = None

def get_policy_tool() -> PolicyTool:
    global _policy_tool
    if _policy_tool is None:
        _policy_tool = PolicyTool()
    return _policy_tool
