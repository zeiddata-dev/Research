# Zeid Data Security Playbooks — CrowdStrike

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** Falcon (EDR), Falcon Identity (assumed), Falcon LogScale (optional)

## Assumed log sources (make assumptions)
- Falcon detections (DetectionSummaryEvent)
- Falcon telemetry (ProcessRollup2, NetworkConnectIP4, DNSRequest)
- Identity events (assumed): suspicious auth/AD indicators

## SIEM assumptions (examples)
- Splunk: `index=crowdstrike* sourcetype=crowdstrike:*`
- Sentinel: `Custom table via connector (assumed)`

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
