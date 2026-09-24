"""
Approval Tool for Human-in-the-Loop Actions.
Handles creation, status transitions, and audit trail for sensitive enterprise actions
such as 'Create Remote Work Request'.
Persists all changes to SQLite enterprise database.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.database.repositories import AccessRequestRepository, AuditLogRepository


class ApprovalTool:
    def __init__(self):
        self.req_repo = AccessRequestRepository()
        self.audit_repo = AuditLogRepository()

    def prepare_remote_work_request(
        self,
        employee_name: str = "Rahul Sharma",
        employee_id: str = "EMP-001",
        reason: str = "Eligible under current policy (Tenure: 18 months, Rating: 4.2)",
        evidence_source: str = "Remote Work Policy (POL-HR-042) — Section 1 & 2"
    ) -> Dict[str, Any]:
        """Create a pending action request awaiting auditor approval."""
        req_id = f"RWR-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:4].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        req_data = {
            "request_id": req_id,
            "action_type": "Create Remote Work Request",
            "employee_id": employee_id,
            "employee_name": employee_name,
            "product_or_system": "Enterprise Hybrid / Remote Work Portal",
            "reason": reason,
            "evidence_source": evidence_source,
            "risk_level": "Medium",
            "status": "PENDING",
            "requested_operation": "Grant Hybrid/Remote Work Authorization (Hybrid 3/2 Model)",
            "request_timestamp": timestamp
        }

        # Save to database
        self.req_repo.create(
            employee_id=employee_id,
            employee_name=employee_name,
            product_or_system="Enterprise Hybrid / Remote Work Portal",
            reason=f"{reason} | Evidence: {evidence_source}",
            risk_level="Medium",
            requested_operation="Grant Hybrid/Remote Work Authorization (Hybrid 3/2 Model)",
            request_id=req_id
        )

        # Log to audit trail
        self.audit_repo.create(
            query_id=req_id,
            user_id=employee_id,
            action_type="ACTION_REQUEST_PREPARED",
            agent_name="Approval Tool",
            details=f"Prepared remote work authorization request for {employee_name}. Awaiting Human Auditor sign-off.",
            status="PENDING",
            duration_ms=40
        )

        return req_data

    def process_decision(
        self,
        request_id: str,
        decision: str,  # 'approve' or 'reject'
        approver_name: str = "Enterprise Human Auditor"
    ) -> Dict[str, Any]:
        """Finalize the action request based on human auditor decision."""
        approved = decision.lower() == "approve"
        new_status = "APPROVED" if approved else "REJECTED"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        success = self.req_repo.update_status(
            request_id=request_id,
            status=new_status,
            approved_by=approver_name
        )

        # Fetch updated request
        req = self.req_repo.get_by_id(request_id)
        emp_name = req["employee_name"] if req else "Rahul Sharma"
        emp_id = req["employee_id"] if req else "EMP-001"

        # Log audit entry
        self.audit_repo.create(
            query_id=request_id,
            user_id=emp_id,
            action_type=f"HUMAN_AUDITOR_{new_status}",
            agent_name="Human-in-the-Loop Auditor",
            details=f"Action '{request_id}' was {new_status} by {approver_name} for {emp_name}.",
            status="SUCCESS",
            duration_ms=65
        )

        return {
            "success": True,
            "request_id": request_id,
            "status": new_status,
            "approved_by": approver_name,
            "timestamp": timestamp,
            "message": f"✓ Request {new_status.lower()} successfully" if approved else "✗ Request rejected by human auditor",
            "request": req
        }

    def get_all_requests(self) -> List[Dict[str, Any]]:
        return self.req_repo.get_all()


# Singleton
_approval_tool = None

def get_approval_tool() -> ApprovalTool:
    global _approval_tool
    if _approval_tool is None:
        _approval_tool = ApprovalTool()
    return _approval_tool
