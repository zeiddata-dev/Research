<!-- ZEID DATA README HERO START -->
<p align="center">
  <img src="../assets/banners/readme/templates.svg" alt="Templates" width="100%">
</p>

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../content"><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="https://zeiddata.com"><img alt="Website" src="https://img.shields.io/badge/Website-00B8A9?style=for-the-badge&logo=googlechrome&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data - Security Templates (Quick Guide)

This folder contains **ready-to-copy templates** you can use to standardize security work across teams—without reinventing the wheel each time.

## What’s in here
Common template types you may find:
- **Detection templates** (what to detect, data sources, logic, tuning)
- **Incident response templates** (triage steps, containment, evidence checklist)
- **Threat hunting templates** (hypothesis, queries, expected signals)
- **Risk & compliance templates** (controls, evidence, audit notes)
- **Change management templates** (what changed, why, impact, approvals)
- **Runbooks / playbooks** (step-by-step operational procedures)

## How to use these templates
1. **Copy** the closest template to your use case  
2. **Fill in** the environment-specific fields (vendor, log source, owner, severity)  
3. **Test** in a non-production or limited-scope context  
4. **Document** outcomes (false positives, gaps, tuning decisions)  
5. **Promote** to production with approvals and tracking

## Minimum fields to complete (most templates)
- **Owner / team**
- **Purpose** (what problem this solves)
- **Data sources** (DNS, EDR, firewall, SIEM, cloud logs, etc.)
- **Detection / procedure** (logic, steps, queries)
- **Severity + triage guidance**
- **Evidence to collect** (fields, screenshots, exports)
- **References** (tickets, policies, threat intel)

## Good habits
- Prefer **clear, repeatable steps** over long narratives
- Keep detections **measurable** (what signals, what threshold, what timeframe)
- Track changes with a **version + changelog**
- Design for **audit-ready outputs** (who, what, when, why, evidence)

## Disclaimer
These templates are **starting points**. Validate with your policies, legal/privacy requirements, and your production environment before use.
