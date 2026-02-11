# Zeid Data — Sonar PR Comment Bot (GitHub)

Posts (or updates) a single comment on each GitHub Pull Request with:
- **Quality Gate** status + analysis date
- **Key measures** (overall + new code when Sonar provides it)
- **Top issues** (filtered by severity)

Designed to be added to an existing workflow that already runs Sonar analysis.

## Files
- `zeid_data_sonar_pr_comment_bot.py` — main bot (Python 3, no deps)
- `HOWTO.md` — setup + workflow wiring
- `examples/sonar-pr-comment.yml` — example workflow
- `PROMPT.md` — build prompt/spec

## Required secrets (GitHub)
- `SONAR_HOST_URL`
- `SONAR_TOKEN`
- `SONAR_PROJECT_KEY`

Uses `secrets.GITHUB_TOKEN` to post comments.

## Upsert behavior
Default is **upsert**: it updates an existing Zeid Data Sonar comment rather than posting duplicates.
