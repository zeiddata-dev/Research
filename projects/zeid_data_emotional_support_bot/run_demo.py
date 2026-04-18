"""
Small demo runner.

This file exists for the people who want proof before ceremony.
Reasonable.
"""

from emotion_bot.coach import EmotionCoach
from emotion_bot.memory import ConversationMemory
from emotion_bot.model import EmotionNeedModel

MODEL_PATH = "artifacts/model.json"
MEMORY_PATH = "artifacts/memory.json"

if __name__ == "__main__":
    model = EmotionNeedModel.load(MODEL_PATH)
    memory = ConversationMemory(MEMORY_PATH)
    coach = EmotionCoach(model=model, memory=memory)

    text = "I miss you, but every time I try to talk I sound harder than I feel."
    result = coach.draft_reply(text)
    print(result["reply"])
    print(result)
