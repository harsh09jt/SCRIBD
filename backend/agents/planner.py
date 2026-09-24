"""
Planner Agent.
Decomposes complex multi-domain enterprise queries into structured, observable execution plans.
Provides clean summaries for user visibility without exposing internal chain-of-thought.
"""

import uuid
import re
from typing import Dict, Any, List


class PlannerAgent:
    """Creates explicit structured execution plans for complex queries."""

    def __init__(self):
        self.name = "Planner Agent"
        self.purpose = "Analyzes complex multi-domain queries and formulates a step-by-step observable execution plan."

    def generate_plan(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate safe, structured execution plan."""
        q_lower = query.lower()
        plan_id = f"PLAN-{uuid.uuid4().hex[:6].upper()}"

        # Demo 2 pattern: "Can Rahul purchase Product X and what documents are required?"
        if ("purchase" in q_lower or "eligible" in q_lower or "can " in q_lower) and \
           ("product" in q_lower or "health shield" in q_lower or "cyber risk" in q_lower or "term life" in q_lower) and \
           any(name in q_lower for name in ["rahul", "priya", "amit", "neha", "vikram", "sneha"]):
            
            # Extract employee name
            emp_name = "Rahul"
            for n in ["Rahul", "Priya", "Amit", "Neha", "Vikram", "Sneha"]:
                if n.lower() in q_lower:
                    emp_name = n
                    break

            # Extract product name
            prod_name = "Product X"
            if "product x" in q_lower or "health shield" in q_lower:
                prod_name = "Product X (Corporate Health Shield)"
            elif "product y" in q_lower or "cyber risk" in q_lower:
                prod_name = "Product Y (Cyber Risk Elite)"
            elif "product z" in q_lower or "term life" in q_lower:
                prod_name = "Product Z (Term Life Pro)"

            steps = [
                f"1. Retrieve {emp_name}'s employee profile, tenure, department, and eligibility attributes from enterprise database",
                f"2. Retrieve {prod_name} specifications, underwriting criteria, and target requirements",
                "3. Retrieve corporate benefits and product eligibility policy guidelines",
                f"4. Cross-evaluate {emp_name}'s tenure and status against product eligibility rules",
                f"5. Identify mandatory onboarding and claim documents required for {prod_name}",
                "6. Verify all eligibility claims against retrieved authoritative citations",
                "7. Synthesize grounded final response with verified status and document checklist"
            ]

            return {
                "plan_id": plan_id,
                "query": query,
                "complexity": "complex_multi_domain",
                "steps": steps,
                "agents_involved": [
                    "Supervisor Agent",
                    "Planner Agent",
                    "Employee Agent",
                    "Product Agent",
                    "Policy Agent",
                    "Retrieval Agent",
                    "Verification Agent",
                    "Response Agent"
                ],
                "rationale": f"Query spans employee record evaluation, product underwriting specs, and policy documentation."
            }

        # Demo 3 pattern: "Create a remote-work request for Rahul"
        elif any(k in q_lower for k in ["create", "submit", "request"]) and "remote" in q_lower:
            emp_name = "Rahul"
            for n in ["Rahul", "Priya", "Amit", "Neha", "Vikram", "Sneha"]:
                if n.lower() in q_lower:
                    emp_name = n
                    break

            steps = [
                f"1. Retrieve {emp_name}'s employment records (tenure, location, performance rating, manager)",
                "2. Retrieve Remote Work Policy (POL-HR-042 Section 1 & Section 2) guidelines",
                f"3. Verify {emp_name}'s eligibility compliance under Section 1 criteria",
                "4. Halt execution for Human Auditor approval (Human-in-the-Loop gate)",
                "5. Upon approval, commit remote work request to enterprise database and audit ledger"
            ]

            return {
                "plan_id": plan_id,
                "query": query,
                "complexity": "action_approval_workflow",
                "steps": steps,
                "agents_involved": [
                    "Supervisor Agent",
                    "Employee Agent",
                    "Policy Agent",
                    "Verification Agent",
                    "Human Approval Agent",
                    "Action Executor"
                ],
                "rationale": "Action requires state mutation and human auditor sign-off."
            }

        # General multi-step query
        else:
            steps = [
                "1. Analyze entity references and query intent across domains",
                "2. Query enterprise ChromaDB vector index with semantic search and keyword boost",
                "3. Enforce document-level permission access control (RBAC)",
                "4. Verify retrieved evidence against candidate factual claims",
                "5. Generate grounded response with authoritative source citations"
            ]

            return {
                "plan_id": plan_id,
                "query": query,
                "complexity": "standard_agentic",
                "steps": steps,
                "agents_involved": [
                    "Supervisor Agent",
                    "Retrieval Agent",
                    "Verification Agent",
                    "Response Agent"
                ],
                "rationale": "Standard enterprise knowledge retrieval and evidence verification."
            }


# Singleton
_planner_agent = None

def get_planner_agent() -> PlannerAgent:
    global _planner_agent
    if _planner_agent is None:
        _planner_agent = PlannerAgent()
    return _planner_agent
