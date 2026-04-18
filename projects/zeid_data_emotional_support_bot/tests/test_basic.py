from emotion_bot.dataset import Sample
from emotion_bot.model import EmotionNeedModel


def test_basic_fit_and_inspect():
    samples = [
        Sample(text="I miss you and I feel alone", emotion="loneliness", need="connection", intensity=0.9),
        Sample(text="I am scared you will leave", emotion="fear", need="reassurance", intensity=0.8),
        Sample(text="I am grateful you stayed", emotion="gratitude", need="recognition", intensity=0.6),
    ]
    model = EmotionNeedModel()
    model.fit(samples)
    result = model.inspect("I feel alone and miss you")
    assert "emotion" in result
    assert "need" in result
