"""Finance, health & safety, sustainability and customer-facing policies."""

FINANCE_POLICIES = [
    dict(file="corporate_credit_card_policy", id="POL-FIN-111", title="Corporate Credit Card Policy",
         dept="Global Finance", owner="Corporate Controller", ver="2.4", date="2026-02-23", sections=[
        ("1. Eligibility and Limits", "Corporate cards are issued to employees who travel or purchase regularly, with manager approval. Default monthly limits are $5,000 USD for staff and $15,000 USD for Directors and above."),
        ("2. Use and Reconciliation", "Cards are for business expenses only, personal use is prohibited. Receipts must be uploaded and expenses reconciled within 10 business days of the statement. Lost cards must be reported to the bank and Finance immediately."),
    ]),
    dict(file="financial_reporting_and_sox_controls_policy", id="POL-FIN-112", title="Financial Reporting and Internal Controls (SOX) Policy",
         dept="Global Finance", owner="Chief Financial Officer", ver="3.5", date="2026-07-20", sections=[
        ("1. Accuracy of Records", "All transactions must be recorded accurately, promptly and with supporting documents. Falsifying, hiding or delaying entries is strictly prohibited."),
        ("2. Internal Controls", "Key financial controls are documented, tested by Internal Audit every year and certified quarterly by control owners. The CEO and CFO certify the financial statements. Deficiencies are reported to the Audit Committee."),
        ("3. Month-End Close", "The books are closed within 6 business days of month-end, with all manual journal entries reviewed by a second person."),
    ]),
    dict(file="payroll_and_tax_withholding_policy", id="POL-FIN-113", title="Payroll Processing and Tax Withholding Policy",
         dept="Global Finance", owner="Global Payroll Manager", ver="3.0", date="2026-01-08", sections=[
        ("1. Pay Schedule", "Salaries are paid monthly on the last working day of the month by direct bank transfer. Payslips are available in the HR portal on the day of payment. Changes to bank details must be submitted by the 20th to take effect in that month."),
        ("2. Tax Withholding", "Income tax and statutory contributions are withheld according to local law. Annual tax statements are issued within 30 days of the tax year end."),
    ]),
    dict(file="budget_and_capital_expenditure_policy", id="POL-FIN-114", title="Budgeting and Capital Expenditure Policy",
         dept="Global Finance", owner="VP of Financial Planning & Analysis", ver="2.1", date="2026-04-01", sections=[
        ("1. Annual Budget", "Budgets are prepared each October and approved by the Board in December. Spending beyond the approved budget by more than 5% needs CFO approval."),
        ("2. Capital Expenditure", "Purchases of assets above $25,000 USD are capitalised and need a business case. Projects above $500,000 USD need Investment Committee approval and a post-implementation review within 12 months."),
    ]),
]

EHS_POLICIES = [
    dict(file="workplace_health_and_safety_policy", id="POL-EHS-001", title="Workplace Health and Safety Policy",
         dept="Environment, Health & Safety", owner="Head of EHS", ver="3.2", date="2026-03-09", sections=[
        ("1. Responsibilities", "Acme provides a safe workplace. Every employee must follow safety rules, report hazards and stop unsafe work. Managers must complete safety training and inspect their areas quarterly."),
        ("2. Incident Reporting", "All workplace accidents, injuries and near misses must be reported to EHS within 24 hours. Serious injuries are investigated within 3 business days and reported to authorities as the law requires."),
        ("3. Ergonomics and First Aid", "Employees may request an ergonomic assessment of their workstation. Trained first aiders and defibrillators are available at every office."),
    ]),
    dict(file="drug_and_alcohol_free_workplace_policy", id="POL-EHS-002", title="Drug and Alcohol-Free Workplace Policy",
         dept="Environment, Health & Safety", owner="Head of EHS", ver="2.0", date="2026-01-14", sections=[
        ("1. Prohibited Conduct", "Working under the influence of alcohol or illegal drugs, and possessing, selling or using illegal drugs on company premises or business, is prohibited. Alcohol may be served only at approved company events."),
        ("2. Support", "Employees who seek help voluntarily before any incident are referred to the EAP and will not be disciplined for asking for support."),
    ]),
    dict(file="workplace_violence_prevention_policy", id="POL-EHS-003", title="Workplace Violence Prevention Policy",
         dept="Corporate Security", owner="Head of Corporate Security", ver="2.1", date="2026-02-12", sections=[
        ("1. Zero Tolerance", "Threats, intimidation, physical violence and possession of weapons on company premises are prohibited. This includes threats made by phone, email or social media."),
        ("2. Reporting and Response", "Any threat must be reported at once to Corporate Security, and to emergency services if there is immediate danger. Security assesses each report within 4 hours and can restrict site access while it is reviewed."),
    ]),
    dict(file="emergency_and_crisis_management_policy", id="POL-EHS-004", title="Emergency Evacuation and Crisis Management Policy",
         dept="Environment, Health & Safety", owner="Head of EHS", ver="2.5", date="2026-05-05", sections=[
        ("1. Evacuation", "Every site has an evacuation plan with named floor wardens. Fire drills are held twice a year. On an alarm, employees must leave immediately by the nearest exit and gather at the assembly point."),
        ("2. Crisis Communication", "In a crisis, employees must follow instructions from the Crisis Management Team, check the emergency notification system and not speak to the media."),
    ]),
    dict(file="travel_safety_and_duty_of_care_policy", id="POL-EHS-005", title="Travel Safety and Duty of Care Policy",
         dept="Environment, Health & Safety", owner="Head of Corporate Security", ver="2.2", date="2026-06-16", sections=[
        ("1. Before Travel", "International travel must be booked through the approved travel agency so that Acme can locate travellers in an emergency. Travel to high-risk destinations needs Security approval at least 10 business days before departure."),
        ("2. During Travel", "Travellers are covered by the corporate travel insurance and can call the 24/7 assistance line. Employees must check in after arrival in high-risk locations and carry the emergency contact card."),
    ]),
    dict(file="environmental_sustainability_and_esg_policy", id="POL-ESG-001", title="Environmental Sustainability and ESG Policy",
         dept="Corporate Sustainability", owner="Chief Sustainability Officer", ver="2.3", date="2026-07-27", sections=[
        ("1. Targets", "Acme targets net-zero operational emissions by 2040 and a 50% reduction in Scope 1 and 2 emissions by 2030 from a 2022 baseline. Progress is reported annually in the sustainability report."),
        ("2. Operations", "Offices use renewable electricity where available. Business flights are reduced through virtual meetings for trips under 2 hours, and e-waste is recycled through certified vendors."),
        ("3. Sustainable Investing", "ESG risks are included in investment and underwriting decisions for corporate clients."),
    ]),
]

CUSTOMER_POLICIES = [
    dict(file="customer_complaint_handling_policy", id="POL-CX-001", title="Customer Complaint Handling Policy",
         dept="Customer Experience", owner="Head of Customer Experience", ver="3.1", date="2026-04-30", sections=[
        ("1. Acknowledgement and Resolution", "Complaints are acknowledged within 2 business days and resolved within 15 business days. Complex cases may take up to 30 days if the customer is updated every 7 days."),
        ("2. Escalation", "Customers who are not satisfied may ask for review by a senior manager and then by the independent ombudsman. Every complaint is logged, categorised and reviewed monthly for root causes."),
    ]),
    dict(file="fair_treatment_of_customers_and_claims_policy", id="POL-CX-002", title="Fair Treatment of Customers and Claims Handling Policy",
         dept="Claims & Customer Experience", owner="Director of Claims Processing", ver="2.9", date="2026-05-12", sections=[
        ("1. Fair Treatment", "Customers must receive clear, honest information about coverage, exclusions and premiums. Vulnerable customers receive additional support and plain-language explanations."),
        ("2. Claims Service Standards", "Claims are acknowledged within 1 business day. Straightforward claims are decided within 10 business days of receiving all documents, and payment follows within 5 business days of approval. Every rejection must state the reason in writing and explain how to appeal."),
    ]),
    dict(file="underwriting_authority_policy", id="POL-UW-001", title="Underwriting Authority and Risk Acceptance Policy",
         dept="Insurance Underwriting", owner="Chief Underwriting Officer", ver="3.2", date="2026-06-03", sections=[
        ("1. Authority Limits", "Underwriter: up to $1,000,000 USD sum insured. Senior Underwriter: up to $5,000,000 USD. Chief Underwriter: up to $25,000,000 USD. Anything above needs the Underwriting Committee."),
        ("2. Referrals and Exclusions", "Risks with prior losses above $500,000 USD, sanctioned jurisdictions, or incomplete disclosure must be referred. Underwriters may not approve their own relatives or personal contacts."),
    ]),
]
