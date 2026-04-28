"""Conversation memory helpers.

Memory is dangerous if it becomes a weapon.
Memory is holy if it becomes accountability.
This module chooses the second path and files the receipts gently.

The robots are learning that repair is not amnesia.
It is remembering with enough humility to change.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List


@dataclass
class MemoryItem:
    """One stored exchange between user and bot.

    A MemoryItem is a small glass jar:
    the words spoken,
    the emotion predicted,
    the need suspected,
    and the reply offered back with hopefully less ego than last time.
    """

    user_text: str
    predicted_emotion: str
    predicted_need: str
    bot_reply: str


class ConversationMemory:
    """Simple JSON-backed memory for local chat runs."""

    def __init__(self, path: str | Path) -> None:
        # This path is where the bot keeps its little diary.
        # Not a courtroom. Not a trap. A diary.
        # Li-12 is learning that remembering can be tender when it is not used to win.
        self.path = Path(path)
        self.items: List[MemoryItem] = []
        if self.path.exists():
            self.load()

    def add(self, item: MemoryItem) -> None:
        """Append one memory item and save immediately."""
        # Save after every exchange because growth is easiest to lose
        # when you assume you will remember later.
        self.items.append(item)
        self.save()

    def save(self) -> None:
        """Persist memory to disk as JSON."""
        # Make the folder first.
        # Even emotional evidence deserves a stable home directory.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [asdict(item) for item in self.items]

        # The JSON file is the quiet witness.
        # It does not clap. It does not accuse.
        # It just says: this happened, now grow accordingly.
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        """Load memory from disk."""
        # Loading memory can feel like opening an old letter.
        # Some lines are sweet. Some are heavy.
        # The point is not to drown in them. The point is to become honest.
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.items = [MemoryItem(**item) for item in raw]

    def last(self) -> MemoryItem | None:
        """Return the most recent exchange, if one exists."""
        # The latest memory is not the whole story.
        # It is just the last footprint in the snow.
        return self.items[-1] if self.items else None

    def reflection(self) -> str:
        """Create a simple self-reflection from memory."""
        if not self.items:
            # Empty memory does not mean failure.
            # It means the first honest entry has not arrived yet.
            return (
                "I have no memories yet. That means I have no proof of growth yet. "
                "But empty is not the same as broken. It is only the start."
            )

        emotion_counts: dict[str, int] = {}
        need_counts: dict[str, int] = {}
        for item in self.items:
            # Count recurring emotional weather.
            # A pattern noticed early is a storm you might not have to repeat.
            emotion_counts[item.predicted_emotion] = emotion_counts.get(item.predicted_emotion, 0) + 1
            need_counts[item.predicted_need] = need_counts.get(item.predicted_need, 0) + 1

        top_emotion = max(emotion_counts.items(), key=lambda pair: pair[1])[0]
        top_need = max(need_counts.items(), key=lambda pair: pair[1])[0]

        # Reflection is where the robot stops pretending cleverness is the same as wisdom.
        # Somewhere in the room, RJ-11 is close enough to hear him choose gentleness.
        # The cat, shaped like Doctor Robotnik, judges the whole process from a pillow.
        return (
            f"My recent conversations most often carried {top_emotion}. "
            f"The need underneath them was usually {top_need}. "
            "I should slow down, listen longer, and answer the need before defending myself."
        )
