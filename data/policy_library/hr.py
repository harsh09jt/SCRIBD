"""People & HR policies."""

ALL = None  # None => default access (all roles)
MGMT = ["manager", "hr", "legal", "admin"]

HR_POLICIES = [
    dict(file="equal_opportunity_and_diversity_policy", id="POL-HR-110", title="Equal Opportunity, Diversity and Inclusion Policy",
         dept="Human Resources", owner="Chief People Officer", ver="3.0", date="2026-04-02", sections=[
        ("1. Commitment and Scope", "Acme provides equal employment opportunity without regard to race, color, religion, gender, gender identity, sexual orientation, age, national origin, disability, marital or veteran status, or any other legally protected characteristic.\nThis applies to recruiting, pay, promotion, training, discipline and termination, and covers employees, contractors and interns."),
        ("2. Fair Hiring and Advancement", "Every role uses structured interviews. Director-level and above hiring requires a diverse interview panel of at least 3 members.\nPay and promotion outcomes are reviewed annually for gaps by gender and ethnicity. Any unexplained gap above 2% must be remediated in the next compensation cycle."),
        ("3. Employee Resource Groups", "Employees may form an Employee Resource Group (ERG) with at least 25 members and an executive sponsor.\nEach ERG receives an annual budget of up to $10,000 USD and 4 paid hours per member per month for approved activities."),
    ]),
    dict(file="anti_harassment_and_posh_policy", id="POL-HR-111", title="Anti-Harassment and Sexual Harassment Prevention (POSH) Policy",
         dept="Human Resources & Legal", owner="Chief People Officer", ver="4.0", date="2026-02-18", sections=[
        ("1. Prohibited Conduct", "Harassment, sexual harassment, bullying, stalking, intimidation and retaliation are prohibited in offices, remote settings, client sites, company events and on any digital channel.\nUnwelcome physical contact, sexual remarks, offensive jokes, displaying explicit material and abuse of authority are all covered."),
        ("2. Reporting and the Internal Complaints Committee", "Complaints may be raised with an HR Business Partner, the Internal Complaints Committee (ICC) or the confidential ethics hotline, ideally within 3 months of the incident.\nThe ICC is chaired by a senior woman leader and includes an external member. Complaints are acknowledged within 2 business days and inquiries are completed within 90 days."),
        ("3. Interim Protection, Outcomes and Training", "Interim measures such as a change of reporting line or up to 30 days of paid leave may be offered to the complainant. Outcomes range from a written warning to termination.\nRetaliation is itself grounds for dismissal. All employees complete POSH training within 30 days of joining and every year after."),
    ]),
    dict(file="recruitment_and_hiring_policy", id="POL-HR-112", title="Recruitment, Hiring and Background Verification Policy",
         dept="Talent Acquisition", owner="Talent Acquisition Lead", ver="3.2", date="2026-03-12", sections=[
        ("1. Requisition and Approval", "A role may be opened only when headcount is approved in the workforce plan. Requisitions require sign-off from the hiring manager, the Finance Business Partner and the function VP. Director-level and above roles also need Chief People Officer approval."),
        ("2. Selection Process", "Candidates go through at least 3 interview rounds, including one behavioural round. Interviewers submit scorecards within 48 hours. Offers are issued within 5 business days of the final interview and must stay within the approved salary band."),
        ("3. Background Verification", "Offers are contingent on identity, education, employment history for the last 7 years and criminal record checks through the approved vendor, completed within 21 days of joining.\nAdverse findings are reviewed by HR and Legal before any decision, and the candidate has 5 business days to respond."),
    ]),
    dict(file="compensation_and_bonus_policy", id="POL-HR-114", title="Compensation, Salary Bands and Variable Pay Policy",
         dept="Total Rewards", owner="Total Rewards Director", ver="4.4", date="2026-06-30", sections=[
        ("1. Salary Bands", "Each job level (L1 to L10) has a salary band with minimum, midpoint and maximum, benchmarked every year against the market 50th to 65th percentile.\nOffers are made between 90% and 110% of the midpoint. Offers above 110% need Compensation Committee approval."),
        ("2. Merit Increase and Annual Bonus", "Merit increases take effect on April 1. Rating 4.5 and above: 8% to 10%. Rating 3.5 to 4.4: 4% to 6%. Rating 3.0 to 3.4: 0% to 3%. Below 3.0: not eligible.\nAnnual bonus targets are 10% of base for L1-L4, 15% for L5-L6 and 25% for L7 and above, scaled by a company performance multiplier of 0% to 150% and paid in March."),
        ("3. Payroll Corrections and Pay Transparency", "Overpayments are recovered over no more than 3 months. Underpayments are corrected within 5 business days of confirmation.\nEmployees are free to discuss their own pay, and salary ranges are published in job postings wherever local law requires."),
    ]),
    dict(file="disciplinary_action_policy", id="POL-HR-115", title="Disciplinary Action and Progressive Discipline Policy",
         dept="Employee Relations", owner="Head of Employee Relations", ver="2.6", date="2026-05-08", roles=MGMT, sections=[
        ("1. Progressive Steps", "Discipline normally progresses from a verbal warning, to a written warning, to a final written warning with a 60-day improvement plan, and then to termination.\nSerious misconduct such as theft, violence, harassment, fraud or a deliberate data breach may skip steps."),
        ("2. Investigation and Due Process", "HR opens a case within 2 business days. The employee receives the allegations in writing, has 5 business days to respond and may bring a colleague to meetings.\nA decision is made within 15 business days. Paid suspension of up to 10 days is allowed during an investigation."),
        ("3. Records and Appeals", "Warnings stay on file for 24 months. An employee may appeal to the next-level manager and HR within 7 days, and the appeal decision is final.\nManagers must consult HR before taking any disciplinary action."),
    ]),
    dict(file="annual_sick_and_casual_leave_policy", id="POL-HR-116", title="Annual, Sick, Casual and Statutory Leave Policy",
         dept="Human Resources", owner="Head of HR Operations", ver="4.0", date="2026-01-20", sections=[
        ("1. Leave Entitlements", "- Annual leave: 25 days per year, accruing 2.08 days a month. Up to 10 days may be carried forward and they lapse on March 31.\n- Sick leave: 12 days per year. A medical certificate is required after 3 consecutive days.\n- Casual leave: 6 days per year.\n- Public holidays follow the regional calendar, with a minimum of 10 days."),
        ("2. Bereavement, Jury Duty and Other Leave", "Bereavement leave is 5 paid days for immediate family and 3 days for extended family. Marriage leave is 5 days. Jury duty and court witness time are paid as required by law."),
        ("3. Applying and Encashment", "Apply in the HR portal at least 5 business days ahead for leave longer than 3 days. Managers respond within 2 business days.\nUp to 15 unused annual leave days are encashed at separation at the basic daily rate."),
    ]),
    dict(file="sabbatical_and_unpaid_leave_policy", id="POL-HR-117", title="Sabbatical and Extended Unpaid Leave Policy",
         dept="Human Resources", owner="Total Rewards Director", ver="1.8", date="2026-03-25", sections=[
        ("1. Sabbatical Eligibility", "Employees with 7 years of continuous service and a rating of 3.5 or higher in the last 2 cycles may take up to 8 weeks of sabbatical at 100% of base pay. Combined with annual leave, the total break may not exceed 12 weeks."),
        ("2. Extended Unpaid Leave", "Up to 6 months of unpaid leave may be granted for education, caregiving or personal circumstances with VP approval.\nHealth benefits continue for the first 90 days if the employee pays their own contribution."),
        ("3. Return to Work", "Employees return to the same or an equivalent role and must confirm their return date 30 days in advance. Sabbatical pay is repayable pro rata if the employee resigns within 6 months of returning."),
    ]),
    dict(file="working_hours_and_attendance_policy", id="POL-HR-118", title="Working Hours, Timekeeping and Attendance Policy",
         dept="HR Operations", owner="Head of HR Operations", ver="3.3", date="2026-02-05", sections=[
        ("1. Standard Hours", "The standard work week is 40 hours (8 hours a day) with core collaboration hours from 10:00 to 16:00 local time. A 30-minute unpaid break is taken after 5 hours of work, and employees must have at least 11 hours of rest between shifts."),
        ("2. Overtime", "Overtime for non-exempt employees must be approved in advance by the manager. It is paid at 1.5x the hourly rate on weekdays and 2x on weekends and public holidays."),
        ("3. Attendance", "Three unexplained absences in a quarter trigger an HR review. Employees must inform their manager before the start of the working day when they will be absent or late."),
    ]),
    dict(file="resignation_and_notice_period_policy", id="POL-HR-119", title="Resignation, Notice Period and Exit Clearance Policy",
         dept="People Operations", owner="Head of People Operations", ver="2.9", date="2026-06-14", sections=[
        ("1. Notice Periods", "Notice is 30 days during probation and for levels L1 to L3, 60 days for L4 to L6, and 90 days for L7 and above.\nA notice period may be shortened or bought out (pay in lieu at 50% of the remaining notice pay) with manager and HR approval."),
        ("2. Submitting a Resignation", "Resignations are submitted in writing to the manager and HR. HR acknowledges within 2 business days and schedules an exit interview in the final week."),
        ("3. Clearance and Final Settlement", "Employees hand over a knowledge-transfer plan in the first 5 days of notice and return the laptop and badge on the last working day, when all system access is revoked.\nFull and final settlement is paid within 45 days of the last working day."),
    ]),
    dict(file="learning_and_development_policy", id="POL-HR-120", title="Learning, Development and Tuition Reimbursement Policy",
         dept="Learning & Development", owner="Head of Learning & Development", ver="2.4", date="2026-01-30", sections=[
        ("1. Learning Budget", "Every full-time employee receives $2,500 USD in annual learning credits for courses, conferences and approved certifications. Certifications are reimbursed in full on passing."),
        ("2. Tuition Reimbursement", "Degree programs relevant to the role are reimbursed up to $10,000 USD a year: 75% for grades A or B. Reimbursed amounts must be repaid in full if the employee leaves within 12 months, and 50% within 24 months."),
        ("3. Mandatory Training", "All employees complete 40 hours of learning a year. Compliance modules (code of conduct, security, POSH) must be completed within 30 days of assignment."),
    ]),
    dict(file="employee_referral_program_policy", id="POL-HR-121", title="Employee Referral Program Policy",
         dept="Talent Acquisition", owner="Talent Acquisition Lead", ver="2.0", date="2026-04-15", sections=[
        ("1. Referral Bonus", "The referral bonus is $1,500 USD for levels L1-L4, $3,000 USD for L5-L7 and $5,000 USD for Director and above. It is paid 50% when the hire joins and 50% after the hire completes 6 months."),
        ("2. Eligibility Rules", "Referrals must be submitted through the portal before the candidate applies. HR, Talent Acquisition staff and the hiring manager are not eligible. If two employees refer the same candidate, the earliest submission wins."),
    ]),
    dict(file="relocation_and_global_mobility_policy", id="POL-HR-122", title="Relocation and Global Mobility Policy",
         dept="Global Mobility", owner="Head of Global Mobility", ver="2.2", date="2026-05-20", sections=[
        ("1. Eligibility and Allowances", "Business-initiated moves of more than 50 km for employees with at least 12 months of tenure qualify. The relocation lump sum is $5,000 USD for single employees and $8,000 USD with family, plus up to 30 days of temporary housing."),
        ("2. Shipping, Visa and Tax", "Household shipping is covered up to 3 cubic metres (single) or 10 cubic metres (family). Acme sponsors visa and immigration costs. International assignments longer than 6 months receive tax equalisation."),
        ("3. Repayment", "Relocation benefits must be repaid in full if the employee resigns within 24 months of the move."),
    ]),
    dict(file="dress_code_policy", id="POL-HR-123", title="Workplace Dress Code and Professional Appearance Policy",
         dept="Human Resources", owner="Head of HR Operations", ver="1.5", date="2025-11-10", sections=[
        ("1. General Standard", "Business casual is the default. Client-facing meetings require business professional attire. Casual dress is allowed on Fridays and on remote days when not on video with clients."),
        ("2. Safety and Cultural Considerations", "Protective footwear and gear are mandatory in data centres and labs. Religious and cultural attire is respected and reasonable accommodation is provided."),
    ]),
    dict(file="employee_grievance_redressal_policy", id="POL-HR-124", title="Employee Grievance Redressal Policy",
         dept="Employee Relations", owner="Head of Employee Relations", ver="2.5", date="2026-03-03", sections=[
        ("1. Three-Level Process", "Level 1: raise the grievance with your manager, who responds within 5 business days. Level 2: escalate to your HR Business Partner, who resolves within 10 business days. Level 3: the Grievance Committee decides within 15 business days and its decision is final."),
        ("2. Confidentiality and Non-Retaliation", "Grievances can be submitted anonymously through the ethics portal. Retaliation against anyone raising a grievance in good faith is prohibited. Records are retained for 5 years."),
    ]),
    dict(file="employee_wellbeing_and_eap_policy", id="POL-HR-125", title="Employee Wellbeing, Mental Health and EAP Policy",
         dept="Benefits", owner="Total Rewards Director", ver="2.1", date="2026-07-08", sections=[
        ("1. Employee Assistance Program (EAP)", "The EAP provides free, confidential counselling: 8 sessions per issue per year for employees and dependents, with a 24/7 helpline. Employer access to who uses the EAP is not permitted."),
        ("2. Wellbeing Benefits", "Employees receive a $1,200 USD annual wellness allowance and 3 mental-health days a year that do not need a medical certificate."),
        ("3. Manager Responsibilities", "Managers complete mental-health awareness training, agree reasonable return-to-work adjustments with HR and escalate any immediate risk to the on-call clinician or emergency services."),
    ]),
    dict(file="disability_and_reasonable_accommodation_policy", id="POL-HR-126", title="Disability and Reasonable Accommodation Policy",
         dept="Human Resources & Legal", owner="Head of Employee Relations", ver="2.2", date="2026-02-27", sections=[
        ("1. Requesting an Accommodation", "Employees or candidates may request an accommodation from HR at any time. HR starts an interactive discussion within 5 business days and gives a decision within 15 business days."),
        ("2. Types of Accommodation", "Examples include ergonomic or assistive equipment, flexible schedules, remote work, accessible workspaces and adjusted job duties. A denial must be reviewed by Legal."),
        ("3. Confidentiality", "Medical information is kept confidential and stored separately from the personnel file."),
    ]),
    dict(file="equity_and_stock_option_policy", id="POL-HR-127", title="Equity, Stock Options and RSU Plan Policy",
         dept="Total Rewards", owner="Total Rewards Director", ver="3.1", date="2026-05-29", sections=[
        ("1. Grants and Vesting", "Equity grants are made to L5 and above and to designated critical talent. Grants vest over 4 years with a 1-year cliff (25%), then monthly for the remaining 36 months. RSUs settle quarterly."),
        ("2. Leavers", "Unvested grants are forfeited on separation. Vested stock options remain exercisable for 90 days after the last working day."),
        ("3. Trading Restrictions", "Sales of vested shares are subject to the trading windows and pre-clearance rules in the Insider Trading and Securities Dealing Policy."),
    ]),
    dict(file="retirement_and_provident_fund_policy", id="POL-HR-128", title="Retirement Savings and Provident Fund Policy",
         dept="Benefits", owner="Total Rewards Director", ver="3.5", date="2026-01-12", sections=[
        ("1. Enrolment and Employer Match", "Employees are auto-enrolled at 3% of base pay after 60 days and may change their rate every quarter. Acme matches contributions up to 5% of eligible base pay."),
        ("2. Vesting", "Employee contributions vest immediately. The employer match vests 33% a year over 3 years."),
        ("3. Gratuity", "Employees with 5 or more years of continuous service receive gratuity on retirement, resignation or death under the Group Gratuity Plan."),
    ]),
    dict(file="internal_mobility_and_promotion_policy", id="POL-HR-129", title="Internal Mobility and Promotion Policy",
         dept="Talent Management", owner="Head of Talent Management", ver="2.3", date="2026-06-02", sections=[
        ("1. Internal Transfers", "Employees may apply for internal roles after 12 months in their current role with a rating of 3.5 or higher. The current manager is informed but cannot block a transfer beyond 30 days. Transfers take effect within 60 days."),
        ("2. Promotions", "Promotions are decided in the June and December calibration cycles. A candidate must show sustained performance at the next level for 2 consecutive cycles and be approved by the calibration panel."),
    ]),
    dict(file="volunteer_and_community_investment_policy", id="POL-CSR-001", title="Volunteer Time Off and Community Investment Policy",
         dept="Corporate Social Responsibility", owner="Head of CSR", ver="1.7", date="2026-04-22", sections=[
        ("1. Volunteer Time Off", "Each employee receives 16 paid volunteer hours per year for registered non-profit organisations. Hours are logged in the HR portal."),
        ("2. Donation Matching", "Acme matches employee donations to eligible charities 1:1 up to $1,000 USD per employee per year. Political and religious organisations are not eligible."),
    ]),
    dict(file="personnel_records_policy", id="POL-HR-130", title="Employee Personnel Records and Privacy Policy",
         dept="Human Resources", owner="Head of HR Operations", ver="2.0", date="2026-03-18", sections=[
        ("1. What Is Kept", "The personnel file contains contracts, role history, performance reviews and payroll details. Medical and disability records are stored separately with restricted access."),
        ("2. Access and Retention", "Employees may request a copy of their own file and receive it within 10 business days. Files are kept for 7 years after separation and then securely destroyed."),
    ]),
    dict(file="onboarding_and_probation_policy", id="POL-HR-131", title="Onboarding and Probation Policy",
         dept="Human Resources", owner="Head of People Operations", ver="2.4", date="2026-02-11", sections=[
        ("1. Onboarding", "New hires receive laptop and access on day 1, complete a 5-day orientation and agree a 30/60/90-day plan with their manager."),
        ("2. Probation", "Probation lasts 6 months (3 months for interns and contractors). It may be extended once by up to 3 months. Confirmation is issued in writing by HR after a manager review."),
    ]),
]
