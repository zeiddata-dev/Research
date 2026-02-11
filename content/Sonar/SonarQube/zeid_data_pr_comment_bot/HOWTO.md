# HOWTO — Sonar PR Comment Bot (GitHub)

## 1) Add secrets
In your GitHub repo settings:
- `SONAR_HOST_URL` (e.g., https://sonarqube.company.com or https://sonarcloud.io)
- `SONAR_TOKEN`
- `SONAR_PROJECT_KEY`

## 2) Add workflow
Copy:
- `examples/sonar-pr-comment.yml` → `.github/workflows/sonar-pr-comment.yml`

## 3) Ensure Sonar analysis runs before the bot step
The bot works best if `report-task.txt` exists (from the scanner), because it can poll Sonar’s Compute Engine task.

Common locations:
- `.scannerwork/report-task.txt`
- `target/sonar/report-task.txt`
- `build/sonar/report-task.txt`

Custom path:
- set `SONAR_REPORT_TASK_FILE` env var or pass `--report-task-file`.

## 4) Optional: fail CI when gate fails
Add `--fail-on-gate` to the run command.
