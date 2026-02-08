# Zeid Data Security Playbooks — Google Workspace

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** Admin Audit Log, Login Audit, Drive Audit, Gmail Audit (assumed)

## Assumed log sources (make assumptions)
- Login audit log
- Admin audit log
- Drive audit log
- Gmail audit log

## SIEM assumptions (examples)
- Splunk: `index=google_workspace* sourcetype in (gws:login, gws:admin, gws:drive, gws:gmail)`
- Sentinel: `GWorkspaceActivityReports (connector) / custom tables`

## Playbooks in this folder
- PB01 Suspicious Authentication
- PB02 MFA Abuse and Push Fatigue
- PB03 Privileged Change or Admin Grant
- PB04 Malicious Process or EDR Detection
- PB05 Data Exfiltration and Large Transfers
- PB06 Command and Control Beaconing
- PB07 Lateral Movement
- PB08 Ransomware or Destructive Activity
- PB09 Insider Risk and Sensitive Access
- PB10 OAuth Token / API Key Misuse
