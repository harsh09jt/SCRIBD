# Third-Party Vendor Management and Risk Governance Policy
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
