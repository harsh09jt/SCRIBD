"""
Protected Access Request creation and workflow tool.
"""

from typing import Dict, Any
from backend.database.repositories import AccessRequestRepository, AuditLogRepository


class AccessRequestTool:
    def __init__(self):
        self.req_repo = AccessRequestRepository()
        self.audit_repo = AuditLogRepository()

    def create_pending_request(
        self,
        employee_id: str,
        employee_name: str,
        product_or_system: str,
        reason: str,
        risk_level: str,
        requested_operation: str
    ) -> Dict[str, Any]:
        """Create a pending access request awaiting Human-in-the-Loop approval."""
        req = self.req_repo.create(
            employee_id=employee_id,
            employee_name=employee_name,
            product_or_system=product_or_system,
            reason=reason,
            risk_level=risk_level,
            requested_operation=requested_operation
        )
        self.audit_repo.create(
            query_id=req["request_id"],
            user_id=employee_id,
            action_type="ACCESS_REQUEST_SUBMITTED",
            agent_name="Access Request Tool",
            details=f"Created pending access request for {employee_name} on {product_or_system} (Risk: {risk_level})",
            status="PENDING",
            duration_ms=45
        )
        return req

    def process_approval(
        self,
        request_id: str,
        approved: bool,
        approver_name: str = "Enterprise Human Auditor"
    ) -> Dict[str, Any]:
        """Finalize the access request upon human auditor decision."""
        status = "APPROVED" if approved else "REJECTED"
        success = self.req_repo.update_status(request_id, status, approver_name)
        
        req = self.req_repo.get_by_id(request_id)
        emp_id = req["employee_id"] if req else "EMP-UNKNOWN"
        emp_name = req["employee_name"] if req else "Employee"
        target = req["product_or_system"] if req else "System"

        self.audit_repo.create(
            query_id=request_id,
            user_id=emp_id,
            action_type=f"ACCESS_REQUEST_{status}",
            agent_name="Human Approval Agent",
            details=f"Request {request_id} was {status} by {approver_name} for {emp_name} on {target}",
            status="SUCCESS",
            duration_ms=60
        )

        return {
            "success": success,
            "request_id": request_id,
            "status": status,
            "approved_by": approver_name,
            "request": req
        }


# Singleton
_access_tool = None

def get_access_request_tool() -> AccessRequestTool:
    global _access_tool
    if _access_tool is None:
        _access_tool = AccessRequestTool()
    return _access_tool
