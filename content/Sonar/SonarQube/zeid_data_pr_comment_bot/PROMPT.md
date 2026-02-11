# Prompt — Build a GitHub Sonar PR Comment Bot (Zeid Data)

Build a tool that posts (or updates) a single comment on every GitHub Pull Request with a SonarQube summary.

## Inputs
- SonarQube base URL (SONAR_HOST_URL)
- Sonar token (SONAR_TOKEN)
- Sonar project key (SONAR_PROJECT_KEY)
- GitHub repo (GITHUB_REPOSITORY)
- PR number (github.event.pull_request.number)
- GitHub token (GITHUB_TOKEN)

## Output
A PR comment that includes:
- Quality Gate status + analysis date
- Key measures table
- Top issues (severity filtered)
- Links to Sonar overview/issues/hotspots pages

## Requirements
- Python 3.8+, no dependencies
- Use Sonar Web API endpoints:
  - /api/qualitygates/project_status (prefer analysisId when possible)
  - /api/measures/component
  - /api/issues/search
- Best-effort CE polling if report-task.txt exists (ceTaskUrl -> analysisId)
- GitHub API: list comments; upsert by searching for a hidden marker; patch existing comment or create new
- Optional flag: --fail-on-gate to exit 1 when Quality Gate is ERROR
- Package deliverables in a zip with README + HOWTO + example workflow
