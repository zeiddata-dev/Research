<!-- ZEID DATA README HERO START -->
![Zeid Data content banner](../assets/banners/readme/content.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="."><img alt="Content" src="https://img.shields.io/badge/Content-00B8A9?style=for-the-badge&logo=bookstack&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../projects"><img alt="Projects" src="https://img.shields.io/badge/Projects-7B61FF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../tools/scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../workbooks"><img alt="Workbooks" src="https://img.shields.io/badge/Workbooks-00C7E5?style=for-the-badge&logo=github&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

<!-- ZEID DATA TAGS START -->
### Tags

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![content](https://img.shields.io/badge/content-334155?style=flat-square) ![vendor-content](https://img.shields.io/badge/vendor%20content-334155?style=flat-square) ![governance](https://img.shields.io/badge/governance-6F42C1?style=flat-square) ![evidence-assets](https://img.shields.io/badge/evidence%20assets-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data Network Security Content

This folder contains vendor-organized network security content: hardening guidance, reference configurations, detection ideas, runbooks, validation steps, and audit-ready evidence material.

The purpose is practical reuse. A reader should be able to find a vendor, understand the control or workflow, apply it safely in a controlled environment, and capture proof that it worked.

## What this folder is for

Use `content/` for public-safe material such as:

- Baseline hardening notes.
- Reference configurations with comments and assumptions.
- Validation commands and expected evidence.
- Detection and monitoring ideas.
- Operational runbooks, rollback notes, and break-glass guidance.
- Audit-ready evidence checklists.
- Vendor field guides and implementation notes.

## Minimum vendor content structure

Recommended layout:

```text
content/
  VendorName/
    README.md
    hardening/
    detections/
    runbooks/
    evidence/
    references.md
```

A vendor folder does not need every subfolder on day one. Add structure when there is actual content to place there.

## Quality bar

Every vendor note should include:

- Product or platform scope.
- Version assumptions, if known.
- Required permissions.
- Exact setting, command, policy, query, or workflow.
- Validation method.
- Evidence to capture.
- Known risk, rollback, or operational impact.
- Public references when available.

## Public-safe rules

Do not commit private customer configs, tokens, secrets, tenant URLs, internal IPs, private screenshots, or sensitive logs. Use sanitized examples and clearly mark placeholders.

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`detections/`](../detections)
- [`templates/`](../templates)
