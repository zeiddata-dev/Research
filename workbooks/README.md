<!-- ZEID DATA README HERO START -->
![Zeid Data workbooks banner](../assets/banners/readme/workbooks.png)

<p align="center">
  <a href="../README.md"><img alt="Repo Root" src="https://img.shields.io/badge/Repo%20Root-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-1F6FEB?style=for-the-badge&logo=readthedocs&logoColor=white"></a>
  <a href="../detections"><img alt="Detections" src="https://img.shields.io/badge/Detections-FFB800?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../research"><img alt="Research" src="https://img.shields.io/badge/Research-0B5FFF?style=for-the-badge&logo=github&logoColor=white"></a>
  <a href="../templates"><img alt="Templates" src="https://img.shields.io/badge/Templates-334155?style=for-the-badge&logo=markdown&logoColor=white"></a>
</p>
<!-- ZEID DATA README HERO END -->

# Zeid Data Workbooks

This folder is for dashboards, workbook exports, saved searches, visual analytics, and importable views that help turn evidence into reviewable operational pictures.

A workbook is not a place to invent insight. It should show source-backed views, make gaps visible, and help a reviewer move from summary to evidence.

## What belongs here

- Microsoft Sentinel workbook JSON.
- Splunk dashboards and saved searches.
- Elastic/Kibana dashboard exports.
- Grafana dashboards.
- Static dashboard prototypes with clear sample data boundaries.
- Screenshot previews and import notes.

## Minimum workbook documentation

Each workbook folder should include:

| Section | Requirement |
|---|---|
| Purpose | What decision, review, or workflow the workbook supports. |
| Platform | Product and version assumptions, if known. |
| Data sources | Tables, indexes, log sources, fields, or sample datasets required. |
| Import steps | Exact import path or deployment instructions. |
| Evidence model | How panels map back to source records. |
| Known gaps | Missing data, assumptions, unsupported views, or stale panels. |
| Screenshots | Public-safe preview images, if available. |

## Evidence-first dashboard rule

Every panel should either:

- link to source records,
- show the source query,
- list required fields,
- or clearly display `evidence missing`.

Do not publish static confidence, risk, or health claims without a visible evidence path.

## Suggested layout

```text
workbooks/
  sentinel/
    workbook-name/
      README.md
      workbook.json
      screenshots/
  splunk/
    dashboard-name/
      README.md
      dashboard.xml
      savedsearches.conf
  grafana/
    dashboard-name/
      README.md
      dashboard.json
```

## Review checklist

- [ ] Import steps are present.
- [ ] Required data sources are listed.
- [ ] Required fields are listed.
- [ ] Screenshots are sanitized.
- [ ] Queries are readable or linked.
- [ ] Unsupported panels show gaps instead of fake findings.
- [ ] Dashboard claims trace back to evidence.

## Related docs

- [`docs/taxonomy.md`](../docs/taxonomy.md)
- [`docs/standards/evidence.md`](../docs/standards/evidence.md)
- [`templates/`](../templates)
