"""
Seeds the database with realistic enterprise data:
- 20+ Employee records (including Rahul Sharma, Priya Patel, Vikram Singh, etc.)
- 10+ Insurance Product records
- 11 Policy records
- 5 Contract records
- Seed Access Requests and Audit Logs
"""

import os
from datetime import datetime
from backend.database.connection import get_db
from backend.database.models import SCHEMA_SQL


def seed_database():
    db = get_db()
    db.init_schema(SCHEMA_SQL)
    print("Database schema initialized.")

    # 1. Seed Employees (20+ records)
    employees = [
        ("EMP-001", "Rahul Sharma", "rahul.sharma@acme.corp", "Engineering", "Senior Software Engineer", "London, UK", "Full-time", "Vikram Singh", "Active", 18, 4.2, 1, "Confidential"),
        ("EMP-002", "Priya Patel", "priya.patel@acme.corp", "Product", "Lead Product Manager", "San Francisco, USA", "Full-time", "Elena Rostova", "Active", 24, 4.5, 1, "Secret"),
        ("EMP-003", "Vikram Singh", "vikram.singh@acme.corp", "Infrastructure", "Principal SRE Architect", "Bangalore, India", "Full-time", "David Chen", "Active", 36, 4.6, 1, "TopSecret"),
        ("EMP-004", "Sneha Rao", "sneha.rao@acme.corp", "Human Resources", "Senior HR Business Partner", "New York, USA", "Full-time", "Sarah Jenkins", "Active", 14, 3.9, 1, "Confidential"),
        ("EMP-005", "Ananya Iyer", "ananya.iyer@acme.corp", "Finance", "Senior Financial Analyst", "Singapore", "Full-time", "Michael Chang", "Active", 8, 3.7, 0, "Confidential"),
        ("EMP-006", "Amit Verma", "amit.verma@acme.corp", "Commercial Sales", "Enterprise Sales Director", "Chicago, USA", "Full-time", "Elena Rostova", "Active", 48, 4.8, 1, "Secret"),
        ("EMP-007", "Neha Gupta", "neha.gupta@acme.corp", "Legal & GRC", "Chief Compliance Counsel", "London, UK", "Full-time", "Sarah Jenkins", "Active", 22, 4.3, 1, "Secret"),
        ("EMP-008", "Rohan Mehta", "rohan.mehta@acme.corp", "Infrastructure", "DevOps Cloud Engineer", "Dublin, Ireland", "Full-time", "Vikram Singh", "Active", 12, 4.0, 1, "Confidential"),
        ("EMP-009", "Pooja Das", "pooja.das@acme.corp", "Underwriting", "Senior Actuarial Specialist", "Mumbai, India", "Full-time", "Michael Chang", "Active", 30, 4.4, 1, "Secret"),
        ("EMP-010", "Suresh Menon", "suresh.menon@acme.corp", "Operations", "Director of Claims Processing", "Toronto, Canada", "Full-time", "David Chen", "Active", 40, 4.5, 1, "Secret"),
        ("EMP-011", "Kavita Reddy", "kavita.reddy@acme.corp", "Customer Experience", "Customer Success Lead", "Sydney, Australia", "Full-time", "Elena Rostova", "Active", 16, 4.1, 1, "Confidential"),
        ("EMP-012", "Arjun Kapoor", "arjun.kapoor@acme.corp", "Cybersecurity", "SOC Lead Threat Analyst", "London, UK", "Full-time", "David Chen", "Active", 20, 4.3, 1, "Secret"),
        ("EMP-013", "Meera Joshi", "meera.joshi@acme.corp", "Data Platform", "Lead Data Engineer", "San Francisco, USA", "Full-time", "Vikram Singh", "Active", 15, 4.2, 1, "Confidential"),
        ("EMP-014", "Deepak Nambiar", "deepak.nambiar@acme.corp", "Commercial Sales", "Account Executive", "Tokyo, Japan", "Full-time", "Amit Verma", "Active", 6, 3.5, 0, "Public"),
        ("EMP-015", "Tanvi Shah", "tanvi.shah@acme.corp", "Product Design", "Senior Staff UX Designer", "Berlin, Germany", "Full-time", "Priya Patel", "Active", 28, 4.7, 1, "Confidential"),
        ("EMP-016", "Manish Pandey", "manish.pandey@acme.corp", "Engineering", "Fullstack Developer", "Bangalore, India", "Contractor", "Rahul Sharma", "Active", 4, 3.2, 0, "Public"),
        ("EMP-017", "Shweta Kulkarni", "shweta.kulkarni@acme.corp", "Legal & GRC", "Paralegal Associate", "New York, USA", "Full-time", "Neha Gupta", "Active", 9, 3.8, 1, "Confidential"),
        ("EMP-018", "Nikhil Saxena", "nikhil.saxena@acme.corp", "Operations", "Disaster Recovery Coordinator", "Austin, USA", "Full-time", "Vikram Singh", "Active", 32, 4.4, 1, "Secret"),
        ("EMP-019", "Ritu Agrawal", "ritu.agrawal@acme.corp", "Human Resources", "Talent Acquisition Lead", "Paris, France", "Full-time", "Sneha Rao", "Active", 19, 4.1, 1, "Confidential"),
        ("EMP-020", "Zainab Al-Mansoor", "zainab.mansoor@acme.corp", "Finance", "Global Payroll Manager", "Dubai, UAE", "Full-time", "Michael Chang", "Active", 26, 4.5, 1, "Secret"),
        ("EMP-021", "Lucas Silva", "lucas.silva@acme.corp", "Engineering", "Security Automation Intern", "Sao Paulo, Brazil", "Intern", "Rahul Sharma", "Active", 2, 3.4, 0, "Public")
    ]

    for emp in employees:
        db.execute_commit("""
            INSERT OR REPLACE INTO employees 
            (employee_id, name, email, department, role, location, employment_type, manager, status, tenure_months, performance_rating, remote_eligible, clear_access_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, emp)

    # 2. Seed Products (10 Insurance Products)
    products = [
        ("PRD-INS-001", "Corporate Health Shield", "Group Health", "Full-time employees aged 18-65 and dependents", "$450/member/year", "Enrollment roster, Government ID, Dependent certificates", "Acme Mutual Life & Health", "Active"),
        ("PRD-INS-002", "Term Life Pro", "Group Life", "Full-time executives earning >$120,000/year", "0.22% of Sum Assured", "Tax returns (W-2), Tele-medical health report, Beneficiary deed", "Acme Mutual Assurance", "Active"),
        ("PRD-INS-003", "Cyber Risk Elite", "Cyber & Specialty", "Enterprises with 100% MFA and active EDR agents", "$12,500/year base", "SOC 2 Type II audit, Cyber Questionnaire, BCP Plan", "Acme Cyber Underwriters Lloyd's", "Active"),
        ("PRD-INS-004", "Keyman Insurance", "Commercial Life", "Active key executives owning <51% equity", "Based on actuarial valuation", "Certified Board Resolution, 3-year Audited Financials, Medical exam", "Acme Corporate Assurance", "Active"),
        ("PRD-INS-005", "Executive Disability Shield", "Disability Income", "Full-time employees working >=32 hours/week", "$85/employee/month", "Attending physician disability statement, 6 months salary slips", "Acme Disability Syndicate", "Active"),
        ("PRD-INS-006", "Commercial Fleet Cover", "Commercial Auto", "Enterprise fleets with minimum 5 telematics-enabled vehicles", "$1,200/vehicle/year", "Vehicle RC, Driver Commercial Licenses, Route risk assessment", "Acme General Insurance", "Active"),
        ("PRD-INS-007", "Group Gratuity Plan", "Pension & Trusts", "Entities with >=20 permanent staff under tax trust", "Variable unit-linked", "Executed Trust Deed, Tax Exemption Certificate, Actuarial valuation", "Acme Institutional Assets", "Active"),
        ("PRD-INS-008", "Directors & Officers (D&O)", "Management Liability", "Corporate Boards with 2+ years trading history", "$18,000/year base", "Signed Proposal Form, Audited Financials, Subsidiary entity list", "Acme Specialty Casualty", "Active"),
        ("PRD-INS-009", "Property & Casualty Umbrella", "Commercial Property", "Facilities equipped with automated NFPA fire sprinklers", "0.15% of Property Value", "Asset Valuation Report, Fire Safety Certificate, P&L records", "Acme Property Assurance", "Active"),
        ("PRD-INS-010", "Global Marine Cargo", "Marine & Trade", "Approved commercial carriers under IACS with Incoterms", "0.35% of Invoice Value", "Commercial Sales Invoice, Ocean Bill of Lading, Survey report", "Acme Maritime Underwriters", "Active")
    ]

    for prd in products:
        db.execute_commit("""
            INSERT OR REPLACE INTO products
            (product_id, product_name, category, eligibility, price, requirements, underwriter, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, prd)

    # 3. Seed Policies
    policies = [
        ("POL-HR-042", "Enterprise Remote Work and Hybrid Operations Policy", "Human Resources", "v3.4", "2026-08-10", "data/policies/remote_work_policy.md"),
        ("POL-BEN-019", "Health Insurance Claim & Cashless Hospitalization Procedure", "Benefits", "v4.1", "2026-07-15", "data/policies/health_insurance_claim_procedure.md"),
        ("POL-FIN-108", "Corporate Travel and Expense Governance Policy", "Finance", "v2.9", "2026-06-20", "data/policies/travel_and_expense_policy.md"),
        ("POL-HR-055", "Parental Leave and Family Support Policy", "Human Resources", "v3.0", "2026-05-12", "data/policies/paternity_and_maternity_leave_policy.md"),
        ("POL-SEC-089", "Global Data Protection and Privacy Policy", "Security & Legal", "v5.0", "2026-09-01", "data/policies/data_privacy_and_gdpr_policy.md"),
        ("POL-ETH-001", "Corporate Code of Conduct and Business Ethics", "Legal & Compliance", "v4.2", "2026-01-15", "data/policies/code_of_conduct_and_ethics.md"),
        ("POL-IT-014", "IT Equipment Allocation and BYOD Policy", "Information Technology", "v3.1", "2026-04-18", "data/policies/equipment_and_byod_policy.md"),
        ("POL-ENG-033", "Engineering On-Call and Incident Standby Policy", "Engineering", "v2.5", "2026-03-30", "data/policies/overtime_and_oncall_policy.md"),
        ("POL-ETH-009", "Whistleblower Protection and Grievance Reporting Policy", "Ethics Committee", "v2.1", "2026-02-14", "data/policies/whistleblower_protection_policy.md"),
        ("POL-SEC-002", "Information Security and Access Control Policy", "Cybersecurity", "v4.8", "2026-08-25", "data/policies/information_security_and_access_policy.md"),
        ("POL-HR-077", "Employee Separation, Offboarding and Severance Policy", "People Operations", "v2.3", "2026-06-05", "data/policies/severance_and_exit_procedure.md"),
        ("POL-IT-028", "Enterprise Backup and Disaster Recovery Policy", "Infrastructure & Security", "v3.2", "2026-08-15", "data/policies/backup_policy.md"),
        ("POL-GRC-062", "Third-Party Vendor Management and Risk Governance Policy", "Procurement & GRC", "v2.7", "2026-07-22", "data/policies/vendor_management_policy.md"),
        ("POL-HR-100", "Acme Enterprise Global Employee Handbook", "Human Resources", "v5.2", "2026-08-01", "data/policies/employee_handbook.md")
    ]

    for pol in policies:
        db.execute_commit("""
            INSERT OR REPLACE INTO policies
            (policy_id, title, department, version, last_updated, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
        """, pol)

    # 4. Seed Contracts
    contracts = [
        ("CNT-VND-2024-001", "Vendor ABC Cloud Solutions Inc", "Cloud Infrastructure Hosting", "2024-01-01", "2027-12-31", "99.95%", "California, USA", "Active"),
        ("CNT-TPA-2025-089", "MediClaim Global TPA Services LLC", "Third-Party Medical Administrator", "2025-04-01", "2028-03-31", "120 min Pre-Auth", "New York, USA", "Active"),
        ("CNT-LOG-2025-014", "Delta Logistics Global LLC", "Commercial Fleet Transport", "2025-02-01", "2027-01-31", "98.5% On-Time", "Illinois, USA", "Active"),
        ("CNT-LEG-2026-003", "Morrison, Sterling & Sterling LLP", "Corporate Legal Retainer", "2026-01-01", "2026-12-31", "60 Partner Hours/mo", "England and Wales", "Active"),
        ("CNT-SEC-2025-044", "Zenith Cyber Defense Systems Inc", "Managed 24/7 Security Operations", "2025-05-01", "2028-04-30", "10 min Incident Response", "Delaware, USA", "Active"),
        ("CNT-EXEC-2026-001", "Chief Executive Officer Employment Agreement", "Executive Compensation & Board", "2026-01-01", "2029-12-31", "N/A", "Delaware, USA", "Active")
    ]

    for cnt in contracts:
        db.execute_commit("""
            INSERT OR REPLACE INTO contracts
            (contract_id, vendor_name, contract_type, effective_date, expiry_date, sla_uptime, governing_law, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, cnt)

    # 5. Seed sample Access Requests
    access_requests = [
        ("REQ-2026-01", "EMP-001", "Rahul Sharma", "Cyber Risk Elite Underwriting Console", "Required for developing automated security telemetry connector", "High", "APPROVED", "Grant Role: CyberRisk_Underwriting_Read", "David Chen", "2026-09-20 10:15:00", "2026-09-20 14:30:00"),
        ("REQ-2026-02", "EMP-004", "Sneha Rao", "Global Payroll Compensation Reports", "Annual salary parity audit across EMEA regions", "Medium", "APPROVED", "Grant Read Access: Payroll_EMEA", "Michael Chang", "2026-09-18 09:00:00", "2026-09-18 11:45:00")
    ]

    for req in access_requests:
        db.execute_commit("""
            INSERT OR REPLACE INTO access_requests
            (request_id, employee_id, employee_name, product_or_system, reason, risk_level, status, requested_operation, approved_by, request_timestamp, approval_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, req)

    # 6. Seed sample Audit Logs
    audit_logs = [
        ("LOG-001", "QRY-101", "2026-09-22 18:20:00", "EMP-001", "QUERY_EVALUATION", "Supervisor Agent", "Processed query: 'Remote work eligibility for Rahul'", "SUCCESS", 420),
        ("LOG-002", "QRY-102", "2026-09-22 18:21:00", "EMP-001", "EVIDENCE_VERIFICATION", "Evidence Verification Agent", "Verified 3 claims against POL-HR-042 and employees table", "SUCCESS", 185)
    ]

    for log in audit_logs:
        db.execute_commit("""
            INSERT OR REPLACE INTO audit_logs
            (log_id, query_id, timestamp, user_id, action_type, agent_name, details, status, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, log)

    print("Successfully seeded all 21 employees, 10 products, 11 policies, 5 contracts, access requests, and audit logs!")


if __name__ == "__main__":
    seed_database()
