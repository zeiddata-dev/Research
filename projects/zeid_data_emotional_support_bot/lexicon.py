"""Keyword lexicons for small-data emotional inference.

This is not a replacement for learning. It is a scaffold while the model gets
more examples. Even damaged systems can start with careful defaults.

A lexicon is a little field guide for the storm:
when the words say "alone," look for loneliness;
when they say "stay," look for reassurance;
when they say "sorry," do not confuse the sound with changed behavior.
"""

from __future__ import annotations

# Emotion keywords are not prophecy.
# They are hints, like footprints near the door.
# Li-12 is learning not to stomp through the evidence in boots.
EMOTION_KEYWORDS = {
    "anger": ["angry", "furious", "rage", "mad", "resent", "heated"],
    "conflicted": ["conflicted", "comfort", "distance", "both", "mixed"],
    "confusion": ["confused", "unclear", "mixed", "tangled", "do not know", "dont know"],
    "fear": ["afraid", "scared", "unsafe", "anxious", "protect", "loss", "disappear"],
    "gratitude": ["thank", "grateful", "appreciate", "glad", "matters to me"],
    "grief": ["mourning", "grief", "gone", "loss", "goodbye", "not dead yet"],
    "hope": ["hope", "rebuild", "trying", "progress", "believe", "slowly"],
    "hurt": ["hurt", "abandoned", "ignored", "wound", "invisible", "pain"],
    "loneliness": ["alone", "lonely", "isolated", "without hearing from you"],
    "love": ["love", "care about you", "still care", "closeness", "miss you"],
    "overwhelmed": ["overwhelmed", "too much", "push", "room", "space"],
    "regret": ["regret", "wish", "sorry", "should have", "replaying", "harder than i feel"],
    "shame": ["ashamed", "hate that", "small", "defensive", "guilty", "exposed"],
}

# Need keywords are the small prayers under the sentence.
# Sometimes the surface says "I am mad," but the need says "please be safe."
# Sometimes the surface says "whatever," but the need says "do not leave me alone in this."
# And sometimes the cat says nothing, because Doctor Robotnik whiskers need no translation.
NEED_KEYWORDS = {
    "accountability": ["actions", "apologized", "excuses", "accountability", "consistency"],
    "clarity": ["clear", "clarity", "straight answer", "honesty", "mixed signals"],
    "connection": ["miss you", "closeness", "connection", "hear from you", "alone", "harder than i feel"],
    "forgiveness": ["forgive", "forgiveness", "sorry", "repair"],
    "gentleness": ["gentle", "gentleness", "soft", "softly", "care"],
    "patience": ["patience", "slow", "slowly", "not ready", "comfort", "distance"],
    "recognition": ["seen", "noticed", "recognition", "proud", "appreciate"],
    "reassurance": ["reassurance", "stay", "leave", "abandoned", "trust the silence", "disappear"],
    "respect": ["respect", "steady", "consistency", "adult", "softly"],
    "safety": ["safe", "safety", "protect", "used against me", "afraid", "scared"],
    "space": ["space", "distance", "room to breathe", "before i can hear you", "push"],
}
