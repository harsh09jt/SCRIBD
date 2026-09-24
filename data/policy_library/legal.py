"""Ethics, legal, compliance, procurement and communications policies."""

MGMT = ["manager", "hr", "legal", "admin"]
INVEST = ["hr", "legal", "admin"]

LEGAL_POLICIES = [
    dict(file="anti_bribery_and_corruption_policy", id="POL-ETH-011", title="Anti-Bribery and Corruption Policy",
         dept="Legal & Compliance", owner="Chief Compliance Officer", ver="3.1", date="2026-03-10", sections=[
        ("1. Zero Tolerance", "Acme prohibits offering, paying, requesting or accepting a bribe or improper advantage, directly or through an agent, to or from anyone, including government officials. The policy follows the US FCPA, the UK Bribery Act and local anti-corruption laws."),
        ("2. Facilitation Payments and Third Parties", "Facilitation (grease) payments are not permitted. Agents, distributors and consultants who deal with government must pass anti-corruption due diligence and sign an anti-bribery clause before engagement."),
        ("3. Reporting and Consequences", "Suspected bribery must be reported to Compliance or the ethics hotline immediately. Violations lead to disciplinary action up to termination and may be reported to authorities. Anti-bribery training is required annually."),
    ]),
    dict(file="gifts_and_entertainment_policy", id="POL-ETH-012", title="Gifts, Hospitality and Entertainment Policy",
         dept="Legal & Compliance", owner="Chief Compliance Officer", ver="2.8", date="2026-03-10", sections=[
        ("1. Gift Limits", "Employees may accept or give a gift or hospitality of a modest value, up to $100 USD per person per occasion and $300 USD per person per year. Cash and cash equivalents such as gift cards are never permitted."),
        ("2. Pre-Approval and Register", "Anything above the limit needs written approval from the manager and Compliance before it is accepted or given. All gifts and hospitality above $50 USD must be recorded in the Gift Register within 5 business days."),
        ("3. Government Officials and Active Tenders", "Gifts to government officials require prior Legal approval. No gifts may be exchanged with a supplier during an open tender."),
    ]),
    dict(file="conflict_of_interest_policy", id="POL-ETH-013", title="Conflict of Interest Policy",
         dept="Legal & Compliance", owner="Chief Compliance Officer", ver="3.0", date="2026-01-28", sections=[
        ("1. What Is a Conflict", "A conflict of interest arises when a personal, financial or family interest could influence, or appear to influence, your business judgement. Examples include hiring relatives, owning more than 1% of a supplier or competitor, and outside board roles."),
        ("2. Disclosure", "Employees disclose any actual or potential conflict in the compliance portal within 10 days of becoming aware, and again in the annual attestation. The manager and Compliance decide on mitigation."),
        ("3. Outside Activities", "Paid outside work or board service needs prior written approval and must not use Acme time, confidential information or resources."),
    ]),
    dict(file="insider_trading_and_securities_dealing_policy", id="POL-ETH-014", title="Insider Trading and Securities Dealing Policy",
         dept="Legal & Compliance", owner="General Counsel", ver="3.3", date="2026-02-16", sections=[
        ("1. Inside Information", "Material non-public information (for example unreleased financial results, mergers, major contracts or cyber incidents) must not be used to trade securities or be shared with anyone who does not need it. This applies to Acme and to other listed companies."),
        ("2. Blackout Periods and Pre-Clearance", "Designated insiders may not trade from 14 days before quarter-end until 2 full trading days after earnings are released. All insider trades need pre-clearance from Legal, valid for 3 trading days."),
        ("3. Penalties", "Breaches may lead to dismissal and civil or criminal prosecution. Short selling and trading in derivatives of Acme securities are prohibited."),
    ]),
    dict(file="political_contributions_and_lobbying_policy", id="POL-ETH-015", title="Political Contributions and Lobbying Policy",
         dept="Legal & Compliance", owner="General Counsel", ver="1.9", date="2025-12-05", sections=[
        ("1. Corporate Contributions", "Acme does not make political contributions, in cash or in kind, unless approved in writing by the General Counsel and the Board. Company resources may not be used for personal political activity."),
        ("2. Personal Activity and Lobbying", "Employees may engage in politics in their own time and at their own expense. Any lobbying of government on Acme's behalf must be coordinated with Government Affairs and Legal."),
    ]),
    dict(file="human_rights_and_modern_slavery_policy", id="POL-ETH-016", title="Human Rights and Modern Slavery Policy",
         dept="Legal & Compliance", owner="Chief Compliance Officer", ver="2.0", date="2026-04-14", sections=[
        ("1. Our Commitment", "Acme prohibits forced, bonded, prison and child labour, and human trafficking, in its own operations and its supply chain. The minimum working age is 18 for hazardous work and never below the local legal minimum."),
        ("2. Supply Chain Due Diligence", "High-risk suppliers are assessed every year and audited on-site every 2 years. Confirmed violations lead to a corrective action plan within 30 days or termination of the contract."),
    ]),
    dict(file="anti_money_laundering_policy", id="POL-GRC-070", title="Anti-Money Laundering and Counter-Terrorist Financing Policy",
         dept="Governance, Risk & Compliance", owner="Money Laundering Reporting Officer", ver="3.4", date="2026-05-06", sections=[
        ("1. Customer Due Diligence", "Know-Your-Customer (KYC) checks are required before any policy is issued or payment is made. High-risk customers and politically exposed persons need enhanced due diligence and senior management approval."),
        ("2. Monitoring and Reporting", "Transactions are monitored for unusual patterns. Employees must report suspicion to the Money Laundering Reporting Officer the same day. Employees must not tip off the customer."),
        ("3. Record Keeping", "KYC and transaction records are kept for at least 7 years after the end of the customer relationship."),
    ]),
    dict(file="sanctions_and_export_control_policy", id="POL-GRC-071", title="Sanctions and Export Control Policy",
         dept="Governance, Risk & Compliance", owner="General Counsel", ver="2.5", date="2026-06-11", sections=[
        ("1. Screening", "Customers, suppliers, beneficiaries and payment counterparties are screened against OFAC, UN, EU and UK sanctions lists at onboarding and daily thereafter."),
        ("2. Prohibited Dealings", "Acme does not do business with sanctioned persons or in comprehensively sanctioned territories. Potential matches must be escalated to Legal before any transaction proceeds."),
        ("3. Export Controls", "Transfers of encryption software or controlled technology across borders require classification review by Legal before shipment or access is granted."),
    ]),
    dict(file="antitrust_and_fair_competition_policy", id="POL-GRC-072", title="Antitrust and Fair Competition Policy",
         dept="Governance, Risk & Compliance", owner="General Counsel", ver="2.1", date="2026-02-24", sections=[
        ("1. Prohibited Agreements", "Employees must never agree with competitors on prices, discounts, markets, customers, bids or output. Even informal discussions of these topics at trade events are prohibited."),
        ("2. Trade Associations and Information Sharing", "Legal must approve participation in trade association meetings, and an agenda must be circulated in advance. Competitively sensitive information must not be exchanged. Leave the meeting and tell Legal if such topics arise."),
    ]),
    dict(file="intellectual_property_policy", id="POL-LEG-020", title="Intellectual Property Policy",
         dept="Legal", owner="Chief IP Counsel", ver="3.0", date="2026-03-30", sections=[
        ("1. Ownership", "Work created by employees in the course of their job, including code, designs, documents and inventions, is owned by Acme. Employees sign an IP assignment agreement at joining."),
        ("2. Invention Disclosure", "Potential inventions must be disclosed to Legal through the invention disclosure form before any public disclosure. Employees receive an award of $2,000 USD for each patent filed."),
        ("3. Third-Party IP", "Employees may not use or copy third-party copyrighted material, trademarks or confidential information without a license or permission."),
    ]),
    dict(file="open_source_software_policy", id="POL-LEG-021", title="Open Source Software Usage and Contribution Policy",
         dept="Legal & Engineering", owner="Chief IP Counsel", ver="2.2", date="2026-04-09", sections=[
        ("1. Approved Licenses", "Permissive licenses (MIT, Apache 2.0, BSD) are pre-approved. Weak copyleft (LGPL, MPL) needs review. Strong copyleft licenses such as GPL and AGPL must not be used in distributed products without Legal approval."),
        ("2. Tracking and Scanning", "All open source components must be listed in the software bill of materials (SBOM) and scanned in the CI pipeline for licenses and known vulnerabilities."),
        ("3. Contributing Code", "Contributions to external projects on work time require approval from the engineering director and Legal, and must not include confidential or customer code."),
    ]),
    dict(file="records_retention_and_legal_hold_policy", id="POL-LEG-022", title="Records Retention and Legal Hold Policy",
         dept="Legal", owner="General Counsel", ver="3.1", date="2026-01-19", sections=[
        ("1. Retention Schedule", "Financial and tax records: 7 years. Contracts: 7 years after expiry. Employee records: 7 years after separation. Insurance policy and claim files: 10 years. Marketing materials: 3 years. Email is kept for 3 years."),
        ("2. Legal Hold", "When litigation or an investigation is reasonably expected, Legal issues a legal hold. All deletion of related records, including automated deletion, must stop immediately until Legal releases the hold in writing."),
        ("3. Secure Disposal", "After the retention period, paper records are shredded and electronic records are securely erased with a certificate of destruction."),
    ]),
    dict(file="fraud_prevention_and_investigation_policy", id="POL-GRC-073", title="Fraud Prevention and Investigation Procedure",
         dept="Governance, Risk & Compliance", owner="Head of Internal Audit", ver="2.7", date="2026-06-25", roles=INVEST, sections=[
        ("1. Reporting Suspected Fraud", "Any suspicion of fraud must be reported to Internal Audit or the ethics hotline within 24 hours. The reporter must not investigate or confront the suspect."),
        ("2. Investigation Steps", "Internal Audit and Legal open a case within 2 business days, secure evidence and interview relevant people. The suspect may be placed on paid leave. Findings are reported to the Audit Committee within 30 days."),
        ("3. Recovery and Referral", "Losses are recovered through payroll deduction, insurance or civil action. Cases involving criminal conduct are referred to law enforcement on the advice of Legal."),
    ]),
    dict(file="supplier_code_of_conduct", id="POL-PRC-010", title="Supplier Code of Conduct",
         dept="Procurement", owner="Chief Procurement Officer", ver="2.3", date="2026-02-09", sections=[
        ("1. Required Standards", "Suppliers must comply with all applicable laws, respect human rights, provide safe workplaces, pay at least the legal minimum wage, and prohibit bribery and corruption."),
        ("2. Information Security and Data Protection", "Suppliers handling Acme data must meet the Information Security Policy, notify Acme of a breach within 24 hours and allow security audits."),
        ("3. Audit and Termination", "Acme may audit suppliers on 30 days' notice. Material breaches that are not corrected within 30 days can lead to termination."),
    ]),
    dict(file="procurement_and_sourcing_policy", id="POL-PRC-011", title="Procurement and Sourcing Policy",
         dept="Procurement", owner="Chief Procurement Officer", ver="3.6", date="2026-05-13", sections=[
        ("1. Competitive Bidding", "Purchases below $10,000 USD need one quote. Between $10,000 and $100,000 USD need 3 quotes. Above $100,000 USD require a formal tender. Sole-source purchases need written justification and Procurement approval."),
        ("2. Purchase Orders", "No goods or services may be ordered without an approved purchase order. Invoices without a valid PO are not paid. Payment terms are net 45 days by default."),
        ("3. Vendor Onboarding", "New vendors go through the Vendor Management Policy risk assessment and sanctions screening before first payment."),
    ]),
    dict(file="media_relations_and_external_communications_policy", id="POL-COM-001", title="Media Relations and External Communications Policy",
         dept="Corporate Communications", owner="Head of Corporate Communications", ver="2.2", date="2026-03-04", sections=[
        ("1. Authorised Spokespeople", "Only the CEO, CFO and Corporate Communications are authorised to speak to the media on behalf of Acme. Employees who receive a media enquiry must forward it to the press office within 1 hour and not comment."),
        ("2. Speaking Engagements and Publications", "External talks, articles and podcasts that mention Acme need approval from Corporate Communications at least 10 business days ahead, and Legal review when confidential topics are involved."),
    ]),
    dict(file="social_media_policy", id="POL-COM-002", title="Social Media Policy",
         dept="Corporate Communications", owner="Head of Corporate Communications", ver="3.0", date="2026-03-04", sections=[
        ("1. Personal Use", "Employees may use social media personally but must make clear that views are their own, must not share confidential information, customer data or unreleased plans, and must not harass or discriminate."),
        ("2. Official Accounts", "Only trained and approved employees may post on official Acme accounts. Employees must disclose their employment when endorsing Acme products."),
        ("3. Incidents", "A social media post that may damage the company or expose confidential information should be reported to Corporate Communications and Security at once."),
    ]),
    dict(file="delegation_of_authority_policy", id="POL-FIN-110", title="Delegation of Authority and Approval Matrix",
         dept="Global Finance", owner="Chief Financial Officer", ver="4.1", date="2026-07-01", roles=MGMT, sections=[
        ("1. Spending Approval Limits", "Manager: up to $10,000 USD. Director: up to $50,000 USD. VP: up to $250,000 USD. CFO: up to $1,000,000 USD. CEO: up to $5,000,000 USD. Anything above $5,000,000 USD requires Board approval."),
        ("2. Contract Signing", "Only authorised signatories in the matrix may sign contracts. Non-standard terms, unlimited liability, or exclusivity clauses need Legal approval regardless of value."),
        ("3. Segregation of Duties", "The person who requests a purchase cannot approve it or release the payment. Approvals cannot be delegated further than one level without written authorisation."),
    ]),
]
