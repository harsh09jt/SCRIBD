"""
Employee Agent.
Queries the enterprise employee database, retrieves profile details,
and evaluates organizational eligibility attributes.
"""

from typing import Dict, Any, Optional
from backend.database.repositories import EmployeeRepository


class EmployeeAgent:
    def __init__(self):
        self.name = "Employee Agent"
        self.repo = EmployeeRepository()

    def execute(self, query: str) -> Dict[str, Any]:
        """Extract employee entity from query and return record."""
        # Find employee name from query
        q_lower = query.lower()
        matched_employee = None

        all_employees = self.repo.get_all()
        for emp in all_employees:
            first_name = emp["name"].split()[0].lower()
            if first_name in q_lower or emp["name"].lower() in q_lower:
                matched_employee = emp
                break

        if not matched_employee:
            # Fallback search
            results = self.repo.search(query[:20])
            if results:
                matched_employee = results[0]

        if matched_employee:
            return {
                "success": True,
                "agent": self.name,
                "employee": matched_employee,
                "summary": (
                    f"Employee: {matched_employee['name']} ({matched_employee['employee_id']}) | "
                    f"Role: {matched_employee['role']} ({matched_employee['department']}) | "
                    f"Location: {matched_employee['location']} | "
                    f"Tenure: {matched_employee['tenure_months']} months | "
                    f"Performance Rating: {matched_employee['performance_rating']} | "
                    f"Remote Eligible Flag: {'Yes (1)' if matched_employee['remote_eligible'] else 'No (0)'} | "
                    f"Manager: {matched_employee['manager']}"
                )
            }
        else:
            return {
                "success": False,
                "agent": self.name,
                "employee": None,
                "summary": "No matching employee record found in enterprise database."
            }


# Singleton
_employee_agent = None

def get_employee_agent() -> EmployeeAgent:
    global _employee_agent
    if _employee_agent is None:
        _employee_agent = EmployeeAgent()
    return _employee_agent

