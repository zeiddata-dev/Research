# Zeid Data Security Playbooks — Cisco

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** Cisco Secure Firewall/FTD, Umbrella, Secure Email (assumed), Secure Endpoint (assumed)

## Assumed log sources (make assumptions)
- Cisco Secure Firewall/FTD: connection/threat logs
- Cisco Umbrella: DNS queries, security events
- Cisco Secure Email (assumed): message tracking, detections
- NetFlow (optional): network flows

## SIEM assumptions (examples)
- Splunk: `index=cisco* sourcetype in (cisco:asa, cisco:ftd, cisco:umbrella, netflow)`
- Sentinel: `CommonSecurityLog, DnsEvents (via connector), Syslog (if used)`

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
