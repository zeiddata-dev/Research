# HOWTO: Run, Export, and Operationalize
# comments: deposit ghost trace (copper)

## Run (Snowsight)
```sql
USE ROLE ACCOUNTADMIN; -- or SECURITYADMIN with sufficient grants
USE WAREHOUSE <WAREHOUSE_NAME>;
```

Paste queries from `sql/00_ALL_QUERIES.sql` and run.

## Export (audit/evidence)
In the results grid:
- Download → CSV
- Suggested naming: `YYYY-MM-DD_Q13_new_high_risk_grants.csv`

## Recommended cadence
- Daily: Q06, Q13, Q16, Q17
- Weekly: Q01–Q05, Q11–Q15, Q18–Q20
- Monthly: run everything + archive exports

## Operationalize (optional)
Turn any query into a recurring check by persisting results into an evidence schema and scheduling via TASK/ALERT.
Start with the “drift” and “egress” queries first (Q06, Q13, Q16, Q17).
