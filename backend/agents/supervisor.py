"""
Supervisor Agent.
Central routing and orchestration coordinator for the Enterprise Expert Knowledge Worker.
Determines:
- Simple vs Complex queries
- Whether explicit multi-step planning is required
- Whether RAG is required
- Which specialized domain agents are dispatched
- Whether factual evidence verification is needed
- Whether Human-in-the-Loop approval is required
- Resolves entity references across conversational turns
"""

import uuid
import re
from typing import Dict, Any, List, Optional


# Topics covered by the corporate policy library. Used so that a policy question is routed to the
# Vizier even when the person does not literally type the word "policy".
POLICY_TOPIC_KEYWORDS = [
    "policy", "policies", "procedure", "handbook", "leave", "vacation", "holiday", "sick", "travel", "expense", "per diem",
    "allowance", "byod", "remote work", "remote-work", "hybrid", "whistleblower", "backup", "overtime", "on-call", "oncall",
    # HR & people
    "harassment", "posh", "discrimination", "diversity", "equal opportunity", "recruit", "hiring", "background check",
    "background verification", "salary band", "bonus", "compensation", "disciplin", "sabbatical", "notice period",
    "resignation", "probation", "onboarding", "referral", "relocation", "dress code", "grievance", "wellbeing",
    "mental health", "eap", "accommodation", "stock option", "rsu", "esop", "equity plan", "provident", "retirement",
    "401k", "promotion", "internal transfer", "volunteer", "attendance", "working hours", "tuition", "personnel record",
    # Ethics, legal & compliance
    "bribery", "corruption", "gift", "hospitality", "conflict of interest", "insider trading", "securities dealing",
    "political contribution", "lobbying", "modern slavery", "human rights", "money laundering", "aml", "kyc",
    "sanction", "export control", "antitrust", "competition law", "intellectual property", "patent", "open source",
    "records retention", "legal hold", "fraud", "supplier code", "procurement", "purchase order", "media relations",
    "social media", "delegation of authority", "approval matrix", "signing authority", "approval limit", "spending limit", "spending approval",
    # IT & security
    "acceptable use", "password", "mfa", "multi-factor", "incident response", "security incident", "data breach",
    "breach notification", "data classification", "encryption", "patch", "vulnerabilit", "change management",
    "business continuity", "disaster recovery", "cloud security", "visitor", "badge", "generative ai", "ai usage",
    "chatgpt", "secure development", "sdlc", "logging", "monitoring policy",
    # Finance, safety, ESG, customer
    "credit card", "sox", "financial reporting", "payroll", "tax withholding", "capex", "capital expenditure",
    "safety", "drug", "alcohol", "workplace violence", "evacuation", "duty of care", "esg", "sustainability",
    "net-zero", "complaint", "claims handling", "fair treatment", "underwriting authority", "risk acceptance",
]


class SupervisorAgent:
    def __init__(self):
        self.name = "Supervisor Agent"
        self.purpose = "Central intelligent router evaluating complexity, entity references, domain dispatch, and safety gates."

    def analyze_and_route(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_role: str = "employee"
    ) -> Dict[str, Any]:
        """
        Analyze incoming query, resolve entity references from conversational memory,
        and determine optimal agent routing topology.
        """
        # 1. Resolve Coreferences from Memory
        resolved_query = query
        last_entity = ""

        if conversation_history:
            for turn in reversed(conversation_history):
                content = turn.get("content", "")
                # Match product references
                prod_match = re.search(
                    r'\b(Corporate Health Shield|Term Life Pro|Cyber Risk Elite|Keyman Insurance|Executive Disability Shield|Commercial Fleet Cover|Group Gratuity Plan|Directors & Officers|Property & Casualty|Global Marine Cargo|Product X|Product Y|Product Z)\b',
                    content, re.IGNORECASE
                )
                if prod_match:
                    last_entity = prod_match.group(1)
                    break
                # Match employee references
                emp_match = re.search(
                    r'\b(Rahul|Priya|Vikram|Sneha|Ananya|Amit|Neha|Rohan|Pooja|Suresh)\b',
                    content, re.IGNORECASE
                )
                if emp_match:
                    last_entity = emp_match.group(1)
                    break

        # Check for pronouns: "it", "this", "that", or implicit context e.g. "what documents are required?"
        q_lower = query.lower()
        if last_entity:
            if any(p in f" {q_lower} " for p in [" it ", " this ", " that ", " for it", " for this"]):
                resolved_query = re.sub(r'\b(it|this|that)\b', last_entity, query, flags=re.IGNORECASE)
            elif "what documents are required" in q_lower and "for" not in q_lower:
                resolved_query = f"{query} for {last_entity}"

        q_clean = resolved_query.lower()

        # 2. Domain & Intent Classification
        is_action_request = any(k in q_clean for k in ["create", "submit", "request a", "generate"]) and \
                            any(k in q_clean for k in ["remote work", "remote-work", "hybrid request", "access request"])
        
        is_policy_topic = any(k in q_clean for k in POLICY_TOPIC_KEYWORDS)

        performance_keywords = [
            "performance evaluation", "employee performance", "performance rating", "performance management",
            "calibration cycle", "review cycle", "performance review", "performance appraisal", "rating 3.0",
            "above 3.0", "below 3.0", "pip", "performance improvement plan"
        ]
        is_performance_policy = any(k in q_clean for k in performance_keywords)

        # Named colleagues always mean an employee lookup; generic words such as "employee" or "manager"
        # only do so when the question is not clearly about a policy topic ("employee referral bonus").
        named_employee = any(k in q_clean for k in ["rahul", "priya", "amit", "neha", "vikram", "sneha"])
        generic_employee = any(k in q_clean for k in ["employee", "tenure", "rating", "manager", "who is", "performance"])
        is_employee_domain = named_employee or (generic_employee and not is_policy_topic)

        if is_performance_policy:
            is_policy_domain = True
            is_employee_domain = False
            is_product_domain = False
            is_contract_domain = False

        explicit_product = any(k in q_clean for k in [
            "product", "health shield", "term life", "cyber risk", "premium", "underwriter", "documents are required",
            "keyman", "gratuity plan", "fleet cover", "disability shield", "marine cargo", "umbrella"
        ])
        is_product_domain = explicit_product or (
            any(k in q_clean for k in ["insurance", "coverage", "purchase"]) and not is_policy_topic
        )

        is_policy_domain = is_policy_topic or is_performance_policy

        is_contract_domain = any(k in q_clean for k in ["contract", "vendor", "sla", "agreement", "hosting", "vendor abc", "vendor xyz", "obligations", "restrictions", "sovereignty", "ceo compensation", "ceo contract"])
        # A named policy topic (e.g. "vendor management policy") is answered by the Policy Agent, not the Contract Agent
        if is_policy_topic and not any(k in q_clean for k in ["contract", "sla", "agreement", "vendor abc", "vendor xyz", "ceo"]):
            is_contract_domain = False

        is_restricted_query = any(k in q_clean for k in ["ceo compensation", "ceo contract", "executive salary", "executive agreement", "golden parachute"])

        # Determine complexity & planner requirement
        # Complex multi-domain queries require Planner Agent (e.g. "Can Rahul purchase Product X and what documents are required?")
        active_domains_count = sum([is_employee_domain, is_product_domain, is_policy_domain, is_contract_domain])
        requires_planner = active_domains_count >= 2 or ("can " in q_clean and "purchase" in q_clean) or is_action_request

        # Determine agent dispatch list
        agents_to_dispatch = []

        if requires_planner:
            agents_to_dispatch.append("Planner Agent")

        if is_action_request:
            # Workflow: Employee Agent -> Policy Agent -> Verification Agent -> Human Approval -> Action Executor
            agents_to_dispatch.extend([
                "Employee Agent",
                "Policy Agent",
                "Verification Agent",
                "Human Approval Agent"
            ])
            requires_rag = True
            requires_verification = True
            requires_approval = True
        elif is_employee_domain and is_product_domain:
            # Demo 2: Planner -> Employee Agent -> Product Agent -> Policy Agent -> Retrieval Agent -> Verification Agent -> Response Agent
            agents_to_dispatch.extend([
                "Employee Agent",
                "Product Agent",
                "Policy Agent",
                "Retrieval Agent",
                "Verification Agent",
                "Response Agent"
            ])
            requires_rag = True
            requires_verification = True
            requires_approval = False
        elif is_policy_domain and not is_employee_domain and not is_product_domain:
            # Demo 1: Policy Agent -> Retrieval Agent -> Verification Agent -> Response Agent
            agents_to_dispatch.extend([
                "Policy Agent",
                "Retrieval Agent",
                "Verification Agent",
                "Response Agent"
            ])
            requires_rag = True
            requires_verification = True
            requires_approval = False
        elif is_contract_domain:
            # Demo 4: Contract Agent -> Retrieval Agent -> Verification Agent -> Response Agent
            agents_to_dispatch.extend([
                "Contract Agent",
                "Retrieval Agent",
                "Verification Agent",
                "Response Agent"
            ])
            requires_rag = True
            requires_verification = True
            requires_approval = False
        elif is_product_domain and not is_employee_domain:
            # "What is Product X?" -> Product Agent -> Response Agent
            agents_to_dispatch.extend([
                "Product Agent",
                "Response Agent"
            ])
            requires_rag = True
            requires_verification = False
            requires_approval = False
        else:
            # General enterprise knowledge
            agents_to_dispatch.extend([
                "Retrieval Agent",
                "Verification Agent",
                "Response Agent"
            ])
            requires_rag = True
            requires_verification = True
            requires_approval = False

        return {
            "query_id": f"QRY-{uuid.uuid4().hex[:6].upper()}",
            "original_query": query,
            "resolved_query": resolved_query,
            "requires_planner": requires_planner,
            "requires_rag": requires_rag,
            "requires_verification": requires_verification,
            "requires_approval": requires_approval,
            "is_action_request": is_action_request,
            "is_restricted_query": is_restricted_query,
            "domains": {
                "employee": is_employee_domain,
                "product": is_product_domain,
                "policy": is_policy_domain,
                "contract": is_contract_domain
            },
            "agents_to_dispatch": agents_to_dispatch,
            "classification": (
                "Sensitive Action Workflow" if is_action_request else
                "Complex Multi-Domain Query" if requires_planner else
                "Standard Domain Query"
            )
        }


# Singleton
_supervisor_agent = None

def get_supervisor_agent() -> SupervisorAgent:
    global _supervisor_agent
    if _supervisor_agent is None:
        _supervisor_agent = SupervisorAgent()
    return _supervisor_agent
