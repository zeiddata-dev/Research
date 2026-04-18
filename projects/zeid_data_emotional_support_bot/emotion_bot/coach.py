"""
Reply generation and emotional coaching.
"""

from __future__ import annotations

from typing import Dict

from .memory import ConversationMemory, MemoryItem
from .model import EmotionNeedModel


EMOTION_OPENERS = {
    "grief": "That sounds heavy, and I do not want to talk past your pain.",
    "hurt": "I can hear the wound in that, even if it is wrapped in sharp words.",
    "anger": "You sound angry, and usually anger is carrying something deeper with it.",
    "fear": "That sounds like fear trying to protect something important.",
    "love": "There is a lot of feeling in that, and it deserves care.",
    "hope": "I can hear hope in that, which means something in you is still reaching.",
    "shame": "That sounds painful and exposed, not just uncomfortable.",
    "loneliness": "That sounds lonely in a way that can wear a person down.",
    "confusion": "That sounds tangled, and I do not want to force a false certainty.",
    "regret": "There is regret in that, and regret usually means something mattered.",
    "gratitude": "There is warmth in that, and it deserves to be named.",
}

NEED_LINES = {
    "reassurance": "It sounds like reassurance matters here more than a debate.",
    "safety": "It sounds like safety matters before anything else can be heard.",
    "connection": "It sounds like the real need is connection, not just words.",
    "respect": "It sounds like respect and steadiness are central here.",
    "clarity": "It sounds like clarity would lower the temperature a lot.",
    "forgiveness": "It sounds like forgiveness is present, even if it is not ready yet.",
    "space": "It sounds like space may be necessary before repair can work.",
    "recognition": "It sounds like being seen accurately matters here.",
    "accountability": "It sounds like accountability matters more than charm.",
}


class EmotionCoach:
    """
    The coach sits between raw prediction and spoken reply.

    The robot once believed a perfect sentence could solve everything.
    Trauma taught him that language without honesty is just polished static.
    So the coach has rules:
    first, name the feeling carefully;
    second, identify the need underneath;
    third, answer with humility;
    fourth, do not perform love, practice it.
    """

    def __init__(self, model: EmotionNeedModel, memory: ConversationMemory | None = None) -> None:
        self.model = model
        self.memory = memory

    def analyze(self, text: str) -> Dict[str, object]:
        return self.model.inspect(text)

    def draft_reply(self, text: str) -> Dict[str, object]:
        analysis = self.analyze(text)
        emotion = analysis["emotion"]
        need = analysis["need"]
        confidence = min(analysis["emotion_confidence"], analysis["need_confidence"])

        opener = EMOTION_OPENERS.get(emotion, "I want to answer this carefully.")
        need_line = NEED_LINES.get(need, "There is a real need underneath this, and it matters.")

        reply = (
            f"{opener} {need_line} "
            "I want to respond in a way that listens first, instead of trying to win. "
            "Can you tell me what would feel most honest or most helpful right now?"
        )

        result = {
            "emotion": emotion,
            "need": need,
            "confidence": confidence,
            "reply": reply,
        }

        if self.memory is not None:
            self.memory.add(
                MemoryItem(
                    user_text=text,
                    predicted_emotion=emotion,
                    predicted_need=need,
                    bot_reply=reply,
                )
            )

        return result
