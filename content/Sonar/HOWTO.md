# HOWTO — Sonar Merge Blocker (Quality Gate)

This guide shows how to wire Sonar Quality Gate into your CI so the pipeline fails when the gate fails.

---

## 1) Create a Sonar token

In SonarQube Server or SonarCloud:
- Go to your user profile / security settings
- Create a token (name it for the CI system)
- Store it as a secret in your CI (never commit it)

You will use:
- `SONAR_TOKEN` = the token value
- `SONAR_HOST_URL` = your Sonar base URL (e.g. `https://sonarcloud.io` or your internal SonarQube URL)

---

## 2) Ensure your pipeline runs a Sonar analysis step

Examples (choose what you already use):

- `sonar-scanner`
- `mvn sonar:sonar`
- `gradle sonarqube`
- language-specific scanners/plugins

After a successful scan, a file named `report-task.txt` is generated (commonly at):
- `.scannerwork/report-task.txt` (sonar-scanner)
- `target/sonar/report-task.txt` (often Maven)
- `build/sonar/report-task.txt` (some Gradle setups)

This script auto-detects those paths by default.

---

## 3) Add the merge blocker step

### 3A) Minimal invocation

```bash
python3 zeid_data_sonar_merge_blocker.py
```

The script will:
- read `report-task.txt`
- poll the Compute Engine task until status is SUCCESS
- request Quality Gate status for that analysis
- exit non-zero if the gate fails

### 3B) Tune polling (optional)

```bash
SONAR_TIMEOUT_SECONDS=600 SONAR_POLL_SECONDS=5 python3 zeid_data_sonar_merge_blocker.py
```

### 3C) If your `report-task.txt` is in a custom location

```bash
python3 zeid_data_sonar_merge_blocker.py --report-task-file path/to/report-task.txt
```

---

## 4) Drop-in CI examples

### GitHub Actions

Copy `examples/github-actions-sonar-merge-blocker.yml` into:
`.github/workflows/sonar-merge-blocker.yml`

Add repo secrets:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

Make sure your existing workflow runs a Sonar scan before the blocker step.

### GitLab CI

Copy the snippet from `examples/gitlab-ci-snippet.yml` into your `.gitlab-ci.yml`.

Add CI variables:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

### Azure DevOps

Copy the snippet from `examples/azure-pipelines-snippet.yml` into your `azure-pipelines.yml`.

Add pipeline variables/secrets:
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

---

## 5) Troubleshooting

### “report-task.txt not found”
- Confirm your scan step ran and completed
- Confirm where your scanner writes the file:
  - sonar-scanner: `.scannerwork/report-task.txt`
  - Maven often: `target/sonar/report-task.txt`

Use:
```bash
find . -name report-task.txt -maxdepth 4
```
then pass `--report-task-file`.

### HTTP 401 / 403
- Token is missing/invalid OR user lacks permission for Web API calls
- Ensure `SONAR_TOKEN` is set as a secret
- Ensure the token user has access to the project

### Timeout waiting for CE task
- Your Sonar server is under load or background tasks are slow
- Increase `SONAR_TIMEOUT_SECONDS`

### Status is “NONE” / “UNKNOWN”
- Treat as misconfiguration: usually analysis hasn’t completed or the project is mis-specified
- Prefer CE polling mode (use `report-task.txt`)

---

## 6) Optional: PR vs Branch
If you must query by project key (fallback mode), you can do:

```bash
python3 zeid_data_sonar_merge_blocker.py --project-key my_project --branch main
# or
python3 zeid_data_sonar_merge_blocker.py --project-key my_project --pull-request 123
```

But the recommended mode is still: **scan → report-task.txt → CE poll → analysisId → Quality Gate**.
