# Zeid Data Security Playbooks — Snowflake

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** ACCOUNT_USAGE views, ACCESS_HISTORY (if enabled), Login History, Query History

## Assumed log sources (make assumptions)
- LOGIN_HISTORY
- QUERY_HISTORY
- ACCESS_HISTORY (if enabled)
- ACCOUNT_USAGE views

## SIEM assumptions (examples)
- Splunk: `index=snowflake* sourcetype=snowflake:*`
- Sentinel: `Custom tables via Event Hub/connector (assumed)`

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
