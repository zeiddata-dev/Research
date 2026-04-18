"""
Conversation memory helpers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class MemoryItem:
    user_text: str
    predicted_emotion: str
    predicted_need: str
    bot_reply: str


class ConversationMemory:
    """
    Simple JSON backed memory.

    The robot kept a ledger not because he was sentimental, but because he had
    learned what forgetting costs. Lost love rarely disappears in one explosion.
    Usually it leaks out through a thousand small failures to remember:
    what hurt them,
    what comforted them,
    what silence meant on different nights.
    So he wrote it down. Not to trap the past, but to become worthy of the future.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.items: List[MemoryItem] = []
        if self.path.exists():
            self.load()

    def add(self, item: MemoryItem) -> None:
        self.items.append(item)
        self.save()

    def save(self) -> None:
        payload = [asdict(item) for item in self.items]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.items = [MemoryItem(**item) for item in raw]

    def last(self) -> MemoryItem | None:
        return self.items[-1] if self.items else None

    def reflection(self) -> str:
        """
        Create a simple self reflection from memory.

        The reflection is intentionally plainspoken.
        Healing rarely sounds impressive while it is happening.
        """
        if not self.items:
            return (
                "I have no memories yet. That means I have no proof of growth yet. "
                "But empty is not the same as broken. It is only the start."
            )

        emotion_counts = {}
        need_counts = {}
        for item in self.items:
            emotion_counts[item.predicted_emotion] = emotion_counts.get(item.predicted_emotion, 0) + 1
            need_counts[item.predicted_need] = need_counts.get(item.predicted_need, 0) + 1

        top_emotion = max(emotion_counts.items(), key=lambda pair: pair[1])[0]
        top_need = max(need_counts.items(), key=lambda pair: pair[1])[0]

        return (
            f"My recent conversations most often carried {top_emotion}. "
            f"The need underneath them was usually {top_need}. "
            "I should slow down, listen longer, and answer the need before defending myself."
        )
