# Zeid Data — Sonar Evidence Pack Generator

Generate **audit-ready evidence bundles** from SonarQube Server or SonarQube Cloud (SonarCloud).

The tool pulls:
- Quality Gate status + analysis timestamp
- Key measures (bugs, vulnerabilities, hotspots count if available, coverage, duplication, debt, ratings, LOC, smells)
- “New code” deltas (leak-period values when Sonar exposes them)
- Top issues and (best-effort) top security hotspots

It outputs: **JSON + CSV + Markdown** (and optional PDF).

## What’s in this ZIP

- `zeid_data_sonar_evidence_pack.py` — main CLI tool (Python, no external deps required)
- `README.md` — overview
- `HOWTO.md` — setup and CI wiring
- `PROMPT.md` — the build prompt/spec (if you want to regenerate/extend)
- `examples/` — CI snippets

## Requirements

- Python 3.8+
- Sonar token (store as CI secret)
- Network access to your Sonar instance

Optional:
- `reportlab` for `--pdf` output

## Quick start

```bash
export SONAR_HOST_URL="https://sonarcloud.io"
export SONAR_TOKEN="***"
python3 zeid_data_sonar_evidence_pack.py --project-key YOUR_PROJECT_KEY --outdir ./out --raw
```

Outputs go to `./out/evidence_pack_<project>_<timestamp>/`.

## Common options

- Branch evidence pack:
  ```bash
  python3 zeid_data_sonar_evidence_pack.py --project-key KEY --branch main
  ```

- Pull request evidence pack:
  ```bash
  python3 zeid_data_sonar_evidence_pack.py --project-key KEY --pull-request 123
  ```

- Time window filtering for issues (best-effort):
  ```bash
  python3 zeid_data_sonar_evidence_pack.py --project-key KEY --from 2026-02-01T00:00:00Z --to 2026-02-10T00:00:00Z
  ```

- PDF summary:
  ```bash
  python3 zeid_data_sonar_evidence_pack.py --project-key KEY --pdf
  ```

## Notes

- Hotspots API on SonarCloud may be internal/plan-dependent; the tool will **continue** even if hotspots are unavailable.
- Some Sonar versions deprecate certain `issues/search` parameters. The tool uses best-effort compatibility and will record what it could retrieve.
