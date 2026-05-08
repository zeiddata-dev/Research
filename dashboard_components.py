"""Streamlit rendering components and learning intake for the Li-12 dashboard."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dashboard_privacy import sanitize_dashboard_record, safe_excerpt
from dashboard_insights import (
    build_behavior_correlations,
    build_conversation_balance,
    build_followthrough_tracker,
    build_late_night_risk,
    build_loop_detector,
    build_repair_radar,
    build_word_count_per_user,
)

EMPTY_TODAY_MESSAGE = "No usable actual records found for today."
LEARNING_ROOTS = {
    "website": Path("data/website_intake"),
    "training": Path("data/training_queue"),
    "approved": Path("data/approved_learning"),
}


def _st():
    import streamlit as st
    return st


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_id(payload: dict[str, Any]) -> str:
    clean = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def _role_key(role: str) -> str:
    return safe_excerpt(role, 40).lower().replace(" ", "_") or "rebecca"


def _append_jsonl(path: Path, item: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
    return item


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    items: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            safe = sanitize_dashboard_record(payload)
            if isinstance(safe, dict):
                items.append(safe)
    return items


def queue_website_intake(url: str, submitted_by: str, tags: list[str] | None = None, note: str | None = None) -> dict[str, Any]:
    """Save a URL for later review; this does not fetch remote content."""
    parsed = urlparse(str(url).strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Enter a valid http or https URL.")
    role = _role_key(submitted_by)
    item = {
        "timestamp": _now_iso(),
        "submitted_by": role,
        "source_type": "website_intake",
        "url": str(url).strip(),
        "note": safe_excerpt(note or "", 500),
        "tags": [safe_excerpt(tag, 80) for tag in (tags or []) if safe_excerpt(tag, 80)],
        "review_status": "pending_review",
    }
    item["stable_id"] = _stable_id(item)
    path = LEARNING_ROOTS["website"] / role / "website_intake_queue.jsonl"
    return _append_jsonl(path, item)


def queue_training_note(note: str, submitted_by: str, tags: list[str] | None = None) -> dict[str, Any]:
    """Save a training note for review; notes are not trusted memories automatically."""
    clean_note = safe_excerpt(note, 1000)
    if not clean_note:
        raise ValueError("Training note cannot be empty.")
    role = _role_key(submitted_by)
    item = {
        "timestamp": _now_iso(),
        "submitted_by": role,
        "source_type": "training_note",
        "note": clean_note,
        "tags": [safe_excerpt(tag, 80) for tag in (tags or []) if safe_excerpt(tag, 80)],
        "review_status": "pending_review",
    }
    item["stable_id"] = _stable_id(item)
    path = LEARNING_ROOTS["training"] / role / "training_notes.jsonl"
    return _append_jsonl(path, item)


def _learning_paths(role: str) -> list[Path]:
    role_key = _role_key(role)
    paths = list(LEARNING_ROOTS["website"].glob("*/website_intake_queue.jsonl")) + list(LEARNING_ROOTS["training"].glob("*/training_notes.jsonl"))
    paths += list(LEARNING_ROOTS["approved"].glob("*/approved_learning.jsonl"))
    if role_key != "admin":
        paths = [path for path in paths if role_key in path.parts]
    return paths


def load_learning_items(role: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in _learning_paths(role):
        for item in _read_jsonl(path):
            visible = _role_key(role) == "admin" or item.get("submitted_by") == _role_key(role)
            if visible:
                items.append(item)
    items.sort(key=lambda item: str(item.get("timestamp", "")), reverse=True)
    return items


def _update_learning_item(item_id: str, status: str, admin_note: str | None = None) -> dict[str, Any] | None:
    for path in _learning_paths("admin"):
        items = _read_jsonl(path)
        changed = False
        for item in items:
            if item.get("stable_id") == item_id:
                item["review_status"] = status
                if admin_note:
                    item["admin_note"] = safe_excerpt(admin_note, 500)
                item["reviewed_at"] = _now_iso()
                changed = True
                if status == "approved":
                    approved_role = _role_key(str(item.get("submitted_by", "rebecca")))
                    approved_path = LEARNING_ROOTS["approved"] / approved_role / "approved_learning.jsonl"
                    _append_jsonl(approved_path, item)
        if changed:
            path.write_text("".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in items), encoding="utf-8")
            return next((item for item in items if item.get("stable_id") == item_id), None)
    return None


def approve_learning_item(item_id: str, admin_note: str | None = None) -> dict[str, Any] | None:
    return _update_learning_item(item_id, "approved", admin_note)


def reject_learning_item(item_id: str, admin_note: str | None = None) -> dict[str, Any] | None:
    return _update_learning_item(item_id, "rejected", admin_note)


def _rating_color(label: str) -> str:
    if label in {"Calm", "Stable"}:
        return "#39ff88"
    if label == "Repairing":
        return "#15d7ff"
    if label == "Heavy":
        return "#d8a21b"
    if label in {"Tense", "Escalating"}:
        return "#ff4d4d"
    return "#8b949e"


def render_daily_emotions_report(report: dict[str, Any], role: str) -> None:
    st = _st()
    st.markdown("## Daily Emotions Report")
    score = report.get("score")
    if score is None:
        st.info(EMPTY_TODAY_MESSAGE)
        return
    label = str(report.get("weather", "Not enough data"))
    confidence = str(report.get("confidence", "not enough data"))
    evidence_count = int(report.get("evidence_count") or 0)
    color = _rating_color(label)
    st.markdown(
        f"""
        <div style="background:#0d1117;border:1px solid #30363d;border-radius:16px;padding:22px;color:#f0f6fc;margin-bottom:14px;">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:18px;">
            <div>
              <div style="color:#8b949e;font-size:13px;text-transform:uppercase;letter-spacing:.08em;">Relationship Weather</div>
              <div style="font-size:34px;font-weight:800;color:{color};">{label}</div>
            </div>
            <div style="text-align:right;">
              <div style="color:#8b949e;font-size:13px;text-transform:uppercase;letter-spacing:.08em;">Relationship Score</div>
              <div style="font-size:56px;font-weight:900;line-height:1;color:{color};">{int(score)}</div>
            </div>
          </div>
          <div style="height:12px;background:#21262d;border-radius:999px;margin:18px 0 10px 0;overflow:hidden;">
            <div style="height:12px;width:{int(score)}%;background:{color};border-radius:999px;"></div>
          </div>
          <div style="color:#c9d1d9;font-size:14px;">confidence: {confidence} · evidence count: {evidence_count}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    summary = safe_excerpt(report.get("summary", ""), 900)
    if summary:
        st.write(summary)
    advice = [safe_excerpt(item, 180) for item in report.get("advice", []) if safe_excerpt(item, 180)]
    if advice:
        st.markdown("#### Advice to improve today")
        for item in advice[:3]:
            st.markdown(f"- {item}")
    signals = report.get("signals", [])
    if signals:
        st.markdown("#### Top signal badges")
        badges = " ".join(f"`{safe_excerpt(signal.get('title', ''), 40)}`" for signal in signals[:8] if signal.get("evidence_count"))
        if badges:
            st.markdown(badges)
    evidence = report.get("evidence", [])
    if evidence:
        with st.expander("Why Li-12 thinks this"):
            for item in evidence[:10]:
                parts = [safe_excerpt(item.get("timestamp", ""), 40), safe_excerpt(item.get("profile", ""), 80), safe_excerpt(item.get("record_type", "record"), 40)]
                parts = [part for part in parts if part]
                st.markdown(f"**{' · '.join(parts)}**")
                st.write(safe_excerpt(item.get("excerpt", ""), 240))


def render_today_rating_card(rating: dict[str, Any]) -> None:
    render_daily_emotions_report({"score": rating.get("score"), "weather": rating.get("label"), "confidence": rating.get("confidence"), "evidence_count": rating.get("evidence_count"), "summary": "", "advice": [], "signals": rating.get("signals", []), "evidence": rating.get("evidence", [])}, "rebecca")


def render_today_inputs(today_records: list[dict[str, Any]]) -> None:
    st = _st()
    labels = {"chat": "chats today", "journal": "journals today", "memory": "memories today", "bridge": "bridge records today", "insight": "insight signals today"}
    counts = {key: 0 for key in labels}
    for record in today_records:
        record_type = str(record.get("record_type", "record")).lower()
        if record_type in counts:
            counts[record_type] += 1
    nonzero = [(key, count) for key, count in counts.items() if count]
    if not nonzero:
        return
    st.markdown("### Today’s Inputs")
    columns = st.columns(len(nonzero))
    for column, (key, count) in zip(columns, nonzero):
        with column:
            st.metric(labels[key], count)


def render_today_signals(today_records: list[dict[str, Any]], rating: dict[str, Any] | None = None) -> None:
    st = _st()
    if rating is None:
        from dashboard_insights import build_today_relationship_rating
        rating = build_today_relationship_rating(today_records)
    signals = rating.get("signals", [])
    if not signals:
        return
    st.markdown("### Top Signals Today")
    for signal in signals:
        st.markdown(f"**{safe_excerpt(signal.get('title', 'Signal'), 80)}**  \n{safe_excerpt(signal.get('explanation', ''), 220)}  \nconfidence: {safe_excerpt(signal.get('confidence', ''), 40)} · evidence count: {int(signal.get('evidence_count') or 0)}")
        for excerpt in signal.get("excerpts", [])[:3]:
            clean = safe_excerpt(excerpt, 180)
            if clean:
                st.caption(clean)
        action = safe_excerpt(signal.get("suggested_next_action", ""), 180)
        if action:
            st.caption(f"Suggested next action: {action}")


def render_today_evidence(today_records: list[dict[str, Any]], rating: dict[str, Any] | None = None, limit: int = 10) -> None:
    st = _st()
    if rating is None:
        from dashboard_insights import build_today_relationship_rating
        rating = build_today_relationship_rating(today_records)
    evidence = rating.get("evidence") or today_records[:limit]
    if not evidence:
        return
    with st.expander("Why Li-12 thinks this"):
        for item in evidence[:limit]:
            parts = [safe_excerpt(item.get("timestamp", ""), 40), safe_excerpt(item.get("profile", ""), 80), safe_excerpt(item.get("record_type", "record"), 40)]
            parts = [part for part in parts if part]
            excerpt = safe_excerpt(item.get("excerpt", ""), 240)
            if excerpt:
                st.markdown(f"**{' · '.join(parts)}**")
                st.write(excerpt)


def render_word_count_widget(records: list[dict[str, Any]]) -> None:
    st = _st()
    data = build_word_count_per_user(records)
    if not data:
        return
    st.markdown("### Word Count Per User")
    rows = data.get("rows", [])
    st.bar_chart({row["user"]: row["total_words"] for row in rows})
    st.table(rows)
    if data.get("longest_message_signal"):
        st.caption(safe_excerpt(data["longest_message_signal"], 180))
    if data.get("imbalance_signal"):
        st.caption(safe_excerpt(data["imbalance_signal"], 180))


def render_behavior_correlation_widget(records: list[dict[str, Any]]) -> None:
    st = _st()
    correlations = build_behavior_correlations(records)
    if not correlations:
        return
    st.markdown("### Behavior Correlation")
    for item in correlations:
        st.markdown(f"**{safe_excerpt(item.get('name', ''), 100)}**  \nDirection: {safe_excerpt(item.get('direction', ''), 40)} · confidence: {safe_excerpt(item.get('confidence', ''), 40)} · evidence count: {int(item.get('evidence_count') or 0)}")
        st.write(safe_excerpt(item.get("explanation", ""), 240))
        for excerpt in item.get("excerpts", [])[:3]:
            if excerpt:
                st.caption(safe_excerpt(excerpt, 180))
        st.caption("Correlation is not causation.")


def render_relationship_widgets(records: list[dict[str, Any]]) -> None:
    st = _st()
    widgets = [
        build_conversation_balance(records),
        build_repair_radar(records),
        build_loop_detector(records),
        build_late_night_risk(records),
        build_followthrough_tracker(records),
    ]
    widgets = [widget for widget in widgets if widget]
    if not widgets:
        return
    st.markdown("### Relationship Widgets")
    for widget in widgets:
        st.markdown(f"**{safe_excerpt(widget.get('title', ''), 80)}**")
        for key, value in widget.items():
            if key in {"title", "rows", "excerpts", "top_terms"} or value in (None, "", [], {}):
                continue
            st.caption(f"{key.replace('_', ' ')}: {safe_excerpt(value, 160)}")
        if widget.get("top_terms"):
            st.caption(f"top repeated terms: {widget['top_terms']}")
        for excerpt in widget.get("excerpts", [])[:3]:
            st.caption(safe_excerpt(excerpt, 160))


def _render_learning_items(items: list[dict[str, Any]], status: str, role: str) -> None:
    st = _st()
    visible = [item for item in items if item.get("review_status") == status]
    if not visible:
        return
    for item in visible[:50]:
        title = safe_excerpt(item.get("url") or item.get("note") or item.get("source_type") or "Learning item", 120)
        st.markdown(f"**{title}**")
        st.caption(f"submitted by: {safe_excerpt(item.get('submitted_by', ''), 60)} · status: {safe_excerpt(item.get('review_status', ''), 40)}")
        if _role_key(role) == "admin" and status == "pending_review":
            col1, col2 = st.columns(2)
            item_id = str(item.get("stable_id", ""))
            with col1:
                if st.button(f"Approve {item_id[:8]}", key=f"approve_{item_id}"):
                    approve_learning_item(item_id)
                    st.success("Approved.")
            with col2:
                if st.button(f"Reject {item_id[:8]}", key=f"reject_{item_id}"):
                    reject_learning_item(item_id)
                    st.success("Rejected.")


def render_learning_page(role: str) -> None:
    st = _st()
    st.title("Learning")
    tabs = st.tabs(["URL Fetcher", "Training Notes", "Pending Review", "Approved Learning", "Rejected / Ignored"])
    role_key = _role_key(role)
    with tabs[0]:
        with st.form("url_fetcher_form"):
            url = st.text_input("URL")
            note = st.text_input("Note")
            tags = st.text_input("Tags, comma-separated")
            submitted = st.form_submit_button("Submit for review")
            if submitted:
                try:
                    queue_website_intake(url, role_key, [tag.strip() for tag in tags.split(",") if tag.strip()], note)
                    st.success("Saved for review.")
                except ValueError as exc:
                    st.warning(str(exc))
    with tabs[1]:
        with st.form("training_notes_form"):
            note = st.text_area("Training note")
            tags = st.text_input("Tags, comma-separated", key="training_tags")
            submitted = st.form_submit_button("Save training note")
            if submitted:
                try:
                    queue_training_note(note, role_key, [tag.strip() for tag in tags.split(",") if tag.strip()])
                    st.success("Saved for review.")
                except ValueError as exc:
                    st.warning(str(exc))
    items = load_learning_items(role_key)
    with tabs[2]:
        _render_learning_items(items, "pending_review", role_key)
    with tabs[3]:
        _render_learning_items(items, "approved", role_key)
    with tabs[4]:
        rejected = [item for item in items if item.get("review_status") in {"rejected", "ignored"}]
        if rejected:
            for item in rejected[:50]:
                st.markdown(f"**{safe_excerpt(item.get('url') or item.get('note') or 'Learning item', 120)}**")
                st.caption(f"status: {safe_excerpt(item.get('review_status', ''), 40)}")
