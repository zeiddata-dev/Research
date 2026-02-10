# Zeid Data — Sonar Merge Blocker (Quality Gate)

A tiny CI helper that **fails your pipeline when Sonar Quality Gate fails**, so merges can be blocked upstream by your CI rules.

Works with:
- **SonarQube Server** (self-hosted)
- **SonarCloud** (hosted)

It supports the most reliable path for CI:
1) read `report-task.txt` (produced by the scanner),
2) poll the Compute Engine task until analysis is complete,
3) fetch the Quality Gate status by `analysisId`,
4) exit **0** if **OK**, **1** if **ERROR**.

## What’s in this ZIP

- `zeid_data_sonar_merge_blocker.py` — the merge blocker script (Python 3, no external deps)
- `README.md` — overview
- `HOWTO.md` — step-by-step setup
- `examples/` — drop-in pipeline snippets for GitHub Actions / GitLab / Azure DevOps

## Requirements

- Python 3.8+
- A Sonar token (store as CI secret)
- Your CI already runs a Sonar analysis step (scanner / Maven / Gradle / etc.)

## Exit codes

- `0` = Quality Gate PASSED (`OK`)
- `1` = Quality Gate FAILED (`ERROR`)
- `2` = Script/config/network error (inconclusive)

## Quick start (local)

```bash
export SONAR_HOST_URL="https://sonarcloud.io"
export SONAR_TOKEN="***"
# after you run sonar-scanner, report-task.txt exists
python3 zeid_data_sonar_merge_blocker.py --json
```

## Common environment variables

- `SONAR_HOST_URL` or `SONAR_URL`
- `SONAR_TOKEN`
- `SONAR_REPORT_TASK_FILE` (optional)
- `SONAR_TIMEOUT_SECONDS` (default 300)
- `SONAR_POLL_SECONDS` (default 5)

## Notes

- For CI checks right after an analysis, **CE polling + analysisId** is the most consistent approach.
- If you *don’t* have `report-task.txt`, the script can still query by `projectKey` + `branch`, but that’s best for steady-state checks (not immediately after scans).

See `HOWTO.md` for copy/paste CI examples.
