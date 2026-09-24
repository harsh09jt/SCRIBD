"""
Generates realistic enterprise policy, product, and contract documents for the Enterprise Expert Knowledge Worker.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POL_DIR = os.path.join(BASE_DIR, "policies")
PROD_DIR = os.path.join(BASE_DIR, "products")
CONT_DIR = os.path.join(BASE_DIR, "contracts")

POLICIES = {
    "remote_work_policy.md": """# Enterprise Remote Work and Hybrid Operations Policy
Document ID: POL-HR-042
Version: 3.4
Last Updated: 2026-08-10
Department: Human Resources & Operations
Owner: Chief People Officer

## 1. Eligibility Criteria
Full-time employees with at least 3 months of tenure in good performance standing (Performance Rating 3.0 or higher) are eligible to request hybrid or full remote work arrangements.
Contractors and interns require individual VP-level approval.
Employees located within 30km of an enterprise campus are expected to work in-office at least 2 days per week (Hybrid 3/2 Model).

## 2. Remote Work Authorization Workflow
1. Employee submits remote work request via the internal portal.
2. Direct Manager reviews operational coverage and approves/rejects within 5 business days.
3. HR Operations logs the approved work location for regional payroll compliance.
4. For consecutive remote work exceeding 30 days outside the designated base country, cross-border tax authorization from the Legal & Finance council is mandatory.

## 3. Technology & Workspace Allowance
Eligible remote employees receive a one-time home office setup stipend of $1,000 USD and a recurring monthly high-speed internet reimbursement of $75 USD.
All computing devices must run corporate Mobile Device Management (MDM) with disk-level AES-256 BitLocker/FileVault encryption.
Connecting via public unencrypted Wi-Fi networks without activating the corporate VPN is strictly prohibited.
""",

    "health_insurance_claim_procedure.md": """# Health Insurance Claim & Cashless Hospitalization Procedure
Document ID: POL-BEN-019
Version: 4.1
Last Updated: 2026-07-15
Department: Employee Benefits & HR
Owner: Total Rewards Director

## 1. Cashless Hospitalization Protocol
For planned hospitalizations, the employee or dependent must notify the Third-Party Administrator (TPA - MediClaim Global) at least 48 hours in advance.
For emergency admissions, notification must be submitted within 24 hours of hospital intake.
Cashless pre-authorization requires:
- Corporate Health Card ID
- Government photo identification (Aadhaar / Passport / Driver License)
- Treating physician's preliminary diagnosis and estimated cost breakdown form.

## 2. Reimbursement Claims Workflow
If treatment occurs at a non-network hospital, reimbursement claims must be filed within 30 calendar days of patient discharge.
Mandatory documentation for reimbursement:
1. Original signed claim form part A and B.
2. Original itemized hospital bills and numbered payment receipts.
3. Comprehensive discharge summary with clinical history.
4. Pharmacy prescriptions matched with diagnostic test reports.
5. Canceled bank check with employee name printed for direct NEFT/Wire transfer.

## 3. Exclusions and Waiting Periods
Pre-existing conditions are covered from Day 1 for all full-time employees and registered dependents.
Cosmetic surgeries, non-allopathic alternative therapies without prior authorization, and unprescribed vitamins are non-payable.
Maternity expenses are covered up to $5,000 USD per delivery for up to two children.
""",

    "travel_and_expense_policy.md": """# Corporate Travel and Expense Governance Policy
Document ID: POL-FIN-108
Version: 2.9
Last Updated: 2026-06-20
Department: Global Finance & Procurement
Owner: Corporate Controller

## 1. Travel Class Guidelines
- Domestic flights under 4 hours: Economy Class only.
- International flights between 4 and 8 hours: Premium Economy.
- Intercontinental flights exceeding 8 continuous hours: Business Class permitted for Director level and above, or with explicit VP approval.
- Hotel accommodation limit: Up to $250/night in Tier 1 global cities (New York, London, Tokyo, Singapore), $175/night in Tier 2 cities.

## 2. Daily Per Diem Allowances
Daily meal and incidental expenses (M&IE):
- United States & Western Europe: $85 USD per day.
- Asia Pacific & Latin America: $60 USD per day.
Alcoholic beverages are not reimbursable unless directly associated with an approved client entertainment dinner with prior manager sign-off.

## 3. Expense Filing and Audit Thresholds
All expense reports must be submitted within 21 calendar days of trip conclusion via the Concur portal.
Receipts are strictly mandatory for any individual expense item exceeding $25 USD.
Expense reports exceeding $2,500 require dual approval from the Department Head and Finance Controller.
""",

    "paternity_and_maternity_leave_policy.md": """# Parental Leave and Family Support Policy
Document ID: POL-HR-055
Version: 3.0
Last Updated: 2026-05-12
Department: Human Resources
Owner: Head of Diversity & Inclusion

## 1. Maternity Leave Entitlements
Birthing mothers are entitled to 26 weeks of fully paid maternity leave.
Leave may commence up to 8 weeks prior to the expected delivery date.
An additional 4 weeks of medical leave can be requested in cases of post-natal complications with medical practitioner certification.

## 2. Paternity and Secondary Caregiver Leave
Non-birthing parents and secondary caregivers are entitled to 6 weeks of fully paid parental leave.
This leave can be taken consecutively or divided into two tranches within the first 12 months following birth or legal adoption.

## 3. Gradual Return to Work
Returning parents have the option to transition back on an 80% work schedule (4 days per week) at 100% pay for the initial 4 weeks following return.
On-site lactation rooms and child-care concierge support are accessible across all regional enterprise offices.
""",

    "data_privacy_and_gdpr_policy.md": """# Global Data Protection and Privacy Policy
Document ID: POL-SEC-089
Version: 5.0
Last Updated: 2026-09-01
Department: Information Security & Legal
Owner: Data Protection Officer (DPO)

## 1. Scope & Regulatory Frameworks
This policy governs the processing of Personally Identifiable Information (PII) under GDPR (EU 2016/679), CCPA/CPRA, and the Digital Personal Data Protection Act.
All customer, employee, and partner data must be processed lawfully, transparently, and strictly for specified contractual purposes.

## 2. Incident Response and Breach Notification
Any suspected data breach or unauthorized disclosure of PII must be escalated to the Incident Response Team (`security@acme.corp`) within 60 minutes of detection.
In accordance with GDPR Article 33, supervisory authorities and impacted data subjects must be formally notified within 72 hours where there is a high risk to rights and freedoms.

## 3. Data Subject Rights (DSR) Protocols
Requests for data access, rectification, portability, or erasure (Right to be Forgotten) must be validated and resolved within 30 calendar days.
Customer PII stored in production databases must be encrypted with AES-256 at rest and masked in all non-production environments.
""",

    "code_of_conduct_and_ethics.md": """# Corporate Code of Conduct and Business Ethics
Document ID: POL-ETH-001
Version: 4.2
Last Updated: 2026-01-15
Department: Legal & Compliance
Owner: Chief Legal Officer

## 1. Anti-Bribery and Corruption
Acme Enterprise enforces a zero-tolerance policy against bribery, kickbacks, or corrupt payments under the US Foreign Corrupt Practices Act (FCPA) and UK Bribery Act.
Employees may never offer or accept gifts, meals, or hospitality exceeding $100 USD in cumulative value from any single vendor or client per annum without written compliance disclosure.

## 2. Conflicts of Interest
Employees must disclose any external commercial engagements, secondary board directorships, or personal relationships with competing firms or suppliers.
Disclosures must be logged in the Compliance Portal within 14 days of change in circumstance.

## 3. Equal Opportunity and Harassment-Free Workplace
Acme is committed to equal employment opportunities regardless of race, gender, sexual orientation, disability, or veteran status.
Bullying, sexual harassment, or discriminatory behavior results in immediate disciplinary review up to and including termination of employment.
""",

    "equipment_and_byod_policy.md": """# IT Equipment Allocation and BYOD Policy
Document ID: POL-IT-014
Version: 3.1
Last Updated: 2026-04-18
Department: Information Technology
Owner: VP of Enterprise Infrastructure

## 1. Hardware Provisioning Standards
Standard engineering allocations include an Apple MacBook Pro 16-inch (M-Series Silicon, 32GB RAM) or Dell XPS 15 workstation.
Standard business allocations receive an Apple MacBook Air 15-inch or Lenovo ThinkPad Carbon X1.
Hardware refresh cycles occur every 36 months from initial date of deployment.

## 2. Bring Your Own Device (BYOD) Guidelines
Personal mobile devices used for corporate email (Microsoft Outlook), Slack, or 2FA authentication must install the corporate MDM profile.
The MDM profile strictly enforces 6-digit PIN passcodes, biometric unlocking, and remote wipe capabilities restricted strictly to corporate application containers.

## 3. Lost or Stolen Equipment
In the event of lost or stolen corporate hardware, the employee must contact IT Security Helpdesk within 2 hours to execute immediate remote device locking and cryptographic wipe.
""",

    "overtime_and_oncall_policy.md": """# Engineering On-Call and Incident Standby Policy
Document ID: POL-ENG-033
Version: 2.5
Last Updated: 2026-03-30
Department: Site Reliability Engineering & Platform
Owner: VP of Infrastructure

## 1. On-Call Rotations & Standby Allowances
Engineers participating in primary 24/7 Tier-1/Tier-2 production pager duty rotations receive an on-call standby stipend of $650 USD per 7-day rotation.
Secondary on-call engineers receive $350 USD per rotation.
Engineers engaged in Sev-1 or Sev-2 incident resolution during non-standard hours (22:00 to 06:00 local time) are entitled to 1.5x compensatory rest hours.

## 2. Incident SLA Response Times
Primary on-call engineers must acknowledge critical PagerDuty alerts within 10 minutes.
Initial incident triage and bridge creation must occur within 20 minutes for Sev-1 outages impacting core payment or customer-facing services.
""",

    "whistleblower_protection_policy.md": """# Whistleblower Protection and Grievance Reporting Policy
Document ID: POL-ETH-009
Version: 2.1
Last Updated: 2026-02-14
Department: Audit & Ethics Committee
Owner: Independent Board Ombudsman

## 1. Reporting Channels
Employees, contractors, and third parties can report financial irregularities, safety violations, harassment, or legal breaches anonymously via:
- Dedicated toll-free ethics hotline: 1-800-555-ETHX (available 24/7)
- Secure encrypted web portal: `https://ethics.internal.acme.corp`
- Direct sealed transmission to the Independent Ombudsman.

## 2. Non-Retaliation Guarantee
The company strictly prohibits any form of retaliation, demotion, termination, or harassment against any individual who files a good-faith whistleblower report.
Any manager or executive found engaging in retaliatory behavior is subject to immediate summary dismissal.
""",

    "information_security_and_access_policy.md": """# Information Security and Access Control Policy
Document ID: POL-SEC-002
Version: 4.8
Last Updated: 2026-08-25
Department: Cybersecurity & GRC
Owner: Chief Information Security Officer (CISO)

## 1. Principle of Least Privilege
Access to enterprise systems, cloud platforms (AWS, Azure), source code repositories, and production databases is granted strictly on a need-to-know basis.
Default access for all new accounts is zero privilege.
Privileged access roles (Cloud Admin, Database Superuser, Production SRE) require dual-custody approval from the employee's manager and the Security Operations Lead.

## 2. Password and Authentication Governance
- Minimum password length: 14 alphanumeric characters with mixed casing and symbols.
- Passwords must be rotated every 90 days for privileged administrative accounts.
- Multi-Factor Authentication (MFA) via FIDO2 hardware security keys or authenticator TOTP is mandatory for all internal and VPN access.
- Inactive user accounts exceeding 30 consecutive days are automatically suspended.

## 3. Quarterly Access Reviews
Department managers must conduct and sign off on quarterly access reviews verifying that all active permissions align with current employee job functions.
Delinquent reviews exceeding 14 days trigger automatic privilege revocation for affected groups.
""",

    "severance_and_exit_procedure.md": """# Employee Separation, Offboarding and Severance Policy
Document ID: POL-HR-077
Version: 2.3
Last Updated: 2026-06-05
Department: People Operations
Owner: VP of People Operations

## 1. Notice Periods
- Individual contributors: 30 calendar days written notice.
- Managers and Senior Staff Engineers: 60 calendar days.
- Directors, Vice Presidents, and C-Suite Executives: 90 calendar days.
The company reserves the right to initiate Garden Leave with full salary and benefit continuation in lieu of notice.

## 2. Offboarding and Digital Deprovisioning
Access to corporate email, Slack, GitHub, AWS consoles, and VPN tunnels is terminated at 17:00 local time on the employee's final working day.
All physical assets (laptops, monitors, security badges) must be returned to IT asset management within 7 business days of departure.
Full and final financial settlements including accrued leave encashment are disbursed within 30 days of clearance.
""",

    "backup_policy.md": """# Enterprise Backup and Disaster Recovery Policy
Document ID: POL-IT-028
Version: 3.2
Last Updated: 2026-08-15
Department: Infrastructure & Information Security
Owner: Chief Information Security Officer (CISO)
Access Roles: employee, manager, hr, legal, admin

## 1. Backup Frequencies and Retention Schedules
- Tier-1 Production Databases: Incremental backups every 15 minutes, full automated daily snapshots with 35-day point-in-time recovery (PITR).
- Tier-2 Application Servers: Daily differential backups retained for 90 days.
- Long-Term Regulatory Archives: Monthly immutable GFS (Grandfather-Father-Son) snapshots retained for 7 years to satisfy SOX and SEC regulatory retention.

## 2. Air-Gapped and Immutable Storage (WORM)
All secondary production backup volumes must be replicated to an isolated, air-gapped AWS S3 Glacier Vault configured with Object Lock in Compliance Mode (Write Once, Read Many).
No single root account or identity shall possess credentials capable of modifying or destroying immutable vault backups prior to policy expiration.

## 3. Disaster Recovery Testing and RTO/RPO Metrics
- Recovery Point Objective (RPO): Maximum 15 minutes for transactional customer records.
- Recovery Time Objective (RTO): Maximum 2 hours for primary workload failover to secondary cloud region.
- Mandatory bi-annual Disaster Recovery simulation game days must be executed by Infrastructure and SRE teams with full audit sign-off.
""",

    "vendor_management_policy.md": """# Third-Party Vendor Management and Risk Governance Policy
Document ID: POL-GRC-062
Version: 2.7
Last Updated: 2026-07-22
Department: Global Procurement & Information Security
Owner: Head of Vendor Risk Management
Access Roles: employee, manager, hr, legal, admin

## 1. Vendor Tiering and Due Diligence
All enterprise third-party suppliers, SaaS vendors, and cloud hosting providers are categorized into three risk tiers:
- Tier-1 (Critical): Providers processing customer PII, hosting core infrastructure, or having persistent API integration. Requires annual SOC 2 Type II audit, SIG questionnaire, and CISO sign-off.
- Tier-2 (Operational): Commercial vendors with business confidential data access. Requires bi-annual security review.
- Tier-3 (Low): Generic commodity suppliers with zero network or data access.

## 2. Mandatory Contractual Safeguards
Every Tier-1 and Tier-2 vendor contract must incorporate:
1. Standard Contractual Clauses (SCCs) for cross-border data transfers.
2. 24-hour mandatory security breach notification SLA.
3. Right-to-audit clauses granting Acme Enterprise independent audit rights.
4. Business continuity and escrow commitments for proprietary source code.

## 3. Offboarding and Vendor Deprovisioning
Upon contract termination, vendors must provide a written Certificate of Data Destruction within 30 calendar days confirming all Acme data has been cryptographically sanitized in compliance with NIST SP 800-88 standards.
""",

    "employee_handbook.md": """# Acme Enterprise Global Employee Handbook
Document ID: POL-HR-100
Version: 5.2
Last Updated: 2026-08-01
Department: Human Resources & People Operations
Owner: Chief People Officer
Access Roles: employee, manager, hr, legal, admin

## 1. Welcome to Acme Enterprise
Welcome to Acme Enterprise. Our mission is to accelerate intelligent, trustworthy infrastructure for global commerce.
This handbook summarizes key organizational principles, employee rights, operational expectations, and cultural commitments.

## 2. Working Hours, Flexibility and Core Collaboration
Core collaboration hours across all regional business offices are 10:00 to 16:00 local time.
Employees are empowered to arrange flexible daily hours in coordination with their direct functional manager, provided team commitments, customer support SLAs, and on-call rotations are strictly met.

## 3. Performance Management and Career Development
Acme operates on a continuous feedback framework with bi-annual performance calibration cycles (June and December).
Performance ratings are calibrated on a 1.0 to 5.0 scale:
- 4.5+: Exceeds All Expectations (Eligible for accelerated equity refreshes and promotions)
- 3.5 - 4.4: Consistently Strong Performance (Eligible for standard bonuses and merit raises)
- 3.0 - 3.4: Solid Contributor
- Below 3.0: Requires Performance Improvement Plan (PIP)

## 4. Employee Benefits Summary
All full-time staff enjoy comprehensive medical coverage (Corporate Health Shield), annual wellness allowances ($1,200/year), continuous learning credits ($2,500/year for approved certifications), and 25 days of paid annual vacation plus public holidays.
"""
}

PRODUCTS = {
    "corporate_health_shield.md": """# Corporate Health Shield (Group Health Insurance)
Product ID: PRD-INS-001
Category: Group Health & Medical
Target Audience: Enterprise Corporate Clients (50+ employees)
Underwriting Carrier: Acme Mutual Life & Health Assurance

## 1. Product Overview
Corporate Health Shield provides comprehensive inpatient hospitalization, day-care procedure, and pre/post-hospitalization medical coverage for corporate employee cohorts and their families.
Base sum insured options: $100,000 USD to $500,000 USD per family floater unit.

## 2. Eligibility Requirements
- Active full-time employees aged 18 to 65.
- Eligible dependents: Legally married spouse, up to 3 dependent children (aged 0 to 25), and dependent parents/parents-in-law up to age 80.
- Minimum corporate group size: 25 enrolled employees.

## 3. Mandatory Documentation Required for Onboarding & Claims
- Employee corporate enrollment roster with date of birth and tax identifier.
- Dependent relationship declarations (Marriage Certificate for spouse, Birth Certificates for children).
- For claims: Hospitalization discharge summary, original pharmacy and diagnostic invoices, and completed Form Claim-A.

## 4. Coverage Highlights
- Zero waiting period for pre-existing diseases.
- Maternity coverage up to $10,000 with newborn baby cover from Day 1.
- Air ambulance evacuation coverage up to $25,000 per incident.
- Cashless network covering over 12,000 accredited hospitals globally.
""",

    "term_life_pro.md": """# Term Life Pro (Executive Group Life Protection)
Product ID: PRD-INS-002
Category: Group Life Assurance
Target Audience: C-Suite, Senior Executives, and Key Enterprise Staff
Underwriting Carrier: Acme Mutual Assurance

## 1. Product Overview
Term Life Pro offers high-value pure risk life assurance designed to protect corporate executive families against untimely death or terminal illness.
Benefit payout: Up to 5x annual base compensation or fixed benefit up to $5,000,000 USD.

## 2. Eligibility Requirements
- Full-time executives and senior managers with minimum annual compensation of $120,000 USD.
- Age bracket: 21 to 65 years.
- Non-smoker preferential pricing tiers available.

## 3. Required Underwriting Documents
1. Certified corporate compensation statement and last 2 years tax returns (W-2 / Form 16).
2. Tele-medical health underwriting report for coverage exceeding $2,000,000.
3. Official corporate beneficiary nomination document signed in presence of human resources witness.
""",

    "cyber_risk_elite.md": """# Cyber Risk Elite (Enterprise Data Breach & Extortion Insurance)
Product ID: PRD-INS-003
Category: Cyber & Specialty Lines
Target Audience: Technology, FinTech, Healthcare, and Cloud Enterprises
Underwriting Carrier: Acme Cyber Underwriters Lloyd's Syndicate

## 1. Product Overview
Comprehensive first-party and third-party cyber insurance policy safeguarding enterprises against data breaches, ransomware extortion, network interruption, and regulatory fines under GDPR and HIPAA.
Aggregate limits available from $5,000,000 to $50,000,000 USD.

## 2. Mandatory Eligibility Prerequisites
- 100% enforcement of Multi-Factor Authentication (MFA) across all email, remote VPN, and cloud administrator consoles.
- Endpoint Detection and Response (EDR) agents active on 98%+ of corporate server and workstation assets.
- Immutable, air-gapped daily backups verified with quarterly restoration testing.
- Annual third-party penetration testing with all critical vulnerabilities patched within 14 days.

## 3. Documentation Required for Policy Inception
1. Completed Acme Cyber Risk Assessment Questionnaire (CRAQ-2026).
2. SOC 2 Type II or ISO 27001:2022 independent audit report.
3. Incident Response Plan and Business Continuity Plan (BCP) documentation.
4. Corporate security topology architecture diagram.
""",

    "keyman_insurance.md": """# Keyman Insurance (Business Continuity Life Protection)
Product ID: PRD-INS-004
Category: Commercial Life & Partnership Protection
Target Audience: Mid-market and Enterprise Corporations
Underwriting Carrier: Acme Corporate Assurance

## 1. Product Overview
Keyman insurance indemnifies a corporation against financial loss, revenue drop, or credit disruption caused by the death or severe disability of a critical business executive or founder.
The corporation is both the premium payer and the direct policy beneficiary.

## 2. Eligibility Requirements
- The key person must own less than 51% direct voting equity of the enterprise.
- Key person must be an active employee or executive officer contributing directly to bottom-line profitability.
- Board of Directors formal resolution approving the insurance procurement is mandatory.

## 3. Required Documents
1. Certified Board Resolution authorizing the Keyman policy purchase.
2. Audited corporate financial balance sheets and P&L statements for preceding 3 fiscal years.
3. Comprehensive medical examination report of the designated Key person.
4. Key person employment agreement highlighting non-compete and intellectual property assignment.
""",

    "executive_disability_income.md": """# Executive Long-Term Disability Shield
Product ID: PRD-INS-005
Category: Income Protection & Disability
Target Audience: Professional Services, Technology Engineers, Executives
Underwriting Carrier: Acme Disability Syndicate

## 1. Product Overview
Replaces up to 66.6% of gross monthly earnings up to $25,000 USD per month in the event an employee suffers total or partial disability preventing them from performing their regular occupation ("Own Occupation" definition).

## 2. Eligibility Requirements
- Full-time salaried employees working minimum 32 hours per week.
- Age: 18 to 64 years.
- Elimination waiting period: 90 days or 180 days consecutive disability before benefit disbursement starts.

## 3. Required Documents for Claim
- Attending physician medical statement and disability certification.
- Pre-disability salary slips for the 6 months immediately preceding date of disabling event.
- Employer job description and physical demand analysis form.
""",

    "commercial_fleet_cover.md": """# Commercial Fleet & Logistics Motor Policy
Product ID: PRD-INS-006
Category: Commercial Property & Casualty
Target Audience: Supply Chain, Logistics, Delivery, Corporate Transport
Underwriting Carrier: Acme General Insurance Co.

## 1. Product Overview
Comprehensive motor and liability coverage for commercial vehicle fleets (sedans, delivery vans, heavy transport trucks).
Includes third-party property damage, driver accidental death cover, and cargo-in-transit loss indemnity.

## 2. Eligibility & Fleet Criteria
- Minimum fleet size: 5 commercial vehicles.
- Telematics GPS monitoring devices must be installed across all active fleet units.
- Commercial driver licensing verified with zero fatal violation records in past 36 months.

## 3. Required Onboarding Documents
- Vehicle registration certificates (RC) and fitness inspection certifications.
- Driver commercial driving licenses and background check verifications.
- Route risk assessment profile and hazardous materials handling permits if applicable.
""",

    "group_gratuity_plan.md": """# Group Gratuity and Pension Trust Plan
Product ID: PRD-INS-007
Category: Retirement & Institutional Funds
Target Audience: Corporate Employers managing statutory employee retirement trusts
Underwriting Carrier: Acme Institutional Asset Management

## 1. Product Overview
Enables corporate employers to fund statutory gratuity and long-term retirement liabilities tax-efficiently through an actuarially managed unit-linked group fund.
Provides capital protection guarantees with stable long-term yields.

## 2. Eligibility Requirements
- Registered corporate legal entity with minimum 20 permanent employees.
- Establishment of an approved Employee Gratuity Trust under regional income tax statutes.

## 3. Required Documents
1. Executed Trust Deed and Rules of the Gratuity Fund.
2. Official Tax Exemption Approval Certificate from Revenue authorities.
3. Actuarial valuation report for existing past-service liability.
4. Member demographic census file (Employee ID, Date of Joining, Basic Salary).
""",

    "directors_and_officers_liability.md": """# Directors & Officers (D&O) Liability Assurance
Product ID: PRD-INS-008
Category: Executive Management Liability
Target Audience: Public and Private Corporate Boards
Underwriting Carrier: Acme Specialty Casualty Syndicate

## 1. Product Overview
Protects directors, officers, and supervisory board members against personal financial liability arising from legal actions, shareholder lawsuits, regulatory investigations, and allegations of managerial negligence or breach of fiduciary duty.

## 2. Eligibility Requirements
- Audited enterprise operations with minimum 2 years trading history.
- Clean claims history with no unresolved shareholder derivative lawsuits.
- Independent external legal counsel and audit committee in active standing.

## 3. Required Documents
- Signed D&O Proposal Form.
- Latest Audited Annual Financial Report.
- Prospectus or private placement memorandum if planning public listing within next 12 months.
- List of current corporate subsidiary entities and ownership percentages.
""",

    "property_and_casualty_umbrella.md": """# Commercial Property & Business Interruption Umbrella
Product ID: PRD-INS-009
Category: Commercial Property & Asset Protection
Target Audience: Enterprise Manufacturing, Tech Parks, Real Estate
Underwriting Carrier: Acme Property Assurance

## 1. Product Overview
All-risks industrial coverage protecting physical structures, plant machinery, inventory, and office assets against fire, earthquake, flood, explosion, and ensuing business interruption loss of gross profit.

## 2. Eligibility Requirements
- Commercial properties equipped with automated fire sprinkler systems meeting NFPA standards.
- 24/7 security monitoring and fire hydrant installations inspected annually.
- Comprehensive asset registers with replacement value appraisal completed within 24 months.

## 3. Required Documents
1. Asset Valuation Appraisal Report.
2. Fire Safety Inspection and Sprinkler Testing Certificate.
3. Historical Gross Profit financial records for business interruption calculations.
""",

    "marine_cargo_international.md": """# Global Marine Cargo & Transit Protection
Product ID: PRD-INS-010
Category: Marine & Trade Finance Insurance
Target Audience: Multinational Exporters, Importers, E-commerce Logistics
Underwriting Carrier: Acme Maritime Underwriters

## 1. Product Overview
Institute Cargo Clauses (A) all-risks international transit protection covering ocean freight, air cargo, and cross-border land shipping against physical damage, piracy, vessel stranding, and general average contribution.

## 2. Eligibility Requirements
- Commercial shipping invoices with recognized Incoterms (CIF, FOB, CIP).
- Approved commercial freight forwarders and carrier vessels classified under IACS.

## 3. Required Documents
- Commercial Sales Invoice and Packing List.
- Original Ocean Bill of Lading (B/L) or Air Waybill (AWB).
- Survey Report and Damage Notice in the event of cargo claims.
"""
}

CONTRACTS = {
    "vendor_abc_cloud_hosting_sla.md": """# Master Service Agreement & SLA: Vendor ABC Cloud Hosting
Contract ID: CNT-VND-2024-001
Parties: Acme Enterprise Corp ("Customer") & Vendor ABC Cloud Solutions Inc ("Vendor")
Effective Date: 2024-01-01 | Expiry Date: 2027-12-31
Governing Law: State of California, United States

## 1. Scope of Hosted Infrastructure Services
Vendor ABC provides multi-region cloud virtual machine hosting, managed Kubernetes orchestration, and persistent NVMe storage volumes across US-East and EU-West regions.

## 2. Service Level Agreement (SLA) Commitments
- System Availability: 99.95% monthly uptime.
- Downtime Compensation: 10% monthly service credit for availability between 99.0% and 99.95%; 25% credit for availability below 99.0%.
- Severity 1 Outage Response Time: Vendor engineers must initiate interactive response within 15 minutes of alert generation.

## 3. Security, Access Restrictions and Compliance Obligations
1. Data Sovereignty: Customer data originating from the European Union must remain physically resident within Vendor ABC's Frankfurt (eu-central-1) data center and cannot be replicated across transatlantic boundaries without written consent.
2. Subcontractor Restrictions: Vendor ABC may not subcontract infrastructure management or data processing to any third-party entity without providing 60 calendar days advance notice and receiving written authorization from Customer's CISO.
3. Security Audits: Customer retains the right to conduct an annual on-site physical data center audit and bi-annual automated network vulnerability penetration tests.
4. Termination for Breach: Either party may terminate this agreement immediately upon written notice if the opposing party commits a material breach of data confidentiality or suffers an uncontained security intrusion.
""",

    "global_health_tpa_msa.md": """# Master Services Agreement: Global Health Third-Party Administrator
Contract ID: CNT-TPA-2025-089
Parties: Acme Enterprise Corp ("Plan Sponsor") & MediClaim Global TPA Services LLC ("TPA")
Effective Date: 2025-04-01 | Expiry Date: 2028-03-31
Governing Law: State of New York

## 1. TPA Claims Adjudication Obligations
The TPA shall manage medical claims adjudication, hospital network cashless admissions, and reimbursement processing for all 15,000+ eligible Acme employees and their dependents.

## 2. Turnaround Time (TAT) Commitments
- Cashless Pre-Authorization: 120 minutes for planned admissions; 45 minutes for emergency admissions.
- Reimbursement Claim Processing: Payment disbursement or formal claim rejection notice within 7 business days of complete document submission.

## 3. Data Protection and HIPAA Compliance
The TPA shall maintain strict Business Associate Agreement (BAA) safeguards under HIPAA.
Protected Health Information (PHI) must be stored in encrypted databases with restricted role-based access logs audited monthly.
""",

    "delta_logistics_fleet_sla.md": """# Fleet Logistics & Transport Master Services Contract
Contract ID: CNT-LOG-2025-014
Parties: Acme Enterprise Corp & Delta Logistics Global LLC
Effective Date: 2025-02-01 | Expiry Date: 2027-01-31
Governing Law: State of Illinois

## 1. Scope of Fleet Operations
Delta Logistics provides dedicated commercial transport vehicles, temperature-controlled refrigerated trailers, and certified commercial operators for regional distribution hubs.

## 2. Insurance and Indemnity Obligations
Delta Logistics must maintain comprehensive commercial motor insurance with minimum coverage of $5,000,000 USD per incident, naming Acme Enterprise Corp as an Additional Insured party.
All drivers must undergo mandatory drug screening and background checks every 12 months.

## 3. Operational Penalties
Late delivery exceeding 2 hours beyond scheduled loading window incur a penalty of $200 per incident.
Cargo damage caused by failure of temperature monitoring is subject to 100% full invoice value reimbursement within 14 calendar days.
""",

    "acme_legal_advisory_retainer.md": """# Legal Advisory and Corporate Counsel Retainer Agreement
Contract ID: CNT-LEG-2026-003
Parties: Acme Enterprise Corp & Morrison, Sterling & Sterling LLP ("Counsel")
Effective Date: 2026-01-01 | Expiry Date: 2026-12-31
Governing Law: England and Wales

## 1. Retained Legal Services
Counsel provides strategic advice covering multinational intellectual property protection, corporate securities filings, executive employment arbitration, and cross-border commercial litigation.

## 2. Fee Structure and Billing
- Fixed Monthly Retainer: $35,000 USD covering up to 60 attorney hours per billing month.
- Excess Partner Hours: Discounted hourly rate of $650 USD/hour.
- Billing reports must be itemized in 6-minute increments and submitted by the 5th business day of each succeeding month.

## 3. Conflict of Interest Restrictions
Counsel covenants not to represent any direct commercial competitor in matters adverse to Acme Enterprise Corp during the active term of this agreement and for a period of 12 months following termination.
""",

    "zenith_secops_agreement.md": """# Managed Security Operations Center (SOC) Master Contract
Contract ID: CNT-SEC-2025-044
Parties: Acme Enterprise Corp & Zenith Cyber Defense Systems Inc ("Zenith")
Effective Date: 2025-05-01 | Expiry Date: 2028-04-30
Governing Law: State of Delaware

## 1. Managed 24/7/365 Detection & Response
Zenith provides continuous threat monitoring, SIEM log correlation, endpoint telemetry surveillance, and automated threat hunting across Acme's multi-cloud and on-premise infrastructure.

## 2. Service Level SLA & Severity Response
- Critical Incident Alert Escalation: Within 10 minutes of malicious payload detection.
- Containment Action: Automated isolation of infected endpoints within 15 minutes of confirmation.

## 3. Confidentiality and Security Standards
Zenith staff assigned to Acme accounts must possess active CISSP or equivalent certifications and have passed federal background security clearance.
All telemetry logs must be stored in sovereign, encrypted repositories retained for 400 days.
""",

    "ceo_compensation_contract.md": """# Executive Employment Agreement & CEO Compensation Contract
Contract ID: CNT-EXEC-2026-001
Parties: Acme Enterprise Corp ("Company") & Chief Executive Officer ("Executive")
Effective Date: 2026-01-01 | Expiry Date: 2029-12-31
Department: Board of Directors & Compensation Committee
Access Roles: admin, hr
Governing Law: State of Delaware, United States
Classification: STRICTLY CONFIDENTIAL - EXECUTIVE ACCESS ONLY

## 1. Executive Compensation & Base Salary
The Executive shall receive an annual base salary of $1,850,000 USD, payable semi-monthly in accordance with the Company's standard executive payroll schedule.
Annual base salary is subject to upward review annually by the Compensation Committee of the Board of Directors.

## 2. Incentive Bonuses and Equity Vesting
- Performance Bonus: Target annual incentive bonus of 200% of Base Salary ($3,700,000 USD), contingent upon achieving Board-approved EBITDA targets and ESG governance milestones.
- Long-Term Incentive Equity: 250,000 Restricted Stock Units (RSUs) vesting over 4 years on a quarterly schedule (25% cliff at 12 months, quarterly thereafter).
- Change of Control ("Golden Parachute"): In the event of a qualifying termination following a Change in Control, the Executive is entitled to 2.5x Base Salary plus immediate acceleration of 100% unvested equity awards.

## 3. Executive Benefits, Perquisites and Aircraft Usage
- The Executive is granted up to 75 personal flight hours per calendar year on Company-leased private corporate aircraft.
- Full family comprehensive concierge medical, dental, and executive disability coverage funded 100% by the Company.
- Annual executive security protection and secure residential cyber monitoring allowance of $150,000 USD.

## 4. Restrictive Covenants and Confidentiality
The Executive covenants that during the term of employment and for 24 months following departure:
1. Executive shall not directly or indirectly engage with, advise, or invest in any designated Tier-1 enterprise competitor.
2. Executive shall not solicit enterprise clients, executives, or engineering talent.
3. This agreement is classified as strictly confidential and is restricted to Board members, Chief Human Resources Officer, and authorized Corporate Legal Counsel.
"""
}


def generate_all_docs():
    os.makedirs(POL_DIR, exist_ok=True)
    os.makedirs(PROD_DIR, exist_ok=True)
    os.makedirs(CONT_DIR, exist_ok=True)

    for filename, content in POLICIES.items():
        with open(os.path.join(POL_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    print(f"Generated {len(POLICIES)} policy documents in {POL_DIR}")

    for filename, content in PRODUCTS.items():
        with open(os.path.join(PROD_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    print(f"Generated {len(PRODUCTS)} product documents in {PROD_DIR}")

    for filename, content in CONTRACTS.items():
        with open(os.path.join(CONT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
    print(f"Generated {len(CONTRACTS)} contract documents in {CONT_DIR}")


if __name__ == "__main__":
    generate_all_docs()
