"""Deterministic relationship analytics for the Li-12 dashboard."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re
from typing import Any

from dashboard_privacy import safe_excerpt

SIGNAL_PATTERNS = {
    "repair": ["sorry", "apologize", "i hear you", "i understand", "i’ll change", "i'll change", "i will do", "i can do that", "i’ll handle", "i'll handle", "i’ll fix", "i'll fix", "thank you for telling me"],
    "stability": ["calm", "stable", "steady", "consistent", "grounded", "peaceful", "patient", "listened", "respectful", "safe"],
    "follow_through": ["done", "completed", "fixed", "handled", "followed through", "took care of", "delivered", "sent", "updated", "cleaned up"],
    "escalation": ["yelling", "angry", "hostile", "fight", "arguing", "pressure", "spiraling", "blow up", "upset", "intense", "overwhelmed"],
    "open_loop": ["again", "same thing", "still unresolved", "keeps happening", "repeated", "loop", "not fixed", "open issue", "unresolved", "waiting"],
    "over_explaining": ["over-explain", "over explain", "too many words", "long message", "paragraphs", "clarify harder", "explain again", "repeating myself", "keep explaining"],
    "supportive": ["thank you", "appreciate", "proud of", "i care", "i love", "support", "kind", "gentle", "you matter", "i’m here", "i'm here"],
    "hostile_absolute": ["always", "never", "nothing changes", "you don’t care", "you don't care", "whatever", "shut down", "hate", "done with this"],
}

SIGNAL_META = {
    "repair": ("Repair attempt", "Evidence suggests someone tried to acknowledge, apologize, or move toward repair.", "Acknowledge repair once, then act."),
    "stability": ("Stability signal", "Possible signal of calm, respect, consistency, or emotional steadiness.", "Protect what is steady and avoid adding pressure."),
    "follow_through": ("Follow-through", "Evidence suggests an action was completed or moved forward today.", "Close one open loop with a visible action."),
    "escalation": ("Escalation risk", "Possible signal of tension, pressure, intensity, or conflict in today's records.", "Keep the next message under 3 sentences."),
    "open_loop": ("Open loop", "Evidence suggests something repeated, remained unresolved, or is still waiting.", "Pick one open loop and define the next owner or time."),
    "repeated_topic": ("Repeated topic", "Evidence suggests the same topic or loop came up more than once.", "Close one repeated topic with one visible action."),
    "over_explaining": ("Over-explaining", "Possible signal that clarity was attempted with too many words or repeated explanation.", "Ask one direct question instead of explaining more."),
    "late_night_intensity": ("Late-night intensity", "A late-night record also carried tension, repair, over-explaining, or unresolved-loop signals.", "Avoid serious conversation after 10 PM."),
    "supportive": ("Supportive language", "Evidence suggests care, appreciation, encouragement, or supportive wording.", "Keep the supportive tone and pair it with one clear action."),
    "hostile_absolute": ("Hostile or absolute language", "Possible signal of absolute wording or harsh phrasing.", "Pause and rewrite the next message with one concrete request."),
}

SCORING = {
    "repair": (8, 20),
    "stability": (6, 18),
    "follow_through": (10, 20),
    "escalation": (-10, -30),
    "open_loop": (-7, -21),
    "late_night_intensity": (-8, -16),
    "over_explaining": (-5, -15),
    "supportive": (5, 15),
    "hostile_absolute": (-8, -24),
}

PROMISE_PATTERNS = ["i will", "i’ll", "i'll", "i can", "i need to", "going to", "promise", "plan to"]
COMPLETE_PATTERNS = SIGNAL_PATTERNS["follow_through"]


def _contains_pattern(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(re.search(r"(?<!\w)" + re.escape(pattern.lower()) + r"(?!\w)", lowered) for pattern in patterns)


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", text or ""))


def _record_text(record: dict[str, Any]) -> str:
    return str(record.get("analysis_text") or record.get("excerpt") or "")


def _record_hour(record: dict[str, Any]) -> int | None:
    timestamp = record.get("timestamp_dt")
    if isinstance(timestamp, datetime):
        return timestamp.hour
    try:
        return datetime.fromisoformat(str(record.get("timestamp", ""))).hour
    except ValueError:
        return None


def _record_dt(record: dict[str, Any]) -> datetime | None:
    timestamp = record.get("timestamp_dt")
    if isinstance(timestamp, datetime):
        return timestamp
    try:
        return datetime.fromisoformat(str(record.get("timestamp", "")))
    except ValueError:
        return None


def _confidence(count: int) -> str:
    if count >= 10:
        return "high"
    if count >= 4:
        return "medium"
    if count >= 1:
        return "low"
    return "not enough data"


def _label_for_score(score: int | None, has_records: bool) -> str:
    if not has_records or score is None:
        return "Not enough data"
    if score >= 90:
        return "Calm"
    if score >= 80:
        return "Stable"
    if score >= 60:
        return "Repairing"
    if score >= 40:
        return "Heavy"
    if score >= 20:
        return "Tense"
    return "Escalating"


def _clean_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": record.get("timestamp", ""),
        "profile": record.get("profile", ""),
        "record_type": record.get("record_type", "record"),
        "excerpt": safe_excerpt(record.get("excerpt", "")),
    }


def detect_record_signals(record: dict[str, Any]) -> set[str]:
    text = _record_text(record)
    signals = {name for name, patterns in SIGNAL_PATTERNS.items() if _contains_pattern(text, patterns)}
    hour = _record_hour(record)
    if hour is not None and (hour >= 22 or hour <= 4) and signals.intersection({"escalation", "repair", "open_loop", "over_explaining", "hostile_absolute"}):
        signals.add("late_night_intensity")
    return signals


def calculate_relationship_score(today_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return deterministic score details for today's actual usable records."""
    if not today_records:
        return {"score": None, "label": "Not enough data", "confidence": "not enough data", "evidence_count": 0, "score_parts": {}}
    signal_counts: Counter[str] = Counter()
    for record in today_records:
        signal_counts.update(detect_record_signals(record))
    score = 60
    score_parts: dict[str, int] = {}
    for signal, (each, cap) in SCORING.items():
        raw_delta = each * signal_counts.get(signal, 0)
        delta = min(raw_delta, cap) if each > 0 else max(raw_delta, cap)
        score += delta
        score_parts[signal] = delta
    score = max(0, min(100, score))
    return {"score": score, "label": _label_for_score(score, True), "confidence": _confidence(len(today_records)), "evidence_count": len(today_records), "score_parts": score_parts}


def build_today_relationship_rating(today_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a deterministic 0-100 relationship weather rating from actual records."""
    score_data = calculate_relationship_score(today_records)
    if not today_records:
        return {**score_data, "signals": [], "evidence": []}

    signal_records: dict[str, list[dict[str, Any]]] = {name: [] for name in SIGNAL_META}
    evidence: list[dict[str, Any]] = []
    for record in today_records:
        clean = _clean_record(record)
        detected = detect_record_signals(record)
        if detected:
            evidence.append({**clean, "signals": sorted(detected)})
        for signal in detected:
            if signal in signal_records:
                signal_records[signal].append(clean)

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
    return {**score_data, "signals": signal_cards, "evidence": evidence[:10], "input_counts": dict(Counter(record.get("record_type", "record") for record in today_records))}


def build_next_clean_action(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    rating = build_today_relationship_rating(records)
    signals = rating.get("signals", [])
    if not signals:
        if records:
            return {"title": "Next Clean Action", "action": "Choose one small follow-through step and make it visible.", "evidence_count": len(records)}
        return None
    strongest = signals[0]
    return {"title": "Next Clean Action", "action": strongest.get("suggested_next_action", "Choose one small visible action."), "evidence_count": strongest.get("evidence_count", 0), "based_on": strongest.get("title", "today's strongest signal")}


def build_advice_to_improve(today_records: list[dict[str, Any]], signals: list[dict[str, Any]]) -> list[str]:
    if not today_records:
        return []
    keys = {signal.get("key") for signal in signals}
    advice: list[str] = []
    if "late_night_intensity" in keys:
        advice.append("Avoid serious conversation after 10 PM.")
    if "over_explaining" in keys:
        advice.append("Ask one direct question instead of explaining more.")
    if "open_loop" in keys or "repeated_topic" in keys:
        advice.append("Close one open loop with a visible action.")
    if "repair" in keys:
        advice.append("Acknowledge repair once, then act.")
    if "escalation" in keys or "hostile_absolute" in keys:
        advice.append("Keep the next message under 3 sentences.")
    if "follow_through" in keys and len(advice) < 3:
        advice.append("Name what is already done and keep the next step small.")
    if not advice:
        advice.append("Keep the tone steady and choose one practical next step.")
    return advice[:3]


def build_today_bridge_summary(today_records: list[dict[str, Any]], rating: dict[str, Any]) -> str:
    """Return a 2-4 sentence summary using careful, non-diagnostic wording."""
    if not today_records:
        return "No usable actual records found for today."
    label = rating.get("label", "Not enough data")
    signals = [signal.get("title", "").lower() for signal in rating.get("signals", [])[:3]]
    if signals:
        first = f"Based on today’s records, evidence suggests activity around {', '.join(signals)}."
    else:
        first = "Based on today’s records, there is activity today but not enough evidence for a strong signal."
    second = f"The relationship weather reads as {label}, with {rating.get('confidence', 'not enough data')} confidence."
    action = build_next_clean_action(today_records)
    third = f"The next clean action is to {str(action.get('action', 'choose one practical next step')).lower()}" if action else "The next clean action is to wait for more actual evidence before drawing a conclusion."
    if not third.endswith("."):
        third += "."
    return " ".join([first, second, third])


def build_daily_emotions_report(records: list[dict[str, Any]], role: str) -> dict[str, Any]:
    from dashboard_data_loader import filter_records_for_today

    today_records = filter_records_for_today(records)
    rating = build_today_relationship_rating(today_records)
    advice = build_advice_to_improve(today_records, rating.get("signals", []))
    return {
        "role": role,
        "title": "Daily Emotions Report",
        "today_records": today_records,
        "weather": rating.get("label", "Not enough data"),
        "score": rating.get("score"),
        "confidence": rating.get("confidence", "not enough data"),
        "evidence_count": rating.get("evidence_count", 0),
        "summary": build_today_bridge_summary(today_records, rating),
        "advice": advice,
        "signals": rating.get("signals", []),
        "evidence": rating.get("evidence", []),
        "next_action": build_next_clean_action(today_records),
    }


def build_word_count_per_user(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    chats = [record for record in records if str(record.get("record_type", "")).lower() == "chat"]
    stats: dict[str, dict[str, Any]] = defaultdict(lambda: {"user": "", "messages": 0, "total_words": 0, "longest_message_words": 0})
    for record in chats:
        user = safe_excerpt(record.get("profile") or "Unassigned", 80)
        words = _word_count(_record_text(record))
        if not user or words <= 0:
            continue
        stats[user]["user"] = user
        stats[user]["messages"] += 1
        stats[user]["total_words"] += words
        stats[user]["longest_message_words"] = max(stats[user]["longest_message_words"], words)
    rows = list(stats.values())
    if len(rows) < 2:
        return None
    for row in rows:
        row["avg_words_per_message"] = round(row["total_words"] / row["messages"], 1) if row["messages"] else 0
    rows.sort(key=lambda row: row["total_words"], reverse=True)
    total_words = sum(row["total_words"] for row in rows)
    top = rows[0]
    imbalance = None
    if total_words and top["total_words"] / total_words >= 0.7:
        imbalance = f"Possible imbalance: {top['user']} has about {round(top['total_words'] / total_words * 100)}% of chat words."
    longest = max(rows, key=lambda row: row["longest_message_words"])
    return {"rows": rows, "imbalance_signal": imbalance, "longest_message_signal": f"Longest message signal: {longest['user']} had {longest['longest_message_words']} words."}


def _records_with(records: list[dict[str, Any]], signal: str) -> list[dict[str, Any]]:
    return [record for record in records if signal in detect_record_signals(record)]


def _correlation(name: str, records: list[dict[str, Any]], left: list[dict[str, Any]], right: list[dict[str, Any]], explanation: str) -> dict[str, Any] | None:
    evidence_count = len(set(id(item) for item in left + right))
    if len(records) < 5 or evidence_count < 2:
        return None
    direction = "positive" if left and right else "unclear"
    confidence = _confidence(evidence_count)
    excerpts = [safe_excerpt(record.get("excerpt", ""), 180) for record in (left + right)[:3]]
    return {"name": name, "direction": direction, "confidence": confidence, "evidence_count": evidence_count, "explanation": explanation, "excerpts": excerpts, "warning": "Correlation is not causation."}


def build_behavior_correlations(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    usable = [record for record in records if record.get("excerpt")]
    if len(usable) < 5:
        return []
    late = [record for record in usable if (_record_hour(record) is not None and (_record_hour(record) >= 22 or _record_hour(record) <= 4))]
    long_messages = [record for record in usable if _word_count(_record_text(record)) >= 80]
    journals = [record for record in usable if record.get("record_type") == "journal"]
    correlations = [
        _correlation("Late-night messages vs escalation signals", usable, late, _records_with(usable, "escalation"), "Late records are compared with tension or escalation language."),
        _correlation("Long messages vs over-explaining signals", usable, long_messages, _records_with(usable, "over_explaining"), "Long messages are compared with over-explaining language."),
        _correlation("Repair attempts vs later stability signals", usable, _records_with(usable, "repair"), _records_with(usable, "stability"), "Repair language is compared with later calm or steady records."),
        _correlation("Repeated topics vs tension signals", usable, _records_with(usable, "open_loop"), _records_with(usable, "escalation"), "Repeated loops are compared with tension language."),
        _correlation("Journal reflection vs follow-through signals", usable, journals, _records_with(usable, "follow_through"), "Journal records are compared with completed-action language."),
        _correlation("Message volume spikes vs emotional weather", usable, [record for record in usable if record.get("record_type") == "chat"], _records_with(usable, "hostile_absolute") + _records_with(usable, "escalation"), "Chat volume is compared with heavier language signals."),
    ]
    return [item for item in correlations if item]


def build_conversation_balance(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    word_counts = build_word_count_per_user(records)
    if not word_counts:
        return None
    return {"title": "Conversation Balance", **word_counts}


def build_repair_radar(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    repairs = _records_with(records, "repair")
    if not repairs:
        return None
    now = max((_record_dt(record) for record in records if _record_dt(record)), default=None)
    week_repairs = repairs
    if now:
        week_repairs = [record for record in repairs if (_record_dt(record) and _record_dt(record) >= now - timedelta(days=7))]
    stability_after = len(_records_with(records, "stability"))
    return {"title": "Repair Radar", "today_count": len(repairs), "week_count": len(week_repairs), "stability_after_count": stability_after, "excerpts": [safe_excerpt(record.get("excerpt", ""), 160) for record in repairs[:3]]}


def build_loop_detector(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    loops = _records_with(records, "open_loop")
    if not loops:
        return None
    terms = Counter()
    for record in loops:
        text = _record_text(record).lower()
        for pattern in SIGNAL_PATTERNS["open_loop"]:
            if pattern in text:
                terms[pattern] += 1
    return {"title": "Loop Detector", "loop_count": len(loops), "top_terms": dict(terms.most_common(5)), "suggested_action": "Close one open loop with a visible action.", "excerpts": [safe_excerpt(record.get("excerpt", ""), 160) for record in loops[:3]]}


def build_late_night_risk(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    late = [record for record in records if (_record_hour(record) is not None and (_record_hour(record) >= 22 or _record_hour(record) <= 4))]
    risky = [record for record in late if detect_record_signals(record).intersection({"escalation", "over_explaining", "open_loop", "hostile_absolute"})]
    if not late:
        return None
    return {"title": "Late-Night Risk", "late_count": len(late), "risk_count": len(risky), "suggested_action": "Avoid serious conversation after 10 PM.", "excerpts": [safe_excerpt(record.get("excerpt", ""), 160) for record in (risky or late)[:3]]}


def build_followthrough_tracker(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    promised = [record for record in records if _contains_pattern(_record_text(record), PROMISE_PATTERNS)]
    completed = _records_with(records, "follow_through")
    if not promised and not completed:
        return None
    return {"title": "Follow-Through Tracker", "promised": len(promised), "evidence_completed": len(completed), "still_open": max(0, len(promised) - len(completed)), "excerpts": [safe_excerpt(record.get("excerpt", ""), 160) for record in (completed + promised)[:3]]}
