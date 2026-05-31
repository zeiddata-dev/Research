<!-- ZEID DATA README HERO START -->
![Zeid Data research banner](../assets/banners/readme/research.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../tools/scripts"><img alt="Scripts" src="https://img.shields.io/badge/Scripts-2EA043?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../templates"><img alt="Templates" src="https://img.shields.io/badge/Templates-334155?style=for-the-badge&logo=markdown&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data Research

This folder is for public-safe research notes, malware analysis, CVE notes, threat models, defensive write-ups, and longer-form technical analysis.

The goal is practical research that can be reviewed, cited, and turned into better detections, safer configurations, stronger runbooks, or clearer dashboards.

## What belongs here

- Malware family notes focused on behavior, detections, mitigations, and safe analysis.
- CVE notes focused on impact, affected surfaces, defensive validation, and remediation.
- Threat models for tools, platforms, workflows, and AI/data systems.
- White papers and field notes.
- Public-safe incident pattern analysis using sanitized or synthetic examples.

## What each research item should include

| Section | Purpose |
|---|---|
| Summary | Short explanation of the topic and why it matters. |
| Scope | What is covered, what is excluded, and what evidence is available. |
| Evidence | Sources, artifacts, references, telemetry, or sample data used. |
| Analysis | Findings, hypotheses, confidence level, and limits. |
| Defensive value | Detections, mitigations, hardening steps, validation commands, or dashboards. |
| References | Public sources or repo-local artifacts. |
| Last reviewed | Date and status so stale research can be flagged automatically. |

## Suggested layout

```text
research/
  malware/
    family-name/
      README.md
      references.md
      detections.md
      iocs.md
  cve/
    2026-xxxxx/
      README.md
      mitigations.md
      validation.md
  threat-models/
    topic-name/
      README.md
  white-papers/
    topic-name.md
```

Use the layout that matches the work. A small note does not need six empty files.

## Evidence language

Research should separate facts, assumptions, hypotheses, and recommendations.

Use:

- `Observed`
- `Reported by source`
- `Hypothesis`
- `Evidence missing`
- `Manual validation required`
- `Not evaluated`

Avoid unsupported certainty. If the research cannot prove something, say that plainly.

## Safety boundary

This folder is for defensive research. Keep it focused on detection, mitigation, validation, and public-safe analysis. Do not publish exploit-ready instructions, credential theft workflows, evasion guidance, private logs, secrets, or sensitive infrastructure details.

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`detections/`](../detections)
- [`templates/`](../templates)
