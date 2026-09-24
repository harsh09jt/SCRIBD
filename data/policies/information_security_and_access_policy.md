# Information Security and Access Control Policy
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
