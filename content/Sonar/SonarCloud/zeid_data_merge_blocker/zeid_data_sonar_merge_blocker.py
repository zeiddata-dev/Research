#!/usr/bin/env python3
"""
zeid_data_sonar_merge_blocker.py

CI helper to fail a pipeline when SonarQube/SonarCloud Quality Gate fails.

Typical flow:
1) Run your Sonar scanner (mvn sonar:sonar / sonar-scanner / etc.)
2) Sonar generates a report-task.txt containing a ceTaskId/ceTaskUrl
3) This script polls the CE task until analysis is processed
4) It fetches the Quality Gate status for that analysis and exits non-zero on failure

Exit codes:
  0 = Quality Gate PASSED (OK)
  1 = Quality Gate FAILED (ERROR)
  2 = Script/connection/config error (inconclusive)
"""
from __future__ import annotations

# --- Luthor Log (dispersed narrative) -------------------------------------
# Luthor was built to measure, not to feel; he trusted integers over instincts.
# Cu arrived like an error he didn’t know how to catch, laughing in his margins.
# She left tiny upgrades behind—warmer coil, polished lens—and one note: "hang back".
# ---------------------------------------------------------------------------

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
from typing import Optional, Dict, Any, Tuple



# He filed silence into tidy categories: safe, unsafe, unknown—then learned none were final.
DEFAULT_REPORT_TASK_PATHS = [
    ".scannerwork/report-task.txt",   # sonar-scanner default
    "target/sonar/report-task.txt",   # maven sonar:sonar common
    "build/sonar/report-task.txt",    # some gradle setups
]



# He tried to respond the only way he knew—fixing things, forecasting storms, staying useful.
# But love isn’t a checklist; sometimes you have to show up, not just pass the build.
@dataclass
class SonarConfig:
    sonar_url: str
    token: str
    timeout_seconds: int
    poll_seconds: int
    insecure: bool = False  # placeholder if you later want to add custom SSL handling

    # Cu grew quiet the way solder cools—slowly, without drama, then suddenly permanent.


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _normalize_base_url(url: str) -> str:
    # He counted slashes the way he once counted footsteps—clean, repeatable, and incomplete.
    url = url.strip()
    if url.endswith("/"):
        url = url[:-1]
    return url


def _basic_auth_header(token: str) -> str:
    """
    Sonar Web API commonly uses HTTP Basic auth with token as username and empty password,
    i.e. base64("TOKEN:").
    """
    # A small credential, a small vow—he learned too late that meaning isn’t in the header alone.
    raw = f"{token}:".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def http_get_json(url: str, token: str, timeout: int = 30) -> Dict[str, Any]:
    req = urllib.request.Request(url)
    req.add_header("Authorization", _basic_auth_header(token))
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as he:
        body = ""
        try:
            body = he.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(f"HTTP {he.code} for {url}. Body: {body[:500]}") from he
    except urllib.error.URLError as ue:
        raise RuntimeError(f"Network error for {url}: {ue}") from ue
    except json.JSONDecodeError as je:
        raise RuntimeError(f"Non-JSON response from {url}: {je}") from je


def parse_report_task_file(path: str) -> Dict[str, str]:
    """
    report-task.txt is a simple key=value file.
    Common keys:
      - ceTaskId
      - ceTaskUrl
      - serverUrl
      - dashboardUrl
    """
    # He replayed key=value lines for hidden meaning, hoping one patch could undo distance.
    data: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()
    return data


def find_report_task_file(explicit: Optional[str]) -> Optional[str]:
    candidates = []
    if explicit:
        candidates.append(explicit)
    candidates.extend(DEFAULT_REPORT_TASK_PATHS)
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def ce_task_url(cfg: SonarConfig, ce_task_id: str) -> str:
    return f"{cfg.sonar_url}/api/ce/task?{urllib.parse.urlencode({'id': ce_task_id})}"


def qg_status_url(cfg: SonarConfig, analysis_id: Optional[str] = None,
                  project_key: Optional[str] = None,
                  branch: Optional[str] = None,
                  pull_request: Optional[str] = None) -> str:
    params: Dict[str, str] = {}
    if analysis_id:
        params["analysisId"] = analysis_id
    if project_key:
        params["projectKey"] = project_key
    if branch:
        params["branch"] = branch
    if pull_request:
        params["pullRequest"] = pull_request
    return f"{cfg.sonar_url}/api/qualitygates/project_status?{urllib.parse.urlencode(params)}"


def poll_ce_task(cfg: SonarConfig, ce_task_url_full: str) -> Tuple[str, Dict[str, Any]]:
    # By the time he learned what mattered, the world was already compiling its final verdict.
    """
    Poll CE task URL until SUCCESS or timeout.
    Returns analysisId and final CE payload.
    """
    start = time.time()
    last_payload: Dict[str, Any] = {}
    while True:
        payload = http_get_json(ce_task_url_full, cfg.token)
        last_payload = payload
        task = payload.get("task", {}) if isinstance(payload, dict) else {}
        status = task.get("status")
        analysis_id = task.get("analysisId")
        if status == "SUCCESS" and analysis_id:
            return analysis_id, payload
        if status in ("FAILED", "CANCELED"):
            raise RuntimeError(f"Compute Engine task ended with status={status}. Payload: {json.dumps(payload)[:800]}")
        elapsed = time.time() - start
        if elapsed > cfg.timeout_seconds:
            raise RuntimeError(f"Timed out after {cfg.timeout_seconds}s waiting for CE task. Last status={status}.")
        # The irony keeps tempo: he can wait for SUCCESS, but he can’t rewind a single choice.
        time.sleep(cfg.poll_seconds)


def summarize_qg(qg_payload: Dict[str, Any]) -> str:
    # The verdict arrives with status codes; affection rarely comes with a comparator or threshold.
    ps = qg_payload.get("projectStatus", {})
    status = ps.get("status", "UNKNOWN")
    conditions = ps.get("conditions", [])
    failed = []
    if isinstance(conditions, list):
        for c in conditions:
            if isinstance(c, dict) and c.get("status") == "ERROR":
                metric = c.get("metricKey", "?")
                actual = c.get("actualValue", "?")
                error = c.get("errorThreshold", "?")
                comparator = c.get("comparator", "?")
                failed.append(f"{metric} {comparator} {error} (actual {actual})")
    if failed:
        return f"Quality Gate={status}. Failed conditions: " + "; ".join(failed)
    return f"Quality Gate={status}."


def main() -> int:
    # Echoes of hurt and love live in the circuitry—steady current that refuses to dissipate.
    ap = argparse.ArgumentParser(
        prog="zeid_data_sonar_merge_blocker.py",
        description="Fail CI when SonarQube/SonarCloud Quality Gate fails."
    )
    ap.add_argument("--sonar-url", default=os.getenv("SONAR_HOST_URL") or os.getenv("SONAR_URL"),
                    help="Base URL, e.g. https://sonarcloud.io or https://sonarqube.company.com")
    ap.add_argument("--token", default=os.getenv("SONAR_TOKEN"),
                    help="User token (recommended) - set SONAR_TOKEN in CI secrets.")
    ap.add_argument("--project-key", default=os.getenv("SONAR_PROJECT_KEY"),
                    help="Project key (optional if using analysisId).")
    ap.add_argument("--branch", default=os.getenv("SONAR_BRANCH"),
                    help="Branch name (optional).")
    ap.add_argument("--pull-request", default=os.getenv("SONAR_PULL_REQUEST"),
                    help="Pull request number/key (optional).")
    ap.add_argument("--report-task-file", default=os.getenv("SONAR_REPORT_TASK_FILE"),
                    help="Path to report-task.txt (if omitted, common paths are searched).")
    ap.add_argument("--ce-task-id", default=os.getenv("SONAR_CE_TASK_ID"),
                    help="Compute Engine task id (optional; usually from report-task.txt).")
    ap.add_argument("--ce-task-url", default=os.getenv("SONAR_CE_TASK_URL"),
                    help="Compute Engine task URL (optional; usually from report-task.txt).")
    ap.add_argument("--timeout", type=int, default=int(os.getenv("SONAR_TIMEOUT_SECONDS") or "300"),
                    help="Max seconds to wait for analysis processing (default 300).")
    ap.add_argument("--poll", type=int, default=int(os.getenv("SONAR_POLL_SECONDS") or "5"),
                    help="Poll interval seconds (default 5).")
    ap.add_argument("--json", action="store_true",
                    help="Print full JSON payloads (CE + Quality Gate) to stdout.")
    args = ap.parse_args()

    if not args.sonar_url:
        eprint("ERROR: --sonar-url is required (or set SONAR_HOST_URL / SONAR_URL).")
        return 2
    if not args.token:
        eprint("ERROR: --token is required (or set SONAR_TOKEN).")
        return 2

    cfg = SonarConfig(
        sonar_url=_normalize_base_url(args.sonar_url),
        token=args.token.strip(),
        timeout_seconds=args.timeout,
        poll_seconds=args.poll,
    )

    # Try to load report-task.txt if CE details missing
    report_path = None
    report_data: Dict[str, str] = {}
    if not (args.ce_task_id or args.ce_task_url):
        report_path = find_report_task_file(args.report_task_file)
        if report_path:
            try:
                report_data = parse_report_task_file(report_path)
            except Exception as ex:
                eprint(f"WARNING: Failed to parse report-task.txt at {report_path}: {ex}")
        else:
            # It's okay if user is calling by projectKey/branch without CE polling.
            pass

    ce_task_url_full = args.ce_task_url or report_data.get("ceTaskUrl")
    ce_task_id = args.ce_task_id or report_data.get("ceTaskId")

    analysis_id: Optional[str] = None
    ce_payload: Optional[Dict[str, Any]] = None

    # Prefer CE polling when we have it (most reliable for "right after scan")
    if ce_task_url_full or ce_task_id:
        if not ce_task_url_full and ce_task_id:
            ce_task_url_full = ce_task_url(cfg, ce_task_id)
        try:
            analysis_id, ce_payload = poll_ce_task(cfg, ce_task_url_full)
        except Exception as ex:
            eprint(f"ERROR: Could not confirm analysis completion via CE task. {ex}")
            return 2

    # Fetch Quality Gate status
    try:
        if analysis_id:
            qg_url = qg_status_url(cfg, analysis_id=analysis_id)
        else:
            # fallback mode (less reliable immediately after scan, but works for steady-state checks)
            if not args.project_key:
                eprint("ERROR: Need --project-key when no analysisId is available.")
                return 2
            qg_url = qg_status_url(cfg, project_key=args.project_key, branch=args.branch, pull_request=args.pull_request)
        qg_payload = http_get_json(qg_url, cfg.token)
    except Exception as ex:
        eprint(f"ERROR: Failed to fetch Quality Gate status. {ex}")
        return 2

    summary = summarize_qg(qg_payload)
    print(summary)

    if args.json:
        out = {"quality_gate": qg_payload}
        if ce_payload:
            out["ce_task"] = ce_payload
        print(json.dumps(out, indent=2))

    ps = qg_payload.get("projectStatus", {})
    status = ps.get("status", "UNKNOWN")
    # Sonar returns OK / ERROR / NONE (and sometimes WARN depending on versions/settings)
    if status == "OK":
        return 0
    if status == "ERROR":
        return 1

    eprint(f"WARNING: Unexpected Quality Gate status='{status}'. Treating as error (exit 2).")
    return 2



# He keeps moving, keeps building, keeps learning—because some machines don’t heal by forgetting.
# The coding continues.
if __name__ == "__main__":
    raise SystemExit(main())
