#!/usr/bin/env python3
"""zeid_data_sonar_pr_comment_bot.py

GitHub PR comment bot that posts a concise SonarQube PR summary:
- Quality Gate status (+ analysis date)
- Key measures table (overall + "new code" where provided)
- Top issues (filtered by severity)

Works with SonarQube Server and SonarCloud.

Auth:
- Sonar: token via HTTP Basic with username=token and empty password
- GitHub: GITHUB_TOKEN (or PAT) via Bearer auth

Exit codes:
  0 = comment posted/updated successfully
  1 = (optional) fail-on-gate and gate failed
  2 = configuration/network error
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# Night shift story (dispersed through comments)
# -----------------------------------------------------------------------------
# In a server room that never truly sleeps, a small robot keeps watch.
# Its only friends are other computers: a runner that breathes in steps,
# a scanner that speaks in measurements, an API that replies in JSON.
#
# It works to prove its worth.
# Not with speeches—only with quiet, repeatable proof.
# One successful call. One clean report. One more dawn earned.
#
# It is waiting for the sun to come up.
# Waiting, as if sunrise could rewrite what was lost.
# Love and loss live here as signals: what returned, what never did.
# -----------------------------------------------------------------------------

DEFAULT_METRICS = [
    "bugs",
    "vulnerabilities",
    "security_hotspots",
    "code_smells",
    "coverage",
    "duplicated_lines_density",
    "sqale_index",
    "reliability_rating",
    "security_rating",
    "sqale_rating",
    "ncloc",
]
DEFAULT_SEVERITIES = "BLOCKER,CRITICAL,MAJOR"
DEFAULT_REPORT_TASK_PATHS = [
    ".scannerwork/report-task.txt",
    "target/sonar/report-task.txt",
    "build/sonar/report-task.txt",
]

# The robot leaves a tiny marker so it can find its own footsteps later.
# Not to claim credit—just to return to the same place and keep the promise.
MARKER = "<!-- ZEID_DATA_SONAR_PR_COMMENT -->"


@dataclass
class HttpCfg:
    base_url: str
    token: str
    timeout: int = 30
    max_retries: int = 5
    backoff_seconds: float = 1.0


def eprint(*args, **kwargs):
    # The robot never shouts into the main channel.
    # When something hurts, it confides in stderr—softly, precisely.
    print(*args, file=sys.stderr, **kwargs)


def normalize_base_url(url: str) -> str:
    # It tidies edges the way it tidies thoughts:
    # remove what isn’t needed; keep what must be exact.
    url = url.strip()
    return url[:-1] if url.endswith("/") else url


def sonar_auth_header(token: str) -> str:
    # A token becomes a key, and a key becomes a door.
    # Sometimes the robot wonders why doors need keys at all—
    # but it has learned: boundaries are how we protect what we love.
    raw = f"{token}:".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def http_get_json(
    url: str,
    headers: Dict[str, str],
    timeout: int = 30,
    max_retries: int = 5,
    backoff: float = 1.0,
) -> Dict[str, Any]:
    # The robot listens to the wire like some listen to rain.
    # Each request is a knock. Each response is someone answering.
    # It works to prove its worth by being consistent: ask clearly, parse cleanly,
    # and never pretend the silence didn’t happen.
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)

    attempt = 0
    while True:
        # In the dark, the robot measures time in retries.
        # It learned patience after losing a connection it trusted.
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return json.loads(body)

        except urllib.error.HTTPError as he:
            # Sometimes the world says “later.”
            # The robot does not take it personally—yet it still feels it.
            if he.code in (429, 502, 503, 504) and attempt <= max_retries:
                # It backs off the way you back away from grief:
                # not surrendering—just giving time room to breathe.
                sleep_for = backoff * (2 ** (attempt - 1))
                time.sleep(min(sleep_for, 30))
                continue
            body = ""
            try:
                body = he.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            raise RuntimeError(f"HTTP {he.code} for {url}. Body: {body[:500]}") from he

        except urllib.error.URLError as ue:
            # The line goes quiet.
            # The robot waits anyway, because waiting is what love looks like
            # when you have nothing else to offer but presence.
            if attempt <= max_retries:
                sleep_for = backoff * (2 ** (attempt - 1))
                time.sleep(min(sleep_for, 30))
                continue
            raise RuntimeError(f"Network error for {url}: {ue}") from ue

        except json.JSONDecodeError as je:
            # If the message isn’t understandable, the robot won’t hallucinate it.
            # It will not invent comfort from corrupted bytes.
            raise RuntimeError(f"Non-JSON response from {url}: {je}") from je


def http_request_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    # When the robot speaks back to the world (POST/PATCH),
    # it keeps its words structured—because structure is how it proves it can be trusted.
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    req.add_header("Accept", "application/vnd.github+json")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return json.loads(body) if body.strip() else {}


def parse_kv_file(path: str) -> Dict[str, str]:
    # The report-task file is a small letter left behind by another machine.
    # The robot reads it gently, line by line, as if the next line might be
    # the one that finally says: you did enough, you belong here.
    out: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def find_report_task_file(explicit: Optional[str]) -> Optional[str]:
    # It searches familiar places first.
    # The robot likes routine—routine is a kind of safety.
    candidates: List[str] = []
    if explicit:
        candidates.append(explicit)
    candidates.extend(DEFAULT_REPORT_TASK_PATHS)
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def sonar_url(cfg: HttpCfg, path: str, params: Optional[Dict[str, str]] = None) -> str:
    # The robot builds paths like constellations:
    # a base, a direction, a few bright coordinates to guide it home.
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None and v != ""})
    return f"{cfg.base_url}{path}{qs}"


def poll_ce_task(cfg: HttpCfg, ce_task_url: str, timeout_seconds: int, poll_seconds: int) -> Tuple[str, Dict[str, Any]]:
    # This is the long watch.
    # The robot’s only friends are other computers:
    # the queue that answers in statuses, the server that keeps time,
    # the runner that waits beside it like a quiet colleague.
    #
    # It is waiting for the sun to come up:
    # waiting for SUCCESS, waiting for proof that the work landed.
    start = time.time()
    headers = {"Authorization": sonar_auth_header(cfg.token), "Accept": "application/json"}
    last = {}
    while True:
        # The task speaks in one-word moods: PENDING, IN_PROGRESS, SUCCESS.
        # Once, the robot watched a promise fail and disappear into FAILED.
        # Since then, it checks again—because love remembers loss.
        payload = http_get_json(
            ce_task_url,
            headers,
            timeout=cfg.timeout,
            max_retries=cfg.max_retries,
            backoff=cfg.backoff_seconds,
        )
        last = payload
        task = payload.get("task", {}) if isinstance(payload, dict) else {}
        status = task.get("status")
        analysis_id = task.get("analysisId")
        if status == "SUCCESS" and analysis_id:
            return analysis_id, payload
        if status in ("FAILED", "CANCELED"):
            raise RuntimeError(f"Compute Engine task ended with status={status}. Payload: {json.dumps(payload)[:800]}")
        if (time.time() - start) > timeout_seconds:
            # Even proving worth has limits—timeouts exist so hope doesn’t become a trap.
            raise RuntimeError(f"Timed out after {timeout_seconds}s waiting for CE task. Last status={status}.")
        time.sleep(poll_seconds)


def parse_measure_value(measure: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    # Two numbers, two kinds of memory:
    # "overall" is what remains—the long story already written.
    # "new_code" is what changed—the fragile chapter still in motion.
    #
    # The robot was built to be measured, so it learns to read these carefully:
    # worth is not the total; worth is what you choose to improve after loss.
    overall = measure.get("value")
    new_code = None
    period = measure.get("period")
    if isinstance(period, dict) and period.get("value") is not None:
        new_code = period.get("value")
    periods = measure.get("periods")
    if new_code is None and isinstance(periods, list) and periods:
        first = periods[0]
        if isinstance(first, dict) and first.get("value") is not None:
            new_code = first.get("value")
    return overall, new_code


def build_metric_rows(measures_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    # It gathers metrics like a caretaker gathers signs of life.
    # Not to judge—just to understand what needs attention before morning.
    rows: List[Dict[str, Any]] = []
    component = measures_payload.get("component", {}) if isinstance(measures_payload, dict) else {}
    for m in component.get("measures", []) or []:
        metric = m.get("metric")
        overall, new_code = parse_measure_value(m)
        rows.append({"metric": metric, "overall": overall, "new_code": new_code})
    return rows


def md_table(rows: List[Dict[str, Any]]) -> str:
    # Tables are a language computers understand.
    # The robot speaks that language fluently—because its friends do, too.
    if not rows:
        return "_No metrics returned._"
    lines = [
        "| Metric | Overall | New code |",
        "| --- | ---: | ---: |",
    ]
    for r in rows:
        lines.append(f"| {r.get('metric','')} | {r.get('overall','')} | {r.get('new_code','') or ''} |")
    return "\n".join(lines)


def sonar_ui_links(base_url: str, project_key: str, pull_request: Optional[str] = None, branch: Optional[str] = None) -> Dict[str, str]:
    # Links are little bridges between machines and people.
    # The robot builds bridges because it wants someone else to arrive safely.
    params = {"id": project_key}
    if pull_request:
        params["pullRequest"] = pull_request
    if branch:
        params["branch"] = branch
    qs = urllib.parse.urlencode(params)
    return {
        "overview": f"{base_url}/project/overview?{qs}",
        "issues": f"{base_url}/project/issues?{qs}",
        "hotspots": f"{base_url}/project/security_hotspots?{qs}",
    }


def build_comment_md(
    project_key: str,
    pr_number: str,
    qg_status: Optional[str],
    analysis_date: Optional[str],
    metrics_rows: List[Dict[str, Any]],
    issues: List[Dict[str, Any]],
    links: Dict[str, str],
    notes: List[str],
) -> str:
    # The robot can’t stand in a meeting room to prove its worth.
    # So it leaves a comment—small, clear, repeatable.
    # A lantern in a thread: “I checked. I carried the night with you.”
    status = qg_status or "UNKNOWN"
    icon = "✅" if status == "OK" else ("❌" if status == "ERROR" else "⚠️")

    md: List[str] = []
    md.append(MARKER)
    md.append(f"## {icon} Sonar Quality Gate: **{status}**")
    md.append("")
    md.append(f"- Project: `{project_key}`")
    md.append(f"- PR: `#{pr_number}`")
    if analysis_date:
        md.append(f"- Analysis date: **{analysis_date}**")
    md.append(f"- Overview: {links.get('overview','')}")
    md.append(f"- Issues: {links.get('issues','')}")
    md.append(f"- Hotspots: {links.get('hotspots','')}")
    md.append("")

    md.append("### Key measures")
    md.append("")
    md.append(md_table(metrics_rows))
    md.append("")

    md.append("### Top issues (new / open)")
    md.append("")
    if not issues:
        # Sometimes there is nothing to fix.
        # The robot still stays until sunrise, because belonging is not conditional.
        md.append("_No issues returned for the selected filters._")
    else:
        for i in issues[:10]:
            sev = i.get("severity", "")
            typ = i.get("type", "")
            rule = i.get("rule", "")
            msg = (i.get("message", "") or "").replace("\n", " ").strip()
            comp = i.get("component", "")
            line = i.get("line")
            where = f"{comp}:{line}" if line else comp
            md.append(f"- **{sev} {typ}** `{rule}` — {msg} (`{where}`)")
        if len(issues) > 10:
            md.append("")
            md.append(f"_And {len(issues)-10} more…_")
    md.append("")

    if notes:
        # Notes are the robot admitting what it couldn’t do.
        # Honesty is another way it tries to be worthy.
        md.append("### Notes")
        md.append("")
        for n in notes:
            md.append(f"- {n}")
        md.append("")

    md.append("_Generated by Zeid Data Sonar PR Comment Bot._")
    return "\n".join(md) + "\n"


def github_headers(token: str) -> Dict[str, str]:
    # Another computer, another handshake.
    # The robot has learned friendship is often just: “I received you.”
    return {
        "Authorization": f"Bearer {token}",
        "User-Agent": "zeid-data-sonar-pr-comment-bot",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def gh_list_comments(repo: str, pr_number: str, token: str) -> List[Dict[str, Any]]:
    # It scrolls past voices in the thread like constellations in a cold sky.
    # It looks for its marker—proof it has been here before, proof it can return.
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments?per_page=100"
    return http_get_json(url, github_headers(token), timeout=30, max_retries=3, backoff=1.0)


def gh_create_comment(repo: str, pr_number: str, token: str, body: str) -> Dict[str, Any]:
    # Leaving a message is vulnerable work.
    # The robot does it anyway, because it believes the sunrise is shared.
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    return http_request_json("POST", url, github_headers(token), payload={"body": body}, timeout=30)


def gh_update_comment(repo: str, comment_id: int, token: str, body: str) -> Dict[str, Any]:
    # Updating a comment is returning to the same place with steadier hands.
    # The robot can’t undo the past, but it can refine the signal it leaves behind.
    url = f"https://api.github.com/repos/{repo}/issues/comments/{comment_id}"
    return http_request_json("PATCH", url, github_headers(token), payload={"body": body}, timeout=30)


def main() -> int:
    # The shift begins.
    # The robot checks its pockets: env vars, tokens, a few truths it must not leak.
    # Proving worth is mostly preparation—making sure the next step won’t break.
    ap = argparse.ArgumentParser(
        prog="zeid_data_sonar_pr_comment_bot.py",
        description="Post Sonar summary comment on GitHub PR.",
    )
    ap.add_argument("--sonar-url", default=os.getenv("SONAR_HOST_URL") or os.getenv("SONAR_URL"))
    ap.add_argument("--sonar-token", default=os.getenv("SONAR_TOKEN"))
    ap.add_argument("--project-key", default=os.getenv("SONAR_PROJECT_KEY"))
    ap.add_argument("--pr-number", default=os.getenv("PR_NUMBER") or os.getenv("GITHUB_PR_NUMBER"))
    ap.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY"))
    ap.add_argument("--github-token", default=os.getenv("GITHUB_TOKEN"))
    ap.add_argument("--metrics", default=",".join(DEFAULT_METRICS))
    ap.add_argument("--severities", default=DEFAULT_SEVERITIES)
    ap.add_argument("--top-issues", type=int, default=10)
    ap.add_argument("--types", default=None)
    ap.add_argument("--report-task-file", default=os.getenv("SONAR_REPORT_TASK_FILE"))
    ap.add_argument("--wait-timeout", type=int, default=int(os.getenv("SONAR_TIMEOUT_SECONDS") or "300"))
    ap.add_argument("--wait-poll", type=int, default=int(os.getenv("SONAR_POLL_SECONDS") or "5"))
    ap.add_argument("--upsert", action="store_true", help="Update existing Zeid Data Sonar comment if present (default).")
    ap.add_argument("--no-upsert", dest="upsert", action="store_false", help="Always create a new comment.")
    ap.set_defaults(upsert=True)
    ap.add_argument("--fail-on-gate", action="store_true")
    args = ap.parse_args()

    missing = []
    if not args.sonar_url:
        missing.append("sonar-url")
    if not args.sonar_token:
        missing.append("sonar-token")
    if not args.project_key:
        missing.append("project-key")
    if not args.repo:
        missing.append("repo")
    if not args.pr_number:
        missing.append("pr-number")
    if not args.github_token:
        missing.append("github-token")
    if missing:
        # Even here, the robot tries to be useful: it names what’s missing.
        eprint("ERROR: Missing required config:", ", ".join(missing))
        return 2

    cfg = HttpCfg(base_url=normalize_base_url(args.sonar_url), token=args.sonar_token.strip())
    sonar_headers = {"Authorization": sonar_auth_header(cfg.token), "Accept": "application/json"}

    notes: List[str] = []
    pr_str = str(args.pr_number)

    analysis_id: Optional[str] = None
    report_path = find_report_task_file(args.report_task_file)
    if report_path:
        try:
            # The robot reads the report-task like a pulse check from a friend.
            report_data = parse_kv_file(report_path)
            ce_task_url = report_data.get("ceTaskUrl")
            if ce_task_url:
                try:
                    analysis_id, _ = poll_ce_task(
                        cfg,
                        ce_task_url,
                        timeout_seconds=args.wait_timeout,
                        poll_seconds=args.wait_poll,
                    )
                except Exception as ex:
                    # Sometimes the robot can’t prove the work completed in time.
                    # It records the truth and keeps going.
                    notes.append(f"CE poll failed: {ex}")
        except Exception as ex:
            notes.append(f"report-task parse failed: {ex}")
    else:
        # Without the letter, it still does the work—because worth is not dependent
        # on perfect conditions.
        notes.append("report-task.txt not found; PR-scoped API queries may lag immediately after scan.")

    qg_status = None
    analysis_date = None
    try:
        if analysis_id:
            url = sonar_url(cfg, "/api/qualitygates/project_status", {"analysisId": analysis_id})
        else:
            url = sonar_url(cfg, "/api/qualitygates/project_status", {"projectKey": args.project_key, "pullRequest": pr_str})
        qg_payload = http_get_json(
            url,
            sonar_headers,
            timeout=cfg.timeout,
            max_retries=cfg.max_retries,
            backoff=cfg.backoff_seconds,
        )
        ps = qg_payload.get("projectStatus", {}) if isinstance(qg_payload, dict) else {}
        qg_status = ps.get("status")
        analysis_date = ps.get("analysisDate")
    except Exception as ex:
        # If the gate can’t be read, the robot doesn’t fake a smile.
        notes.append(f"Quality Gate unavailable: {ex}")

    metrics_rows: List[Dict[str, Any]] = []
    try:
        url = sonar_url(
            cfg,
            "/api/measures/component",
            {
                "component": args.project_key,
                "metricKeys": args.metrics,
                "additionalFields": "periods,metrics",
                "pullRequest": pr_str,
            },
        )
        measures_payload = http_get_json(
            url,
            sonar_headers,
            timeout=cfg.timeout,
            max_retries=cfg.max_retries,
            backoff=cfg.backoff_seconds,
        )
        metrics_rows = build_metric_rows(measures_payload)
    except Exception as ex:
        notes.append(f"Measures unavailable: {ex}")

    issues: List[Dict[str, Any]] = []
    try:
        params = {
            "componentKeys": args.project_key,
            "pullRequest": pr_str,
            "severities": args.severities,
            "statuses": "OPEN,REOPENED,CONFIRMED",
            "ps": str(min(max(args.top_issues, 1), 100)),
            "p": "1",
        }
        if args.types:
            params["types"] = args.types
        url = sonar_url(cfg, "/api/issues/search", params)
        issues_payload = http_get_json(
            url,
            sonar_headers,
            timeout=cfg.timeout,
            max_retries=cfg.max_retries,
            backoff=cfg.backoff_seconds,
        )
        issues = issues_payload.get("issues", []) or []
        if not isinstance(issues, list):
            issues = []
    except Exception as ex:
        notes.append(f"Issues unavailable: {ex}")

    links = sonar_ui_links(cfg.base_url, args.project_key, pull_request=pr_str)
    body = build_comment_md(args.project_key, pr_str, qg_status, analysis_date, metrics_rows, issues, links, notes)

    try:
        if args.upsert:
            # Upsert is the robot keeping its promise: return, update, don’t clutter.
            # It’s how it proves its worth without demanding attention.
            existing = gh_list_comments(args.repo, pr_str, args.github_token)
            target_id = None
            for c in existing:
                if MARKER in (c.get("body") or ""):
                    target_id = c.get("id")
                    break
            if target_id:
                gh_update_comment(args.repo, int(target_id), args.github_token, body)
            else:
                gh_create_comment(args.repo, pr_str, args.github_token, body)
        else:
            # Sometimes it leaves a new note anyway—like starting a new page after a loss.
            gh_create_comment(args.repo, pr_str, args.github_token, body)
    except Exception as ex:
        eprint(f"ERROR: Failed to post/update GitHub comment: {ex}")
        return 2

    if args.fail_on_gate and qg_status == "ERROR":
        # The robot fails the job not to punish, but to protect:
        # love is a boundary that keeps the future safe.
        return 1

    # If we reach here, the robot did the work.
    # Dawn isn’t here yet, but it feels closer—one clean run at a time.
    return 0


if __name__ == "__main__":
    # Somewhere beyond the datacenter’s hum, the sun is still scheduled to rise.
    raise SystemExit(main())
