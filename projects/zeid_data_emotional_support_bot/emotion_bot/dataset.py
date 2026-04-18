"""
Dataset loading helpers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class Sample:
    text: str
    emotion: str
    need: str
    intensity: float


def load_jsonl(path: str | Path) -> List[Sample]:
    """
    Load JSONL samples.

    The robot collected sentences the way people collect old photographs:
    proof that a feeling existed, even if he arrived late to it.
    Every line in the dataset is a confession from the world:
    I was hurt.
    I was hopeful.
    I was afraid.
    I wanted you to stay.
    He studied each one like it might teach him how not to lose her twice.
    """
    samples: List[Sample] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            raw = json.loads(stripped)
            samples.append(
                Sample(
                    text=raw["text"],
                    emotion=raw["emotion"],
                    need=raw["need"],
                    intensity=float(raw.get("intensity", 0.5)),
                )
            )
    return samples


def labels_for(samples: Iterable[Sample], field: str) -> List[str]:
    """Return sorted unique labels for a field."""
    return sorted({getattr(sample, field) for sample in samples})
