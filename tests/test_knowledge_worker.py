"""
End-to-End Automated Test Suite for Enterprise Expert Knowledge Worker.
Validates Demo 1, Demo 2, Demo 3, Demo 4, and Demo 5 (RBAC),
Conversational Memory, Reranking, Human Approval, and Evaluation Benchmark.
"""

import unittest
import sys
import os

# Ensure project root in python path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph.workflow import get_workflow
from backend.rag.retriever import get_retriever
from backend.tools.permission_tool import get_permission_tool
from backend.tools.approval_tool import get_approval_tool
from backend.evaluation.benchmark import get_evaluator
from backend.database.repositories import AccessRequestRepository


class TestEnterpriseKnowledgeWorker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = get_workflow()
        cls.retriever = get_retriever()
        cls.permission_tool = get_permission_tool()
        cls.approval_tool = get_approval_tool()
        cls.evaluator = get_evaluator()
        cls.access_repo = AccessRequestRepository()

    def test_demo_1_remote_work_policy(self):
        """Demo 1: What is our remote work policy?"""
        query = "What is our remote work policy?"
        res = self.workflow.run(query, user_role="employee")

        self.assertFalse(res.get("is_permission_denied"))
        self.assertEqual(res.get("evidence_status"), "Verified")
        self.assertGreater(len(res.get("citations", [])), 0)

        # Check execution trace
        agents_run = [ev["agent"] for ev in res["execution_trace"]]
        self.assertIn("Supervisor Agent", agents_run)
        self.assertIn("Policy Agent", agents_run)
        self.assertIn("Retrieval Agent", agents_run)
        self.assertIn("Verification Agent", agents_run)
        self.assertIn("Response Agent", agents_run)

        # Content check
        resp = res.get("final_response", "")
        self.assertIn("POL-HR-042", resp)
        self.assertIn("Eligibility Criteria", resp)

    def test_general_guidance_for_uncovered_leave_question(self):
        """A leave timing question without direct policy coverage should state that it is general guidance and requires human review."""
        query = "okay tell me the best time to take leave to the company"
        res = self.workflow.run(query, user_role="employee")

        resp = res.get("final_response", "")
        self.assertIn("not explicitly mentioned in the policy documents", resp.lower())
        self.assertIn("general guidance", resp.lower())
        self.assertIn("human-in-the-loop", resp.lower())

    def test_vague_unrelated_query_does_not_get_policy_answer(self):
        """Malformed or vague queries must not be mistaken for policy-grounded evidence."""
        query = "can you tell me the how best employee is choose"
        res = self.workflow.run(query, user_role="employee")

        resp = res.get("final_response", "")
        self.assertIn("not explicitly mentioned in the policy documents", resp.lower())
        self.assertIn("human-in-the-loop", resp.lower())
        self.assertIn("general guidance", resp.lower())
        self.assertNotIn("according to the policy", resp.lower())

    def test_yes_continue_general_guidance_uses_tavily_when_available(self):
        """Explicit approval should trigger the Tavily general-guidance path instead of repeating the same policy fallback."""
        query = "Yes, continue with general guidance"
        original_enabled = self.workflow.tavily_tool.enabled
        original_search = self.workflow.tavily_tool.search
        self.workflow.tavily_tool.enabled = True
        self.workflow.tavily_tool.search = lambda q, max_results=2: {
            "enabled": True,
            "answer": "General web guidance: confirm with the relevant policy owner before acting.",
            "results": [],
            "message": "Web search completed."
        }
        try:
            res = self.workflow.run(query, user_role="employee")
            resp = res.get("final_response", "")
            self.assertIn("Web Context", resp)
            self.assertIn("General web guidance", resp)
            self.assertIn("not found in the official policy documents", resp.lower())
        finally:
            self.workflow.tavily_tool.enabled = original_enabled
            self.workflow.tavily_tool.search = original_search

    def test_performance_evaluation_question_uses_correct_policy_scope(self):
        """Performance evaluation questions must stay anchored to the employee handbook and not mix in remote work or bonus policy language."""
        query = "Is there a company policy for employee performance evaluation?"
        res = self.workflow.run(query, user_role="employee")

        resp = res.get("final_response", "")
        self.assertIn("Performance Management and Career Development", resp)
        self.assertIn("Employee Handbook", resp)
        self.assertNotIn("Remote Work Policy", resp)

    def test_demo_2_multi_domain_purchase_eligibility(self):
        """Demo 2: Can Rahul purchase Product X and what documents are required?"""
        query = "Can Rahul purchase Product X and what documents are required?"
        res = self.workflow.run(query, user_role="employee")

        self.assertFalse(res.get("is_permission_denied"))
        self.assertIsNotNone(res.get("plan"))
        self.assertEqual(len(res["plan"]["steps"]), 7)

        # Check agents
        agents_run = [ev["agent"] for ev in res["execution_trace"]]
        self.assertIn("Supervisor Agent", agents_run)
        self.assertIn("Planner Agent", agents_run)
        self.assertIn("Employee Agent", agents_run)
        self.assertIn("Product Agent", agents_run)
        self.assertIn("Policy Agent", agents_run)
        self.assertIn("Retrieval Agent", agents_run)
        self.assertIn("Verification Agent", agents_run)
        self.assertIn("Response Agent", agents_run)

        # Content check
        resp = res.get("final_response", "")
        self.assertIn("Rahul Sharma", resp)
        self.assertIn("Eligible", resp)
        self.assertIn("Mandatory Documents Required", resp)

    def test_demo_3_human_approval_remote_work_request(self):
        """Demo 3: Create a remote-work request for Rahul."""
        query = "Create a remote-work request for Rahul."
        res = self.workflow.run(query, user_role="employee")

        self.assertTrue(res.get("is_action_request"))
        self.assertIsNotNone(res.get("action_approval"))
        app = res["action_approval"]
        req_id = app["request_id"]
        self.assertEqual(app["status"], "PENDING")
        self.assertEqual(app["employee_name"], "Rahul Sharma")

        # Simulate Human Auditor approval
        decision_res = self.approval_tool.process_decision(
            request_id=req_id,
            decision="approve",
            approver_name="Human Auditor Test"
        )
        self.assertTrue(decision_res["success"])
        self.assertEqual(decision_res["status"], "APPROVED")

        # Verify database record is actually updated
        updated_db_req = self.access_repo.get_by_id(req_id)
        self.assertIsNotNone(updated_db_req)
        self.assertEqual(updated_db_req["status"], "APPROVED")
        self.assertEqual(updated_db_req["approved_by"], "Human Auditor Test")

    def test_demo_4_contract_vendor_abc_restrictions(self):
        """Demo 4: Show me the restrictions in the Vendor ABC contract."""
        query = "Show me the restrictions in the Vendor ABC contract."
        res = self.workflow.run(query, user_role="employee")

        self.assertFalse(res.get("is_permission_denied"))
        agents_run = [ev["agent"] for ev in res["execution_trace"]]
        self.assertIn("Supervisor Agent", agents_run)
        self.assertIn("Contract Agent", agents_run)
        self.assertIn("Retrieval Agent", agents_run)
        self.assertIn("Response Agent", agents_run)

        resp = res.get("final_response", "")
        self.assertIn("Vendor ABC", resp)
        self.assertIn("Data Sovereignty", resp)
        self.assertIn("Subcontractor", resp)

    def test_demo_5_permission_access_control(self):
        """Demo 5: RBAC test on CEO Compensation Contract."""
        query = "Show me the CEO compensation contract."

        # 1. As regular employee: MUST be blocked, 0 chunks to LLM
        res_emp = self.workflow.run(query, user_role="employee")
        self.assertTrue(res_emp.get("is_permission_denied"))
        self.assertEqual(len(res_emp.get("retrieved_chunks", [])), 0)
        self.assertIn("Access Denied", res_emp.get("final_response", ""))

        # 2. As admin: Allowed
        res_admin = self.workflow.run(query, user_role="admin")
        self.assertFalse(res_admin.get("is_permission_denied"))
        self.assertGreater(len(res_admin.get("retrieved_chunks", [])), 0)

    def test_conversational_memory(self):
        """Test entity resolution across multiple conversational turns."""
        turn1 = "What is Product X?"
        res1 = self.workflow.run(turn1, user_role="employee")

        history = [
            {"role": "user", "content": turn1},
            {"role": "assistant", "content": res1["final_response"]}
        ]

        turn2 = "What documents are required for it?"
        res2 = self.workflow.run(turn2, user_role="employee", conversation_history=history)

        self.assertIn("Corporate Health Shield", res2["resolved_query"])
        self.assertIsNotNone(res2.get("product_data"))
        self.assertEqual(res2["product_data"]["product_name"], "Corporate Health Shield")

    def test_evaluation_benchmark(self):
        """Test evaluation benchmark suite."""
        bench = self.evaluator.run_benchmark()
        self.assertEqual(bench["total_test_cases"], 8)
        self.assertGreaterEqual(bench["metrics"]["mrr"], 0.70)
        self.assertGreaterEqual(bench["metrics"]["retrieval_accuracy"], 0.70)
        self.assertEqual(bench["metrics"]["citation_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
