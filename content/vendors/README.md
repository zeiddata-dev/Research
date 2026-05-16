<!-- ZEID DATA README HERO START -->
<p align="center">
  <img src="../../assets/banners/readme/content.png" alt="Zeid Data content banner" width="100%">
</p>

<p align="center">
  <a href="../../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href=".."><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data — Splunk Content (Free Drops)

This repo (or folder) is where Zeid Data publishes **Splunk-ready** security content: dashboards, detections, saved searches, lookups, and installable app artifacts you can ship into a SOC and defend in an audit.

No paywall. Just payload.

---

## What you’ll find here

Depending on the drop, content may include:

- **Dashboards**
  - Classic SimpleXML dashboards
  - Dashboard Studio JSON dashboards
- **Detections**
  - SPL searches (triage + hunting)
  - Correlation-style patterns (where applicable)
  - Tuning notes + false-positive guidance
- **Operational building blocks**
  - Macros (to make deployments portable)
  - Lookups (CSV) + field mappings
  - Knowledge objects (eventtypes, tags, calculated fields)
- **Packaging**
  - Standalone `.conf` snippets **or**
  - Full Splunk app folders that can be installed under `etc/apps/`

> Everything is designed to be: practical, reproducible, and explainable to engineers *and* auditors.

---

## Repo layout (typical)

Your structure may vary by drop, but most Splunk content follows a pattern like:

