# Engineering On-Call and Incident Standby Policy
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
