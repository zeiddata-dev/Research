"""Deterministic relationship rating for today's Li-12 dashboard records."""
from __future__ import annotations

from collections import Counter
from datetime import datetime
import re
from typing import Any

from dashboard_privacy import safe_excerpt

SIGNAL_PATTERNS = {
    "repair": ["sorry", "apologize", "i hear you", "i understand", "i’ll change", "i'll change", "i will do", "i can do that", "i’ll handle", "i'll handle", "i’ll fix", "i'll fix", "thank you for telling me"],
    "stability": ["calm", "stable", "steady", "consistent", "grounded", "peaceful", "patient", "listened", "respectful", "safe"],
    "follow_through": ["done", "completed", "fixed", "handled", "followed through", "took care of", "scheduled", "delivered", "sent", "updated", "cleaned up"],
    "escalation": ["yelling", "angry", "hostile", "fight", "arguing", "pressure", "spiraling", "blow up", "upset", "intense", "overwhelmed"],
    "open_loop": ["again", "same thing", "still unresolved", "keeps happening", "repeated", "loop", "not fixed", "open issue", "unresolved", "waiting"],
    "over_explaining": ["over-explain", "over explain", "too many words", "long message", "paragraphs", "clarify harder", "explain again", "repeating myself", "keep explaining"],
}

SIGNAL_META = {
    "repair": ("Repair attempts", "Evidence suggests someone tried to acknowledge, apologize, or move toward repair.", "Name the repair once, then choose one concrete next step."),
    "stability": ("Stability signals", "Possible signal of calm, respect, consistency, or emotional steadiness.", "Protect the steady pattern and avoid adding extra pressure."),
    "follow_through": ("Follow-through signals", "Evidence suggests an action was completed or moved forward today.", "Confirm what is done and keep the next action small."),
    "escalation": ("Escalation signals", "Possible signal of tension, pressure, intensity, or conflict in today's records.", "Pause escalation and use one short, practical message if a response is needed."),
    "open_loop": ("Open loops and repeated topics", "Evidence suggests something repeated, remained unresolved, or is still waiting.", "Pick one open loop and define the next owner or time."),
    "over_explaining": ("Over-explaining signals", "Possible signal that clarity was attempted with too many words or repeated explanation.", "Shorten the message and ask for one specific outcome."),
    "late_night_intensity": ("Late-night intensity", "A late-night record also carried tension, apology-loop, over-explaining, or unresolved-loop signals.", "Avoid solving heavy topics late at night; park it for a clearer time."),
}

SCORING = {
    "repair": (8, 20),
    "stability": (6, 18),
    "follow_through": (10, 20),
    "escalation": (-10, -30),
    "open_loop": (-7, -21),
    "late_night_intensity": (-8, -16),
    "over_explaining": (-5, -15),
}


def _contains_pattern(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(re.search(r"(?<!\w)" + re.escape(pattern.lower()) + r"(?!\w)", lowered) for pattern in patterns)


def _label_for_score(score: int, has_records: bool) -> str:
    if not has_records:
        return "Not enough data"
    if score >= 80:
        return "Stable"
    if score >= 60:
        return "Repairing"
    if score >= 40:
        return "Heavy"
    if score >= 20:
        return "Tense"
    return "Escalating"


def _confidence(count: int) -> str:
    if count >= 10:
        return "high"
    if count >= 4:
        return "medium"
    if count >= 1:
        return "low"
    return "not enough data"


def _record_hour(record: dict[str, Any]) -> int | None:
    timestamp = record.get("timestamp_dt")
    if isinstance(timestamp, datetime):
        return timestamp.hour
    text = str(record.get("timestamp", ""))
    try:
        return datetime.fromisoformat(text).hour
    except ValueError:
        return None


def _detect_record_signals(record: dict[str, Any]) -> set[str]:
    text = str(record.get("analysis_text") or record.get("excerpt") or "")
    signals = {name for name, patterns in SIGNAL_PATTERNS.items() if _contains_pattern(text, patterns)}
    hour = _record_hour(record)
    late = hour is not None and (hour >= 22 or hour <= 4)
    if late and signals.intersection({"escalation", "repair", "open_loop", "over_explaining"}):
        signals.add("late_night_intensity")
    return signals


def build_today_relationship_rating(today_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a deterministic 0-100 relationship weather rating from actual records."""
    if not today_records:
        return {"score": None, "label": "Not enough data", "confidence": "not enough data", "evidence_count": 0, "signals": [], "evidence": []}

    signal_records: dict[str, list[dict[str, Any]]] = {name: [] for name in SCORING}
    evidence: list[dict[str, Any]] = []
    for record in today_records:
        clean_record = {
            "timestamp": record.get("timestamp", ""),
            "profile": record.get("profile", ""),
            "record_type": record.get("record_type", "record"),
            "excerpt": safe_excerpt(record.get("excerpt", "")),
        }
        detected = _detect_record_signals(record)
        if detected:
            evidence.append({**clean_record, "signals": sorted(detected)})
        for signal in detected:
            if signal in signal_records:
                signal_records[signal].append(clean_record)

    score = 60
    score_parts: dict[str, int] = {}
    for signal, records in signal_records.items():
        each, cap = SCORING[signal]
        raw_delta = each * len(records)
        delta = min(raw_delta, cap) if each > 0 else max(raw_delta, cap)
        score += delta
        score_parts[signal] = delta
    score = max(0, min(100, score))

    signal_cards: list[dict[str, Any]] = []
    for signal, records in signal_records.items():
        if not records:
            continue
        title, explanation, action = SIGNAL_META[signal]
        count = len(records)
        signal_cards.append({
            "key": signal,
            "title": title,
            "explanation": explanation,
            "confidence": _confidence(count),
            "evidence_count": count,
            "excerpts": [safe_excerpt(item.get("excerpt", ""), 180) for item in records[:3]],
            "suggested_next_action": action,
        })

    signal_cards.sort(key=lambda item: item["evidence_count"], reverse=True)
    evidence_count = len(today_records)
    return {
        "score": score,
        "label": _label_for_score(score, True),
        "confidence": _confidence(evidence_count),
        "evidence_count": evidence_count,
        "signals": signal_cards,
        "evidence": evidence[:10],
        "score_parts": score_parts,
        "input_counts": dict(Counter(record.get("record_type", "record") for record in today_records)),
    }


def build_today_bridge_summary(today_records: list[dict[str, Any]], rating: dict[str, Any]) -> str:
    """Return a 2-4 sentence summary using careful, non-diagnostic wording."""
    if not today_records:
        return "No usable actual records found for today."
    label = rating.get("label", "Not enough data")
    signals = [signal.get("title", "").lower() for signal in rating.get("signals", [])[:3]]
    if signals:
        signal_text = ", ".join(signals)
        first = f"Based on today’s records, evidence suggests activity around {signal_text}."
    else:
        first = "Based on today’s records, there is activity today but not enough evidence for a strong signal."
    second = f"The emotional weather reads as {label}, with {rating.get('confidence', 'not enough data')} confidence."
    if label in {"Stable", "Repairing"}:
        third = "The next clean action is to protect what is working and choose one specific follow-through step."
    elif label == "Not enough data":
        third = "The next clean action is to wait for more actual evidence before drawing a conclusion."
    else:
        third = "The next clean action is to reduce pressure and handle only one open loop at a time."
    return " ".join([first, second, third])
