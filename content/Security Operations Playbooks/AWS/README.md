# Zeid Data Security Playbooks — AWS

**Authorized SOC use only. Use only on systems/data you own or have explicit permission to analyze.**

**Assumed vendor stack:** CloudTrail, GuardDuty, Security Hub, VPC Flow Logs, S3 Access Logs (assumed)

## Assumed log sources (make assumptions)
- CloudTrail (management + data events if enabled)
- GuardDuty findings
- Security Hub findings
- VPC Flow Logs
- S3 server access logs (assumed)

## SIEM assumptions (examples)
- Splunk: `index=aws* sourcetype in (aws:cloudtrail, aws:guardduty, aws:securityhub, aws:vpcflow)`
- Sentinel: `AWSCloudTrail, AWSGuardDuty, AWSVPCFlow (via connectors/custom)`

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
