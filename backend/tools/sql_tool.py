"""
Safe SQL Query Tool with strict enterprise destructive command guardrails.
"""

import re
from typing import List, Dict, Any, Tuple
from backend.database.connection import get_db

DESTRUCTIVE_KEYWORDS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bUPDATE\b",
    r"\bINSERT\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bCREATE\b",
    r"\bREPLACE\b"
]


class SafeSQLTool:
    def __init__(self):
        self.db = get_db()

    def validate_query(self, query: str) -> Tuple[bool, str]:
        """Check if query is safe and strictly read-only."""
        clean_q = query.strip()
        if not clean_q.lower().startswith("select"):
            return False, "Security Violation: Only SELECT queries are permitted on enterprise tables."

        for pattern in DESTRUCTIVE_KEYWORDS:
            if re.search(pattern, clean_q, re.IGNORECASE):
                return False, f"Security Violation: Query contains prohibited destructive statement '{pattern.strip(r'\\b')}'. Blocked."

        return True, "Valid"

    def execute_safe_sql(self, query: str) -> Dict[str, Any]:
        """Validate and execute a read-only SQL query."""
        is_safe, msg = self.validate_query(query)
        if not is_safe:
            return {
                "success": False,
                "error": msg,
                "rows": [],
                "query": query
            }

        try:
            rows = self.db.execute_query(query)
            return {
                "success": True,
                "rows": rows,
                "row_count": len(rows),
                "query": query
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "rows": [],
                "query": query
            }


# Singleton
_sql_tool = None

def get_sql_tool() -> SafeSQLTool:
    global _sql_tool
    if _sql_tool is None:
        _sql_tool = SafeSQLTool()
    return _sql_tool
