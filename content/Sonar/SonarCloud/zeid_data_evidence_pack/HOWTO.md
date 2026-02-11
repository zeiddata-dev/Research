# HOWTO — Sonar Evidence Pack Generator

This guide helps you run the tool locally or inside CI.

---

## 1) Create a Sonar token

In SonarQube Server / SonarCloud:
- Open your user profile → Security
- Generate a token for CI/reporting
- Store it as a secret

You will use:
- `SONAR_TOKEN` = token value
- `SONAR_HOST_URL` = base URL (e.g., `https://sonarcloud.io` or your internal SonarQube URL)

---

## 2) Run locally

```bash
export SONAR_HOST_URL="https://sonarcloud.io"
export SONAR_TOKEN="***"
python3 zeid_data_sonar_evidence_pack.py --project-key YOUR_PROJECT_KEY --outdir ./out --raw
```

The output directory will contain:
- `summary.md`
- `evidence.json`
- `issues.csv`
- `hotspots.csv` (if available)
- `raw/` API responses (if `--raw`)

---

## 3) Branch and PR reports

Branch:

```bash
python3 zeid_data_sonar_evidence_pack.py --project-key KEY --branch main
```

Pull request:

```bash
python3 zeid_data_sonar_evidence_pack.py --project-key KEY --pull-request 123
```

---

## 4) Time window filtering

Best-effort filtering is applied to issue creation dates:

```bash
python3 zeid_data_sonar_evidence_pack.py --project-key KEY --from 2026-02-01T00:00:00Z --to 2026-02-10T00:00:00Z
```

Note: Sonar’s issue model is not purely time-series; “what changed” is primarily represented via new-code/leak-period metrics and PR analysis.

---

## 5) CI examples

### GitHub Actions
Copy `examples/github-actions-evidence-pack.yml` into `.github/workflows/`.

Set repo secrets:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

### GitLab CI
Copy `examples/gitlab-ci-evidence-pack.yml` into your `.gitlab-ci.yml` (or include it).

Set CI variables:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

### Azure DevOps
Copy `examples/azure-pipelines-evidence-pack.yml` into your pipeline.

Set variables/secrets:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

---

## 6) Troubleshooting

### 401/403
- Verify token
- Verify the token user has “Browse” permission to the project
- Some endpoints may be restricted by edition/plan

### Hotspots unavailable
- Tool will mark hotspots as unavailable and still produce the bundle
- On SonarCloud, hotspots API may be internal/plan-dependent

### Large projects / pagination
- The tool paginates issues/hotspots until it reaches your top-N cap
- Increase `--top-issues` if needed
