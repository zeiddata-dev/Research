"""Streamlit rendering components for the Li-12 today bridge dashboard."""
from __future__ import annotations

from typing import Any

from dashboard_privacy import safe_excerpt

EMPTY_TODAY_MESSAGE = "No usable actual records found for today."


def _st():
    import streamlit as st
    return st


def _rating_color(label: str) -> str:
    if label == "Stable":
        return "#39ff88"
    if label == "Repairing":
        return "#15d7ff"
    if label == "Heavy":
        return "#d8a21b"
    if label in {"Tense", "Escalating"}:
        return "#ff4d4d"
    return "#8b949e"


def render_today_rating_card(rating: dict[str, Any]) -> None:
    st = _st()
    label = str(rating.get("label") or "Not enough data")
    score = rating.get("score")
    evidence_count = int(rating.get("evidence_count") or 0)
    confidence = str(rating.get("confidence") or "not enough data")
    if score is None:
        st.info(EMPTY_TODAY_MESSAGE)
        return
    color = _rating_color(label)
    st.markdown("### Today’s Emotional Weather")
    st.markdown(
        f"""
        <div style="background:#0d1117;border:1px solid #30363d;border-radius:14px;padding:18px 20px;color:#f0f6fc;">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
            <div style="font-size:54px;font-weight:800;line-height:1;color:{color};">{int(score)}</div>
            <div style="border:1px solid {color};color:{color};border-radius:999px;padding:5px 12px;font-weight:700;">{label}</div>
          </div>
          <div style="height:10px;background:#21262d;border-radius:999px;margin:16px 0 12px 0;overflow:hidden;">
            <div style="height:10px;width:{int(score)}%;background:{color};border-radius:999px;"></div>
          </div>
          <div style="color:#c9d1d9;font-size:14px;">confidence: {confidence} · evidence count: {evidence_count}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
        st.markdown(
            f"**{safe_excerpt(signal.get('title', 'Signal'), 80)}**  \n"
            f"{safe_excerpt(signal.get('explanation', ''), 220)}  \n"
            f"confidence: {safe_excerpt(signal.get('confidence', ''), 40)} · evidence count: {int(signal.get('evidence_count') or 0)}"
        )
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
    with st.expander("View evidence behind today’s rating"):
        for item in evidence[:limit]:
            parts = []
            timestamp = safe_excerpt(item.get("timestamp", ""), 40)
            profile = safe_excerpt(item.get("profile", ""), 80)
            record_type = safe_excerpt(item.get("record_type", "record"), 40)
            excerpt = safe_excerpt(item.get("excerpt", ""), 240)
            if timestamp:
                parts.append(timestamp)
            if profile:
                parts.append(profile)
            if record_type:
                parts.append(record_type)
            if excerpt:
                st.markdown(f"**{' · '.join(parts)}**")
                st.write(excerpt)
