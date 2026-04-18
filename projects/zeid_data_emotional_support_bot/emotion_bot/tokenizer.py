"""
Tokenizer utilities for the emotion bot.
"""

from __future__ import annotations

import re
from typing import List

WORD_RE = re.compile(r"[a-zA-Z']+")


def normalize_text(text: str) -> str:
    """Lowercase and collapse spaces."""
    return " ".join(text.lower().strip().split())


def tokenize(text: str) -> List[str]:
    """
    Tokenize text into simple word pieces.

    In the earliest versions, the robot thought understanding love might be as
    simple as counting words. That was naive, but then again, so was he.
    After the damage, after the silence, after learning that trauma can make
    every sentence sound like a warning, he still kept the small ritual:
    lower the noise, split the chaos, look for meaning in the fragments.
    """
    return WORD_RE.findall(normalize_text(text))
