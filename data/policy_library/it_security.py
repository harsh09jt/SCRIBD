"""IT, information security and engineering policies."""

IT_POLICIES = [
    dict(file="acceptable_use_policy", id="POL-IT-030", title="Acceptable Use of Technology Policy",
         dept="Information Technology", owner="Chief Information Officer", ver="4.2", date="2026-04-27", sections=[
        ("1. Appropriate Use", "Company devices, email, networks and cloud services are provided for business use. Limited personal use is allowed if it does not affect work, security or the law."),
        ("2. Prohibited Activities", "Users must not install unlicensed or unapproved software, bypass security controls, access illegal or explicit content, share their accounts, or use personal email or storage for company data."),
        ("3. Monitoring", "Acme may monitor systems and communications for security and compliance to the extent permitted by local law. Users should have no expectation of privacy on company systems."),
    ]),
    dict(file="password_and_authentication_policy", id="POL-SEC-010", title="Password and Authentication Policy",
         dept="Cybersecurity", owner="Chief Information Security Officer (CISO)", ver="3.2", date="2026-05-19", sections=[
        ("1. Password Requirements", "Passwords must be at least 14 characters and must not be reused across the last 12 passwords. Passwords are only changed when compromise is suspected. Passwords must never be shared, written down or stored in plain text; use the approved password manager."),
        ("2. Multi-Factor Authentication", "MFA is mandatory for all employees for email, VPN, cloud consoles and any system that holds confidential data. Phishing-resistant methods (FIDO2 security keys) are required for administrators."),
        ("3. Account Lockout", "Accounts are locked after 5 failed sign-in attempts within 15 minutes and unlocked by the service desk after identity verification."),
    ]),
    dict(file="incident_response_policy", id="POL-SEC-011", title="Security Incident Response and Breach Notification Policy",
         dept="Cybersecurity", owner="Chief Information Security Officer (CISO)", ver="4.0", date="2026-06-22", sections=[
        ("1. Reporting an Incident", "Employees must report a suspected security incident (lost device, phishing click, unauthorised access) to the Security Operations Center immediately and no later than 1 hour after discovery, by email or the 24/7 hotline."),
        ("2. Severity and Response Times", "- Critical (SEV-1): response within 15 minutes, executive briefing within 1 hour.\n- High (SEV-2): response within 1 hour.\n- Medium (SEV-3): response within 4 hours.\n- Low (SEV-4): response within 1 business day."),
        ("3. Breach Notification", "If personal data is affected, Legal and the Data Protection Officer decide on regulator notification. Regulators are notified within 72 hours of becoming aware of a reportable breach and affected individuals without undue delay. A post-incident review is completed within 10 business days."),
    ]),
    dict(file="data_classification_and_handling_policy", id="POL-SEC-012", title="Data Classification and Handling Policy",
         dept="Cybersecurity", owner="Chief Information Security Officer (CISO)", ver="3.0", date="2026-02-03", sections=[
        ("1. Classification Levels", "Public, Internal, Confidential and Restricted. Customer personal data, financial results before release, and executive compensation are at least Confidential; encryption keys, credentials and M&A information are Restricted."),
        ("2. Handling Rules", "Confidential data must be encrypted in transit and at rest and shared only on a need-to-know basis. Restricted data may only be stored in approved systems and never sent by personal email or messaging apps."),
        ("3. Labelling and Disposal", "Documents must carry their classification label. Storage media are wiped to NIST 800-88 standards before disposal or reuse."),
    ]),
    dict(file="encryption_and_key_management_policy", id="POL-SEC-013", title="Encryption and Key Management Policy",
         dept="Cybersecurity", owner="Chief Information Security Officer (CISO)", ver="2.4", date="2026-03-16", sections=[
        ("1. Required Encryption", "Data at rest must use AES-256 and data in transit must use TLS 1.2 or higher. All laptops use full-disk encryption, and removable media must be encrypted."),
        ("2. Key Management", "Keys are generated and stored in a hardware security module or the approved cloud KMS. Keys are rotated at least every 12 months and immediately after suspected compromise. Access to keys is restricted to named administrators with dual control."),
    ]),
    dict(file="vulnerability_and_patch_management_policy", id="POL-SEC-014", title="Vulnerability and Patch Management Policy",
         dept="Cybersecurity", owner="Head of Security Engineering", ver="3.1", date="2026-07-14", sections=[
        ("1. Scanning", "Internet-facing systems are scanned weekly and internal systems monthly. Independent penetration tests are performed at least once a year."),
        ("2. Remediation Deadlines", "Critical vulnerabilities must be patched within 7 days, High within 30 days, Medium within 90 days. Actively exploited vulnerabilities must be mitigated within 48 hours."),
        ("3. Exceptions", "Any deadline extension requires a documented risk acceptance approved by the CISO for no more than 90 days."),
    ]),
    dict(file="change_management_policy", id="POL-IT-031", title="IT Change Management Policy",
         dept="Information Technology", owner="Head of IT Operations", ver="3.3", date="2026-04-06", sections=[
        ("1. Change Types", "Standard changes are pre-approved and low risk. Normal changes need peer review and Change Advisory Board (CAB) approval. Emergency changes may be applied immediately to restore service but must be reviewed within 2 business days."),
        ("2. Requirements", "Each change needs a description, risk assessment, test evidence, a rollback plan and a scheduled window. Production changes to Tier-1 systems are not permitted during freeze periods in the last 2 weeks of the fiscal quarter."),
    ]),
    dict(file="business_continuity_policy", id="POL-IT-032", title="Business Continuity and Crisis Recovery Policy",
         dept="Infrastructure & Information Security", owner="Head of Business Continuity", ver="2.8", date="2026-08-04", sections=[
        ("1. Business Impact Analysis", "Every department completes a business impact analysis every year and classifies processes as Critical (recovery in 4 hours), Essential (24 hours) or Standard (72 hours)."),
        ("2. Plans and Testing", "Each critical process has a documented continuity plan and a named owner. Plans are tested at least once a year with a tabletop exercise and results are reported to the Risk Committee. Technical recovery targets follow the Backup and Disaster Recovery Policy."),
        ("3. Crisis Communication", "The Crisis Management Team is activated by the COO. Employees are notified through the emergency notification system and must confirm their safety within 2 hours."),
    ]),
    dict(file="cloud_security_policy", id="POL-SEC-015", title="Cloud Security and Governance Policy",
         dept="Cybersecurity", owner="Head of Cloud Security", ver="2.6", date="2026-05-27", sections=[
        ("1. Approved Cloud Use", "Only approved cloud providers and services may hold Acme data. New cloud services need a security review before purchase. Data residency requirements in contracts and law must be respected."),
        ("2. Configuration Baselines", "Storage must not be public unless approved by the CISO. All cloud resources must be tagged with owner and data classification, use least-privilege IAM roles, and have logging turned on. Infrastructure is deployed through code with automated policy checks."),
    ]),
    dict(file="physical_security_and_visitor_policy", id="POL-SEC-016", title="Physical Security and Visitor Access Policy",
         dept="Corporate Security", owner="Head of Corporate Security", ver="2.3", date="2026-01-26", sections=[
        ("1. Access Badges", "Employees must wear their badge visibly on site, must not lend it, and must report loss immediately so it can be deactivated. Tailgating is prohibited."),
        ("2. Visitors", "Visitors are pre-registered by their host, show photo ID, wear a visitor badge and are escorted at all times. Visitor logs are kept for 12 months."),
        ("3. Secure Areas", "Data centres and server rooms need additional authorisation, with access reviewed every quarter. Photography is not allowed in secure areas."),
    ]),
    dict(file="artificial_intelligence_usage_policy", id="POL-SEC-017", title="Artificial Intelligence and Generative AI Usage Policy",
         dept="Cybersecurity & Legal", owner="Chief Information Security Officer (CISO)", ver="1.4", date="2026-08-18", sections=[
        ("1. Approved Tools", "Only AI tools approved by IT Security may be used with company information. Confidential and Restricted data, customer personal data and source code must never be entered into public generative AI chatbots such as ChatGPT or Gemini, or any other public AI service."),
        ("2. Human Oversight", "AI output must be reviewed by a person before it is used for decisions about customers, employees or financial reporting. Employees remain accountable for content they produce with AI and must check it for accuracy and bias."),
        ("3. New AI Use Cases", "Any new AI system that affects customers or employees needs a risk assessment by Legal, Security and Data Privacy before launch and is registered in the AI inventory."),
    ]),
    dict(file="secure_software_development_policy", id="POL-ENG-040", title="Secure Software Development Lifecycle Policy",
         dept="Engineering", owner="VP of Engineering", ver="3.0", date="2026-03-31", sections=[
        ("1. Code Review and Testing", "All code changes need at least 1 peer review before merge. Automated unit tests must pass and code coverage for new code must be at least 80%."),
        ("2. Security Checks", "Static analysis, dependency scanning and secret scanning run on every pull request. Builds with critical findings are blocked from release. Threat modelling is required for new systems that handle customer data."),
        ("3. Secrets and Releases", "Secrets must be stored in the approved vault and never committed to code. Production releases are made only through the approved CI/CD pipeline."),
    ]),
    dict(file="logging_and_monitoring_policy", id="POL-SEC-018", title="Security Logging and Monitoring Policy",
         dept="Cybersecurity", owner="Head of Security Operations", ver="2.2", date="2026-06-08", sections=[
        ("1. What Is Logged", "Authentication events, privileged actions, access to confidential data, network security events and configuration changes are logged and sent to the central SIEM."),
        ("2. Retention and Review", "Security logs are retained for 13 months (12 months searchable). Alerts are triaged by the SOC 24/7, and privileged access logs are reviewed monthly. Logs are protected from alteration."),
    ]),
]
