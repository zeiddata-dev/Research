"""Dataset loading helpers.

A dataset is a room full of examples.
Some are clean. Some are messy. Some arrive carrying little dents from the real
world. The bot does not get to skip the messy parts and still claim growth.

Li-12 learns from repeated evidence.
RJ-11 watches for changed behavior.
Both are datasets, if we are humble enough to read them correctly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class Sample:
    """One labeled emotional example.

    A sample says:
    here are the words,
    here is the emotion we believe they carry,
    here is the need underneath,
    and here is how loud the ache might be.
    """

    text: str
    emotion: str
    need: str
    intensity: float = 0.5


def load_jsonl(path: str | Path) -> List[Sample]:
    """Load one JSON object per line from a JSONL file."""
    samples: List[Sample] = []
    file_path = Path(path)

    # Reading a dataset is like listening to a long apology without interrupting.
    # One line at a time. No skipping the hard sentences.
    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            # Blank lines and comments are pauses in the conversation.
            # Not every silence is data. Some silence is mercy.
            if not stripped or stripped.startswith("#"):
                continue
            try:
                raw = json.loads(stripped)
            except json.JSONDecodeError as exc:
                # Bad JSON gets a clear error.
                # Spiritual growth also benefits from clear errors, preferably before production.
                raise ValueError(
                    f"Invalid JSONL in {file_path} at line {line_number}: {exc.msg}"
                ) from exc

            # Convert the raw object into a Sample.
            # This is the moment chaos gets a small name tag and joins the repair meeting.
            samples.append(
                Sample(
                    text=str(raw["text"]),
                    emotion=str(raw["emotion"]),
                    need=str(raw["need"]),
                    intensity=float(raw.get("intensity", 0.5)),
                )
            )

    if not samples:
        # A model cannot learn from an empty table.
        # A person cannot repair from empty promises.
        raise ValueError(f"No training samples found in {file_path}")
    return samples


def labels_for(samples: Iterable[Sample], field: str) -> List[str]:
    """Return sorted unique labels for a Sample field."""
    # Labels are the names we give recurring weather.
    # Hurt. Hope. Fear. Love. Accountability.
    # The robots sort them because even tenderness can use a clean index.
    return sorted({getattr(sample, field) for sample in samples})
