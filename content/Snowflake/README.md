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
