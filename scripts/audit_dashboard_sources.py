#!/usr/bin/env python3
"""Audit Li-12 dashboard source and strict actual-record loader safety."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dashboard_data_loader import get_record_inventory, load_cached_normalized_records

DASHBOARD_FILES = [
    ROOT / "li12_unified_dashboard.py",
    ROOT / "dashboard_data_loader.py",
    ROOT / "dashboard_insights.py",
    ROOT / "dashboard_privacy.py",
    ROOT / "dashboard_components.py",
]
REQUIRED_FUNCTIONS = [
    "get_today_bounds",
    "filter_records_for_today",
    "build_today_relationship_rating",
    "build_today_bridge_summary",
    "render_today_rating_card",
    "render_today_inputs",
    "render_today_signals",
    "render_today_evidence",
    "debug_print_record_inventory",
]
DISALLOWED_TODAY_PATTERNS = [
    "fake today",
    "sample today",
    "demo today",
    "synthetic today",
    "seed today",
    "placeholder today",
    "mock today",
]
FORBIDDEN_RENDER_FIELDS = [
    "source_file",
    "record_hash",
    "imported_path",
    "raw",
    "parse_error",
    "privacy_level",
    "private_queue",
]
PROJECT_ARTIFACT_TEXT = [
    "# li-12 project layout",
    "root runtime files",
    "python -m py_compile",
    "from pathlib import",
    "workingdirectory=",
    "execstart=",
    "systemctl",
    "journalctl",
]
EMPTY_STATE = "No usable actual records found for today."
PY_COMPILE_COMMAND = [
    sys.executable,
    "-m",
    "py_compile",
    "li12_unified_dashboard.py",
    "dashboard_data_loader.py",
    "dashboard_insights.py",
    "dashboard_privacy.py",
    "dashboard_components.py",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")


def audit_required_functions() -> None:
    found: set[str] = set()
    for path in DASHBOARD_FILES:
        tree = ast.parse(read(path), filename=str(path))
        found.update(node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
    missing = [name for name in REQUIRED_FUNCTIONS if name not in found]
    if missing:
        fail(f"missing required dashboard functions: {', '.join(missing)}")


def audit_no_disallowed_today_patterns() -> None:
    combined = "\n".join(read(path).lower() for path in DASHBOARD_FILES)
    for pattern in DISALLOWED_TODAY_PATTERNS:
        if pattern in combined:
            fail(f"disallowed today-data pattern found: {pattern}")


def _render_today_evidence_body() -> str:
    path = ROOT / "dashboard_components.py"
    tree = ast.parse(read(path), filename=str(path))
    source = read(path)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "render_today_evidence":
            return ast.get_source_segment(source, node) or ""
    fail("render_today_evidence function not found")


def audit_evidence_render_path() -> None:
    body = _render_today_evidence_body()
    for field in FORBIDDEN_RENDER_FIELDS:
        if re.search(rf"[\"']{re.escape(field)}[\"']", body):
            fail(f"today evidence rendering path references forbidden field: {field}")


def audit_empty_state() -> None:
    if EMPTY_STATE not in "\n".join(read(path) for path in DASHBOARD_FILES):
        fail("exact empty-state message is missing")


def audit_no_container_width() -> None:
    for path in DASHBOARD_FILES:
        if "use_container_width" in read(path):
            fail(f"use_container_width found in {path.relative_to(ROOT)}")


def audit_normalized_records(records: list[dict[str, object]], inventory: dict[str, object]) -> None:
    for record in records:
        record_type = str(record.get("record_type", "")).lower()
        excerpt = str(record.get("excerpt", "")).lower()
        if record_type in {"journal", "bridge"} and any(marker in excerpt for marker in PROJECT_ARTIFACT_TEXT):
            fail("normalized records include project/source artifacts as journal or bridge records")
    if int(inventory.get("candidate_chat_message_files_count", 0) or 0) > 0 and int(inventory.get("chat_records_count", 0) or 0) == 0:
        fail("candidate chat/message files exist but chat record count is zero")
    if bool(inventory.get("imported_sources_exists")) and not bool(inventory.get("imported_sources_scanned")):
        fail("data/imported_sources exists but was not scanned")


def audit_py_compile() -> None:
    result = subprocess.run(PY_COMPILE_COMMAND, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        fail(f"py_compile failed: {output}")


def print_inventory(inventory: dict[str, object]) -> None:
    print(f"candidate source files scanned: {inventory.get('candidate_source_files_scanned', 0)}")
    print(f"rejected system/project files count: {inventory.get('rejected_system_project_files_count', 0)}")
    print(f"normalized records total: {inventory.get('normalized_records_total', 0)}")
    print(f"records by type: {inventory.get('records_by_type', {})}")
    print(f"records by profile: {inventory.get('records_by_profile', {})}")
    print(f"chat records count: {inventory.get('chat_records_count', 0)}")
    print(f"journal records count: {inventory.get('journal_records_count', 0)}")
    print(f"memory records count: {inventory.get('memory_records_count', 0)}")


def main() -> None:
    audit_required_functions()
    audit_no_disallowed_today_patterns()
    audit_evidence_render_path()
    audit_empty_state()
    audit_no_container_width()
    inventory = get_record_inventory()
    records = load_cached_normalized_records()
    print_inventory(inventory)
    audit_normalized_records(records, inventory)
    audit_py_compile()
    print("PASS: dashboard source audit passed")


if __name__ == "__main__":
    main()
