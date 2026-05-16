<!-- ZEID DATA README HERO START -->
![Zeid Data workbooks banner](../../../../assets/banners/readme/workbooks.png)

<p align="center">
  <a href="../../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../.."><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![workbooks](https://img.shields.io/badge/workbooks-00C7E5?style=flat-square) ![dashboards](https://img.shields.io/badge/dashboards-334155?style=flat-square) ![visual-analytics](https://img.shields.io/badge/visual%20analytics-334155?style=flat-square) ![security-operations](https://img.shields.io/badge/security%20operations-334155?style=flat-square) ![playbooks](https://img.shields.io/badge/playbooks-334155?style=flat-square) ![incident-response](https://img.shields.io/badge/incident%20response-334155?style=flat-square) ![security-operations-playbooks](https://img.shields.io/badge/security%20operations%20playbooks-334155?style=flat-square) ![okta](https://img.shields.io/badge/okta-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

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
