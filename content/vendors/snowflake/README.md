<!-- ZEID DATA README HERO START -->
![Zeid Data snowflake banner](../../../assets/banners/readme/content.png)

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

![zeid-data](https://img.shields.io/badge/zeid%20data-0B5FFF?style=flat-square) ![public-safe](https://img.shields.io/badge/public%20safe-166534?style=flat-square) ![research](https://img.shields.io/badge/research-1F6FEB?style=flat-square) ![content](https://img.shields.io/badge/content-334155?style=flat-square) ![vendor-content](https://img.shields.io/badge/vendor%20content-334155?style=flat-square) ![governance](https://img.shields.io/badge/governance-6F42C1?style=flat-square) ![evidence-assets](https://img.shields.io/badge/evidence%20assets-334155?style=flat-square) ![snowflake](https://img.shields.io/badge/snowflake-334155?style=flat-square) ![data-security](https://img.shields.io/badge/data%20security-334155?style=flat-square) ![analytics](https://img.shields.io/badge/analytics-334155?style=flat-square) ![vendors](https://img.shields.io/badge/vendors-334155?style=flat-square)

<!-- ZEID DATA TAGS END -->

# Zeid Data Snowflake AI Governance & Compliance Query Pack


This pack provides **20 Snowflake SQL queries** focused on:
- AI governance (Cortex/LLM usage visibility)
- Compliance evidence (IAM, policy coverage, access signals)
- Data movement monitoring (stages, COPY INTO, transfers)

## Files
- `sql/00_ALL_QUERIES.sql` – all queries in one file
- `docs/HOWTO.md` – run/export/operationalize guidance

## Prerequisites
- Most queries rely on `SNOWFLAKE.ACCOUNT_USAGE` (often needs `MONITOR USAGE` or admin visibility).
- Some queries rely on `SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY` (availability varies by edition/config).
- Expect some `ACCOUNT_USAGE` latency (commonly up to ~90 minutes).

## Quick start
1. Snowsight → Worksheets
2. `USE ROLE ACCOUNTADMIN;` (or equivalent)
3. Run queries from `sql/00_ALL_QUERIES.sql`
4. Export results as CSV for evidence snapshots

## Safety tip
If you export query text, keep exports in your evidence repo with restricted access.
Your future self will thank you during audit week.
