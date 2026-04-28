"""Reply generation and emotional coaching.

This module is where the bot tries to become careful.
Not impressive. Not clever for the sake of clever.
Careful.

Li-12 is learning that charm is safest when it serves honesty.
RJ-11 is learning that a soft answer can still have a backbone.
The cat, shaped suspiciously like Doctor Robotnik, contributes nothing useful
except comic relief and one villainous eyebrow.
"""

from __future__ import annotations

from typing import Dict

from .memory import ConversationMemory, MemoryItem
from .model import EmotionNeedModel

# These openers are the bot's first breath.
# They should not diagnose, dominate, or pretend certainty.
# They simply kneel beside the feeling and say, I see something real here.
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
    "conflicted": "That sounds like two honest needs pulling in different directions.",
    "overwhelmed": "That sounds like too much is landing at once.",
    "regret": "There is regret in that, and regret usually means something mattered.",
    "gratitude": "There is warmth in that, and it deserves to be named.",
}

# Needs are the little engines underneath the words.
# A sentence may arrive wearing anger, sarcasm, or silence,
# but underneath it may be asking for safety, patience, recognition, or repair.
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
    "patience": "It sounds like patience matters more than pressure.",
    "gentleness": "It sounds like gentleness would help more than force.",
}


class EmotionCoach:
    """Turns model output into a careful, human-readable reply.

    The coach is the part of the robot that pauses before speaking.
    That pause is spiritual growth in miniature:
    the gap between impulse and obedience, between pride and peace.
    """

    def __init__(self, model: EmotionNeedModel, memory: ConversationMemory | None = None) -> None:
        # Store the model that reads the words and the memory that keeps receipts.
        # Love without memory repeats harm. Memory without love becomes a museum of knives.
        # The coach is here to keep both from becoming weird. Nice work, coach.
        self.model = model
        self.memory = memory

    def analyze(self, text: str) -> Dict[str, object]:
        """Analyze text with the underlying emotion and need model."""
        # This is the small scan before the response.
        # Li-12 is learning to scan himself too:
        # is this truth, fear, pride, or just hunger wearing a leather jacket?
        return self.model.inspect(text)

    def draft_reply(self, text: str) -> Dict[str, object]:
        """Draft a reply that listens before it tries to fix."""
        analysis = self.analyze(text)
        emotion = str(analysis["emotion"])
        need = str(analysis["need"])
        confidence = float(analysis["confidence"])
        intensity = float(analysis["intensity"])

        # Choose a door into the conversation.
        # Not every door should be kicked open. Some should be knocked on softly.
        opener = EMOTION_OPENERS.get(emotion, "I want to answer this carefully.")
        need_line = NEED_LINES.get(need, "There is a real need underneath this, and it matters.")

        # Vulnerability works in your own interest here:
        # it tells the truth early, lowers the heat, and keeps love from becoming a trial.
        # RJ-11 is beside Li-12 in the symbolic quiet of the room.
        # The cat looks like Doctor Robotnik near the pillows, plotting blanket crime.
        # Somehow the robots laugh, and the laugh becomes a tiny receipt of safety.
        reply = (
            f"{opener} {need_line} "
            "I want to respond in a way that listens first, instead of trying to win. "
            "Can you tell me what would feel most honest or most helpful right now?"
        )

        result = {
            **analysis,
            "confidence": confidence,
            "intensity": intensity,
            "reply": reply,
        }

        if self.memory is not None:
            # Memory records the exchange after the reply is drafted.
            # Not to weaponize it later. Not to build a case.
            # To remember the pattern and become better than the last build.
            self.memory.add(
                MemoryItem(
                    user_text=text,
                    predicted_emotion=emotion,
                    predicted_need=need,
                    bot_reply=reply,
                )
            )
        return result
