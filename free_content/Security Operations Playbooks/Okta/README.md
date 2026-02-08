# Zeid Data Security Playbooks — Okta

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** Okta System Log + Risk Events (assumed)

## Assumed log sources (make assumptions)
- Okta System Log (authentication, policy, admin events)
- Okta risk events (assumed)

## SIEM assumptions (examples)
- Splunk: `index=okta* sourcetype=okta:system`
- Sentinel: `Okta_CL (custom) or built-in connector tables`

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
