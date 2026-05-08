"""Privacy helpers for the Li-12 dashboard.

The dashboard must render only display-safe fields. These helpers remove backend
metadata recursively before any record is converted into user-facing evidence.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
import re
from typing import Any

FORBIDDEN_DASHBOARD_KEYS = {
    "source_file",
    "record_hash",
    "imported_path",
    "raw",
    "parse_error",
    "privacy_level",
    "private_queue",
    "backend",
    "backend_fields",
    "debug",
    "env",
    "environment",
}

_SECRET_LIKE = re.compile(
    r"(?i)(api[_-]?key|bot[_-]?token|secret|password|passwd|bearer\s+[a-z0-9._\-]+|sk-[a-z0-9])"
)
_PATH_LIKE = re.compile(r"(?:/[^\s]{2,}|[A-Za-z]:\\\\[^\s]+)")
_WHITESPACE = re.compile(r"\s+")


def sanitize_display_value(value: Any) -> str:
    """Return a short, display-safe string without secrets or file paths."""
    if value is None:
        return ""
    text = str(value)
    text = _SECRET_LIKE.sub("[redacted]", text)
    text = _PATH_LIKE.sub("[path hidden]", text)
    return _WHITESPACE.sub(" ", text).strip()


def sanitize_dashboard_record(record: Any) -> Any:
    """Remove forbidden dashboard keys recursively from records before rendering."""
    if isinstance(record, Mapping):
        cleaned: dict[str, Any] = {}
        for key, value in record.items():
            key_text = str(key)
            if key_text.lower() in FORBIDDEN_DASHBOARD_KEYS:
                continue
            cleaned[key_text] = sanitize_dashboard_record(value)
        return cleaned
    if isinstance(record, Sequence) and not isinstance(record, (str, bytes, bytearray)):
        return [sanitize_dashboard_record(item) for item in record]
    if isinstance(record, str):
        return sanitize_display_value(record)
    return record


def safe_excerpt(text: Any, max_chars: int = 240) -> str:
    """Return a clean excerpt suitable for Rebecca-facing dashboard evidence."""
    cleaned = sanitize_display_value(text)
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[: max_chars - 1].rstrip() + "…"
