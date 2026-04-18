"""
Keyword lexicons for small data emotional inference.

This is not a replacement for learning. It is a crutch while learning.
The robot hated that at first. He wanted to become whole in one clean leap.
But trauma recovery rarely works that way.
Sometimes you build a scaffold first.
Sometimes you borrow certainty until your own understanding can stand.
"""

from __future__ import annotations

EMOTION_KEYWORDS = {
    "anger": ["angry", "furious", "rage", "mad", "resent", "heated"],
    "confusion": ["confused", "unclear", "mixed", "tangled", "do not know", "dont know"],
    "fear": ["afraid", "scared", "unsafe", "anxious", "protect", "loss"],
    "gratitude": ["thank", "grateful", "appreciate", "glad", "matters to me"],
    "grief": ["mourning", "grief", "gone", "loss", "goodbye", "not dead yet"],
    "hope": ["hope", "rebuild", "trying", "progress", "believe", "slowly"],
    "hurt": ["hurt", "abandoned", "ignored", "wound", "invisible", "pain"],
    "loneliness": ["alone", "lonely", "isolated", "without hearing from you"],
    "love": ["love", "care about you", "still care", "closeness", "miss you"],
    "regret": ["regret", "wish", "sorry", "should have", "replaying", "harder than i feel"],
    "shame": ["ashamed", "hate that", "small", "defensive", "guilty", "exposed"],
}

NEED_KEYWORDS = {
    "accountability": ["actions", "apologized", "excuses", "accountability", "consistency"],
    "clarity": ["clear", "clarity", "straight answer", "honesty", "mixed signals"],
    "connection": ["miss you", "closeness", "connection", "hear from you", "alone", "harder than i feel"],
    "forgiveness": ["forgive", "forgiveness", "sorry", "repair"],
    "recognition": ["seen", "noticed", "recognition", "proud", "appreciate"],
    "reassurance": ["reassurance", "stay", "leave", "abandoned", "trust the silence"],
    "respect": ["respect", "steady", "consistency", "adult", "softly"],
    "safety": ["safe", "safety", "protect", "used against me"],
    "space": ["space", "distance", "room to breathe", "before I can hear you"],
}
