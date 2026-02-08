# Zeid Data Security Playbooks — Microsoft

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** Microsoft Sentinel + Microsoft Defender (Endpoint/Identity/Office 365)

## Assumed log sources (make assumptions)
- Microsoft Sentinel (Analytics + Incidents)
- Microsoft Defender for Endpoint (MDE)
- Entra ID (Azure AD) sign-in + audit logs
- M365 Unified audit log

## SIEM assumptions (examples)
- Splunk: ``
- Sentinel: `SigninLogs, AuditLogs, SecurityAlert, SecurityIncident, DeviceProcessEvents, DeviceNetworkEvents`

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
