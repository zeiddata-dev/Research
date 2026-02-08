# Zeid Data Security Playbooks

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

This package contains vendor-aligned SOC playbooks. Each vendor folder includes **10 incident response playbooks**
with **assumed log sources** and **example SIEM pivots**.

## Assumptions (log sources)
Because environments vary, each vendor playbook makes reasonable assumptions about common telemetry, for example:
- Identity logs (SSO/IdP sign-ins, MFA events, admin changes)
- Endpoint telemetry (EDR detections, process/network/file events) where applicable
- Network telemetry (firewall/proxy/DNS) where applicable
- Cloud audit logs (CloudTrail/GuardDuty, Workspace audits, etc.)
- Data platform audit logs (Snowflake/Databricks audit sources)

## Vendor folders
- **01_Cisco** — Cisco Secure Firewall/FTD, Umbrella, Secure Email (assumed), Secure Endpoint (assumed)
- **02_CrowdStrike** — Falcon (EDR), Falcon Identity (assumed), Falcon LogScale (optional)
- **03_Microsoft** — Microsoft Sentinel + Microsoft Defender (Endpoint/Identity/Office 365)
- **04_Splunk** — Splunk Enterprise Security (ES) + core indexes
- **05_Palo_Alto_Networks** — PAN-OS + Prisma Access/GlobalProtect + WildFire (assumed)
- **06_AWS** — CloudTrail, GuardDuty, Security Hub, VPC Flow Logs, S3 Access Logs (assumed)
- **07_Okta** — Okta System Log + Risk Events (assumed)
- **08_Google_Workspace** — Admin Audit Log, Login Audit, Drive Audit, Gmail Audit (assumed)
- **09_Snowflake** — ACCOUNT_USAGE views, ACCESS_HISTORY (if enabled), Login History, Query History
- **10_Databricks** — Workspace audit logs (Delivery to S3/ADLS/Log Analytics), cluster & job events

## Conventions
- Playbooks are Markdown files: `PBxx_<name>.md`
- Each playbook includes: purpose, triggers, triage, containment, eradication, recovery, evidence, queries, post-incident
- Example queries are placeholders; scope them to approved indexes/tables in your environment.
