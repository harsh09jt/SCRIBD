# Encryption and Key Management Policy
Document ID: POL-SEC-013
Version: 2.4
Last Updated: 2026-03-16
Department: Cybersecurity
Owner: Chief Information Security Officer (CISO)
Access Roles: employee, manager, hr, legal, admin

## 1. Required Encryption
Data at rest must use AES-256 and data in transit must use TLS 1.2 or higher. All laptops use full-disk encryption, and removable media must be encrypted.

## 2. Key Management
Keys are generated and stored in a hardware security module or the approved cloud KMS. Keys are rotated at least every 12 months and immediately after suspected compromise. Access to keys is restricted to named administrators with dual control.
