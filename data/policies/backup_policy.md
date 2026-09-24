# Enterprise Backup and Disaster Recovery Policy
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
