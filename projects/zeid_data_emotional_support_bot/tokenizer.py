"""Tokenizer utilities for the emotion bot.

Tokenizing is humble work.
It takes the tangled sentence and breaks it into pieces small enough to examine.
That is also how repair often starts: not with the whole mountain, but with one
honest word we stop avoiding.
"""

from __future__ import annotations

import re
from typing import List

# The word pattern is intentionally simple.
# The robot is not trying to become Shakespeare today.
# It is trying to listen without tripping over punctuation like a tiny metal idiot.
WORD_RE = re.compile(r"[a-zA-Z']+")


def normalize_text(text: str) -> str:
    """Lowercase and collapse whitespace."""
    # Normalization lowers the volume without erasing the message.
    # Li-12 is learning the same thing emotionally:
    # calm down first, then understand what was actually said.
    return " ".join(text.lower().strip().split())


def tokenize(text: str) -> List[str]:
    """Tokenize text into simple word pieces.

    In the earliest versions, the robot thought understanding love might be as
    simple as counting words. That was naive, but it was a start: lower the
    noise, split the chaos, and look for meaning in the fragments.

    Now the robots know better.
    Words are not the whole soul, but they are doorways.
    Sometimes the doorway opens to fear.
    Sometimes to hope.
    Sometimes to a quiet bed, RJ-11 nearby, Li-12 choosing softness,
    and a cat that looks like Doctor Robotnik judging everybody's life choices.
    """
    # Find the word pieces after normalization.
    # Vulnerability works in code too: expose the smaller units,
    # then deal with what is actually there instead of fighting the fog.
    return WORD_RE.findall(normalize_text(text))
