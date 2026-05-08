"""Strict actual-record loading and today filtering for the Li-12 dashboard."""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
from typing import Any, Iterable

try:  # Python 3.9+
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - old Python fallback
    ZoneInfo = None  # type: ignore[assignment]

from dashboard_privacy import sanitize_dashboard_record, safe_excerpt

DASHBOARD_TIMEZONE = "America/Chicago"
TEXT_FIELDS = ("text", "summary", "message", "content", "title", "insight", "excerpt", "description", "body", "entry", "reflection", "journal", "memory", "memories")
TIMESTAMP_FIELDS = ("timestamp", "created_at", "updated_at", "date", "datetime", "ts", "time")
TYPE_FIELDS = ("record_type", "type", "category", "kind", "source")
USER_FIELDS = ("profile", "profile_id", "user", "display_name", "name", "author", "sender", "username")

PREFERRED_SOURCE_DIRS = (
    Path("data/bot_profiles"),
    Path("data/journals"),
    Path("data/journal"),
    Path("data/memories"),
    Path("data/memory"),
    Path("data/chats"),
    Path("data/messages"),
    Path("data/telegram"),
    Path("data/bridge"),
    Path("data/bridge_digests"),
    Path("data/imported_sources"),
    Path("data/uploads"),
    Path("data/website_intake"),
)
ALLOWED_EXTENSIONS = {".json", ".jsonl", ".txt", ".md", ".csv"}
EXCLUDED_DIR_NAMES = {".git", ".venv", "venv", "__pycache__", "node_modules", "archive", "backups", "reports", "_maintenance", "_exports", "scripts"}
EXCLUDED_EXTENSIONS = {".py", ".sh", ".ps1", ".service", ".toml", ".yaml", ".yml", ".ini"}
EXCLUDED_NAME_TOKENS = ("project_layout", "layout", "inventory", "audit", "report", "codex", "prompt", "grep", "py_compile")
DASHBOARD_SOURCE_NAMES = {"li12_unified_dashboard.py", "dashboard_data_loader.py", "dashboard_insights.py", "dashboard_privacy.py", "dashboard_components.py", "audit_dashboard_sources.py"}
SYSTEM_ARTIFACT_PATTERNS = (
    "from pathlib import",
    "def ",
    "class ",
    "python -m py_compile",
    "grep -r",
    "# li-12 project layout",
    "generated:",
    "root runtime files",
    "workingdirectory=",
    "execstart=",
    "systemctl",
    "journalctl",
    "traceback",
    "file \"/home/ubuntu",
    ".py:",
    ".service",
)
CHAT_KEYS = {"message", "text", "chat_id", "sender", "user_id", "username", "display_name", "profile_id", "telegram", "conversation"}
JOURNAL_KEYS = {"journal", "entry", "reflection"}
MEMORY_KEYS = {"memory", "memories"}
BRIDGE_KEYS = {"bridge", "digest", "relationship"}


def _local_timezone(timezone_name: str = DASHBOARD_TIMEZONE):
    if ZoneInfo is not None:
        try:
            return ZoneInfo(timezone_name)
        except Exception:
            pass
    return timezone(timedelta(hours=-6), name=timezone_name)


def get_today_bounds(timezone_name: str = DASHBOARD_TIMEZONE) -> tuple[datetime, datetime]:
    """Return inclusive start and exclusive end for the current local day."""
    tz = _local_timezone(timezone_name)
    today = datetime.now(tz).date()
    start = datetime.combine(today, time.min, tzinfo=tz)
    end = start + timedelta(days=1)
    return start, end


def _parse_timestamp(value: Any, timezone_name: str = DASHBOARD_TIMEZONE) -> datetime | None:
    if value in (None, ""):
        return None
    tz = _local_timezone(timezone_name)
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime.combine(value, time.min)
    elif isinstance(value, (int, float)):
        try:
            parsed = datetime.fromtimestamp(float(value), tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    else:
        text = str(value).strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            parsed = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    parsed = datetime.strptime(text, fmt)
                    break
                except ValueError:
                    continue
            if parsed is None:
                return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def extract_record_timestamp(record: dict[str, Any], timezone_name: str = DASHBOARD_TIMEZONE) -> datetime | None:
    for field in TIMESTAMP_FIELDS:
        if field in record:
            parsed = _parse_timestamp(record.get(field), timezone_name)
            if parsed is not None:
                return parsed
    local_date = record.get("local_date") or record.get("day")
    if local_date:
        parsed = _parse_timestamp(local_date, timezone_name)
        if parsed is not None:
            return parsed
    return None


def _flatten_text(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value]
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            parts.extend(_flatten_text(item))
        return parts
    if isinstance(value, dict):
        return [str(value.get(field, "")) for field in TEXT_FIELDS if str(value.get(field, "")).strip()]
    return []


def extract_record_text(record: dict[str, Any]) -> str:
    parts: list[str] = []
    for field in TEXT_FIELDS:
        parts.extend(_flatten_text(record.get(field)))
    return safe_excerpt(" ".join(parts), max_chars=900)


def _path_parts(path: Path | None) -> set[str]:
    if path is None:
        return set()
    return {part.lower() for part in path.parts}


def _field_names(record: dict[str, Any]) -> set[str]:
    names = {str(key).lower() for key in record.keys()}
    for value in record.values():
        if isinstance(value, dict):
            names.update(str(key).lower() for key in value.keys())
    return names


def _source_kind(path: Path | None) -> str:
    parts = _path_parts(path)
    if parts.intersection({"chats", "messages", "telegram"}):
        return "chat"
    if parts.intersection({"journals", "journal"}):
        return "journal"
    if parts.intersection({"memories", "memory"}):
        return "memory"
    if parts.intersection({"bridge", "bridge_digests"}):
        return "bridge"
    return ""


def classify_record_type(record: dict[str, Any], source_path: Path | None = None) -> str:
    fields = _field_names(record)
    source_kind = _source_kind(source_path)
    type_text = " ".join(str(record.get(field, "")) for field in TYPE_FIELDS).lower()
    if source_kind:
        return source_kind
    if "insight" in type_text or "signal" in type_text:
        return "insight"
    if "bridge" in type_text or fields.intersection(BRIDGE_KEYS):
        return "bridge"
    if "memory" in type_text or fields.intersection(MEMORY_KEYS):
        return "memory"
    if "journal" in type_text or fields.intersection(JOURNAL_KEYS):
        return "journal"
    if any(token in type_text for token in ("chat", "telegram", "message", "conversation")) or fields.intersection(CHAT_KEYS):
        return "chat"
    return "record"


def extract_display_user(record: dict[str, Any]) -> str:
    for field in USER_FIELDS:
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            return safe_excerpt(value, max_chars=80)
        if isinstance(value, dict):
            for nested in ("display_name", "name", "profile", "profile_id", "user", "username"):
                nested_value = value.get(nested)
                if isinstance(nested_value, str) and nested_value.strip():
                    return safe_excerpt(nested_value, max_chars=80)
    return "Unassigned"


def _is_user_facing_record(record: dict[str, Any]) -> bool:
    type_text = " ".join(str(record.get(field, "")) for field in TYPE_FIELDS).lower()
    return not any(blocked in type_text for blocked in ("admin", "system", "backend", "debug", "internal"))


def _looks_like_system_artifact(text: str, source_path: Path | None) -> bool:
    lowered = text.lower()
    if not any(pattern in lowered for pattern in SYSTEM_ARTIFACT_PATTERNS):
        return False
    return _source_kind(source_path) not in {"chat", "journal", "memory"}


def _has_required_shape(record: dict[str, Any], record_type: str, source_path: Path | None) -> bool:
    fields = _field_names(record)
    source_kind = _source_kind(source_path)
    if record_type == "chat":
        return source_kind == "chat" or bool(fields.intersection(CHAT_KEYS))
    if record_type == "journal":
        return source_kind == "journal" or bool(fields.intersection(JOURNAL_KEYS))
    if record_type == "memory":
        return source_kind == "memory" or bool(fields.intersection(MEMORY_KEYS))
    if record_type == "bridge":
        return source_kind == "bridge" or bool(fields.intersection(BRIDGE_KEYS))
    if record_type == "insight":
        return "insight" in fields or "signal" in fields or "insight" in str(record).lower()
    return False


def normalize_display_record(record: Any, timezone_name: str = DASHBOARD_TIMEZONE, source_path: Path | None = None) -> dict[str, Any] | None:
    if not isinstance(record, dict):
        return None
    cleaned = sanitize_dashboard_record(record)
    if not isinstance(cleaned, dict) or not _is_user_facing_record(cleaned):
        return None
    timestamp = extract_record_timestamp(cleaned, timezone_name)
    text = extract_record_text(cleaned)
    if not timestamp or not text:
        return None
    record_type = classify_record_type(cleaned, source_path)
    if not _has_required_shape(cleaned, record_type, source_path):
        return None
    if record_type in {"journal", "bridge", "insight", "record"} and _looks_like_system_artifact(text, source_path):
        return None
    return {
        "timestamp": timestamp.isoformat(),
        "timestamp_dt": timestamp,
        "profile": extract_display_user(cleaned),
        "record_type": record_type,
        "excerpt": safe_excerpt(text),
        "analysis_text": text,
    }


def _iter_json_records(payload: Any) -> Iterable[Any]:
    if isinstance(payload, list):
        yield from payload
    elif isinstance(payload, dict):
        for key in ("records", "items", "data", "chats", "messages", "journals", "memories", "bridge", "digests", "insights", "conversation"):
            value = payload.get(key)
            if isinstance(value, list):
                yield from value
        if any(field in payload for field in TEXT_FIELDS) or _field_names(payload).intersection(CHAT_KEYS | JOURNAL_KEYS | MEMORY_KEYS | BRIDGE_KEYS):
            yield payload


def _read_text_file(path: Path) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    if not text.strip() or _is_traceback_only(text):
        return []
    source_kind = _source_kind(path)
    if source_kind not in {"chat", "journal", "memory", "bridge"} and not _content_has_user_record_markers(text):
        return []
    timestamp = datetime.fromtimestamp(path.stat().st_mtime, tz=_local_timezone()).isoformat()
    field = "message" if source_kind == "chat" else "entry" if source_kind == "journal" else "memory" if source_kind == "memory" else "summary"
    return [{"timestamp": timestamp, "record_type": source_kind or "insight", field: text}]


def _read_records_from_file(path: Path) -> list[Any]:
    if path.suffix.lower() in {".json", ".jsonl"}:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return []
        try:
            return list(_iter_json_records(json.loads(text)))
        except json.JSONDecodeError:
            records: list[Any] = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    records.extend(_iter_json_records(json.loads(line)))
                except json.JSONDecodeError:
                    continue
            return records
    return _read_text_file(path)


def _is_traceback_only(text: str) -> bool:
    lowered = text.strip().lower()
    return lowered.startswith("traceback") and "message" not in lowered and "journal" not in lowered and "memory" not in lowered


def _content_has_user_record_markers(text: str) -> bool:
    lowered = text.lower()
    markers = ("chat_id", "sender", "telegram", "journal", "reflection", "memory", "relationship", "bridge", "message")
    return any(marker in lowered for marker in markers)


def _path_excluded(path: Path) -> bool:
    lowered_name = path.name.lower()
    if path.name in DASHBOARD_SOURCE_NAMES:
        return True
    if path.suffix.lower() in EXCLUDED_EXTENSIONS:
        return True
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return True
    if any(part.lower() in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    return any(token in lowered_name for token in EXCLUDED_NAME_TOKENS)


def discover_candidate_source_files(root: Path = Path(".")) -> tuple[list[Path], dict[str, Any]]:
    """Find allowlisted user-data files only; never scan repo docs/source trees."""
    candidates: list[Path] = []
    rejected = 0
    scanned_dirs: list[str] = []
    imported_sources_exists = (root / "data/imported_sources").exists()
    imported_sources_scanned = False
    for rel_dir in PREFERRED_SOURCE_DIRS:
        directory = root / rel_dir
        if not directory.exists() or not directory.is_dir():
            continue
        scanned_dirs.append(rel_dir.as_posix())
        if rel_dir.as_posix() == "data/imported_sources":
            imported_sources_scanned = True
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            if _path_excluded(path.relative_to(root)):
                rejected += 1
                continue
            candidates.append(path)
    candidates = sorted(set(candidates))
    chat_candidates = [path for path in candidates if _source_kind(path.relative_to(root)) == "chat"]
    inventory = {
        "candidate_source_files_scanned": len(candidates),
        "candidate_chat_message_files_count": len(chat_candidates),
        "rejected_system_project_files_count": rejected,
        "actual_source_directories_scanned": scanned_dirs,
        "imported_sources_exists": imported_sources_exists,
        "imported_sources_scanned": imported_sources_scanned,
        "top_candidate_files": [_safe_relpath(path, root) for path in candidates[:12]],
    }
    return candidates, inventory


def _safe_relpath(path: Path, root: Path = Path(".")) -> str:
    try:
        return safe_excerpt(path.relative_to(root).as_posix(), max_chars=160)
    except ValueError:
        return safe_excerpt(path.name, max_chars=160)


def load_records_with_inventory(root: Path = Path("."), timezone_name: str = DASHBOARD_TIMEZONE) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates, inventory = discover_candidate_source_files(root)
    records: list[dict[str, Any]] = []
    rejected_records = 0
    for path in candidates:
        raw_records = _read_records_from_file(path)
        for raw_record in raw_records:
            normalized = normalize_display_record(raw_record, timezone_name, path.relative_to(root))
            if normalized is None:
                rejected_records += 1
                continue
            records.append(normalized)
    by_type = Counter(record.get("record_type", "record") for record in records)
    by_profile = Counter(record.get("profile", "Unassigned") or "Unassigned" for record in records)
    inventory.update({
        "normalized_records_total": len(records),
        "records_by_type": dict(sorted(by_type.items())),
        "records_by_profile": dict(by_profile.most_common(10)),
        "chat_records_count": by_type.get("chat", 0),
        "journal_records_count": by_type.get("journal", 0),
        "memory_records_count": by_type.get("memory", 0),
        "bridge_records_count": by_type.get("bridge", 0),
        "rejected_normalized_records_count": rejected_records,
    })
    return records, inventory


def load_cached_normalized_records() -> list[dict[str, Any]]:
    """Load actual user-facing records from strict allowlisted source directories."""
    records, _inventory = load_records_with_inventory()
    return records


def get_record_inventory() -> dict[str, Any]:
    """Return safe loader inventory counts for CLI audit/debug output."""
    _records, inventory = load_records_with_inventory()
    return inventory


def filter_records_for_today(records: Iterable[Any], timezone_name: str = DASHBOARD_TIMEZONE) -> list[dict[str, Any]]:
    """Return usable records with valid timestamps inside today's local bounds."""
    start, end = get_today_bounds(timezone_name)
    today_records: list[dict[str, Any]] = []
    for record in records or []:
        normalized = record if isinstance(record, dict) and "timestamp_dt" in record else normalize_display_record(record, timezone_name)
        if normalized is None:
            continue
        timestamp = normalized.get("timestamp_dt")
        if isinstance(timestamp, datetime) and start <= timestamp < end:
            today_records.append(normalized)
    today_records.sort(key=lambda item: item.get("timestamp_dt") or start)
    return today_records
