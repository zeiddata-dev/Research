<!-- ZEID DATA README HERO START -->
![Zeid Data cisco banner](../../../assets/banners/readme/content.png)

<p align="center">
  <a href="../../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../.."><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![content](https://img.shields.io/badge/content-334155?style=flat-square) ![vendor-content](https://img.shields.io/badge/vendor%20content-334155?style=flat-square) ![governance](https://img.shields.io/badge/governance-6F42C1?style=flat-square) ![evidence-assets](https://img.shields.io/badge/evidence%20assets-334155?style=flat-square) ![cisco](https://img.shields.io/badge/cisco-334155?style=flat-square) ![security-operations](https://img.shields.io/badge/security%20operations-334155?style=flat-square) ![network-security](https://img.shields.io/badge/network%20security-334155?style=flat-square) ![vendors](https://img.shields.io/badge/vendors-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data Cisco Free Content Pack

Evidence-first detection content for Cisco telemetry. This folder is designed to help you turn Cisco logs into repeatable, audit-ready security detections and simple reporting outputs.

## What this is
A practical starter kit you can deploy quickly using logs you already have from Cisco security and networking products. The goal is to reduce time-to-detection and standardize evidence capture.

## What’s included (general)
This pack is intentionally modular. Content may include some or all of the following, depending on what telemetry you have enabled:

- Detection logic (queries, rules, and filters) for suspicious network behavior
- Reference allowlist/denylist patterns and tuning notes
- Field mapping notes for common Cisco log schemas
- Validation checklist and test cases
- Optional dashboards or reporting templates (platform-dependent)

## Supported Cisco telemetry (common sources)
You can use this pack with one or more of these data sources:

- Cisco Secure Firewall / Firepower (FTD) connection events
- ASA firewall logs (if still in use)
- Cisco Umbrella DNS logs
- Cisco Secure Endpoint (AMP) event telemetry
- Cisco Secure Network Analytics (Stealthwatch) flow/behavior signals
- Cisco Duo authentication logs
- Cisco Email Security / Web Security (where applicable)
- NetFlow/IPFIX exports from Cisco network devices (if collected)

If you only have one source (for example DNS from Umbrella), you can still get value. The detections are written to degrade gracefully when certain fields are missing.

## Use cases this pack targets
Examples of the kinds of behaviors you can detect with Cisco logs:

- Unusual outbound destinations (new domains, new ASNs, rare countries)
- Suspicious DNS patterns (DGA-like, newly registered domains, high NXDOMAIN rates)
- TLS/HTTPS anomalies (rare SNI, unusual JA3/JA4 when available via your stack)
- Beaconing patterns and periodic outbound traffic
- Authentication anomalies (impossible travel, new device, repeated failures)
- Endpoint execution or lateral movement signals (if Secure Endpoint is present)

