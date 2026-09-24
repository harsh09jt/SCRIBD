"""
Permission Tool & Access Control Engine.
Enforces strict Document-Level Access Control (RBAC).

CRITICAL RULE:
Unauthorized documents MUST NOT reach the LLM.
Permission checking happens BEFORE retrieval results are passed to the model.
"""

from typing import List, Dict, Any, Tuple, Optional


# Role hierarchy definition: higher roles inherit permissions or have broader access
DEFAULT_ROLES = ["employee", "manager", "hr", "legal", "admin"]


class PermissionTool:
    """Document access control gatekeeper."""

    def __init__(self):
        pass

    def check_document_access(self, doc_roles: List[str], user_role: str) -> bool:
        """
        Check if a given user_role has access to a document chunk.
        Admin always has access.
        """
        if not user_role:
            user_role = "employee"
        user_role = user_role.lower().strip()

        # Admin superuser access
        if user_role == "admin":
            return True

        if not doc_roles:
            # Default to public internal access if unspecified
            return True

        normalized_doc_roles = [r.lower().strip() for r in doc_roles]
        return user_role in normalized_doc_roles

    def filter_chunks_for_user(
        self,
        chunks: List[Dict[str, Any]],
        user_role: str
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Filters out any chunks the user is not authorized to access.
        Returns (authorized_chunks, denied_chunks).
        """
        authorized = []
        denied = []

        for chunk in chunks:
            roles = chunk.get("access_roles") or chunk.get("metadata", {}).get("access_roles", [])
            doc_name = chunk.get("document_name", "Restricted Document")
            
            # Explicit check for CEO or Executive documents
            if ("ceo" in doc_name.lower() or "executive compensation" in doc_name.lower()) and not roles:
                roles = ["admin", "hr"]

            if self.check_document_access(roles, user_role):
                authorized.append(chunk)
            else:
                denied.append({
                    "document_name": doc_name,
                    "section": chunk.get("section", "Restricted Section"),
                    "required_roles": roles,
                    "user_role": user_role,
                    "reason": f"Access Denied: Requires one of [{', '.join(roles)}]. Current role '{user_role}' is not authorized."
                })

        return authorized, denied

    def get_role_description(self, role: str) -> str:
        descriptions = {
            "employee": "Standard Enterprise Employee — Access to standard company policies, products, public guidelines, and personal profile.",
            "manager": "Team Manager — Access to department policies, team member profiles, and vendor contracts.",
            "hr": "Human Resources Specialist — Access to all employee profiles, compensation policies, benefits, and executive compensation records.",
            "legal": "Legal & Compliance Counsel — Access to vendor contracts, regulatory agreements, SLAs, and governance policies.",
            "admin": "System Administrator / Executive Auditor — Full unconstrained access across all enterprise assets."
        }
        return descriptions.get(role.lower(), "Standard User")


# Singleton
_permission_tool = None

def get_permission_tool() -> PermissionTool:
    global _permission_tool
    if _permission_tool is None:
        _permission_tool = PermissionTool()
    return _permission_tool
