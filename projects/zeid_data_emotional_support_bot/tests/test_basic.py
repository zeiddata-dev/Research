from emotion_bot.dataset import Sample
from emotion_bot.model import EmotionNeedModel


def test_basic_fit_and_inspect():
    """
    This test proves the model can learn a small emotional pattern
    and inspect a new message for the likely feeling and need beneath it.

    In the story context:

    Li-12 does not always speak cleanly.
    Sometimes his pain comes out as anger, distance, or fear.

    RJ-11 does not need a perfect sentence.
    She needs the system to listen beneath the words.

    The model should learn that:

    "I miss you" can point to loneliness.
    "I am scared you will leave" can point to fear.
    "I am grateful you stayed" can point to gratitude.

    The purpose is not to diagnose a person.
    The purpose is to help the bot respond with care instead of trying to win.
    """

    samples = [
        Sample(
            text="I miss you and I feel alone",
            emotion="loneliness",
            need="connection",
            intensity=0.9,
        ),
        Sample(
            text="I am scared you will leave",
            emotion="fear",
            need="reassurance",
            intensity=0.8,
        ),
        Sample(
            text="I am grateful you stayed",
            emotion="gratitude",
            need="recognition",
            intensity=0.6,
        ),
    ]

    model = EmotionNeedModel()
    model.fit(samples)

    result = model.inspect("I feel alone and miss you")

    assert "emotion" in result
    assert "need" in result
    assert result["emotion"] == "loneliness"
    assert result["need"] == "connection"


def test_model_detects_reassurance_need_from_fear_language():
    """
    Li-12 may say something sharp, but the wound underneath may be fear.

    A healthy response system should not only hear the surface tension.
    It should recognize when the deeper need is reassurance.

    This test checks that fear based language maps to a need for reassurance.
    """

    samples = [
        Sample(
            text="I am scared you will leave",
            emotion="fear",
            need="reassurance",
            intensity=0.8,
        ),
        Sample(
            text="I miss you and I feel alone",
            emotion="loneliness",
            need="connection",
            intensity=0.9,
        ),
        Sample(
            text="Thank you for staying with me",
            emotion="gratitude",
            need="recognition",
            intensity=0.6,
        ),
    ]

    model = EmotionNeedModel()
    model.fit(samples)

    result = model.inspect("I am afraid you are going to disappear")

    assert "emotion" in result
    assert "need" in result
    assert result["need"] == "reassurance"


def test_model_handles_mixed_emotional_language():
    """
    Sometimes the user does not know whether they want comfort or distance.

    That does not mean they are being unclear on purpose.
    It means the system is reading conflict inside the heart.

    RJ-11 may need space and comfort at the same time.
    Li-12 may need to learn that repair cannot be forced.

    This test makes sure the model can still return a usable emotional read
    when the message contains tangled feelings.
    """

    samples = [
        Sample(
            text="I want comfort but I also need space",
            emotion="conflicted",
            need="patience",
            intensity=0.85,
        ),
        Sample(
            text="Please do not push me right now",
            emotion="overwhelmed",
            need="space",
            intensity=0.75,
        ),
        Sample(
            text="I still care but I am hurt",
            emotion="hurt",
            need="gentleness",
            intensity=0.9,
        ),
    ]

    model = EmotionNeedModel()
    model.fit(samples)

    result = model.inspect("I do not know if I want comfort or distance")

    assert "emotion" in result
    assert "need" in result
    assert result["emotion"] in {"conflicted", "overwhelmed", "hurt"}
    assert result["need"] in {"patience", "space", "gentleness"}


def test_model_returns_intensity_signal():
    """
    The bot should not treat every message with the same emotional weight.

    A soft gratitude message does not require the same response as abandonment fear.
    A high intensity wound needs a slower, safer, more careful reply.

    This test makes sure intensity survives inspection in some usable form.
    """

    samples = [
        Sample(
            text="I feel abandoned and scared",
            emotion="fear",
            need="reassurance",
            intensity=0.95,
        ),
        Sample(
            text="I appreciate you listening",
            emotion="gratitude",
            need="recognition",
            intensity=0.5,
        ),
        Sample(
            text="I need a little time before we talk",
            emotion="overwhelmed",
            need="space",
            intensity=0.7,
        ),
    ]

    model = EmotionNeedModel()
    model.fit(samples)

    result = model.inspect("I feel scared and abandoned")

    assert "emotion" in result
    assert "need" in result
    assert "intensity" in result
    assert result["emotion"] == "fear"
    assert result["need"] == "reassurance"
    assert result["intensity"] >= 0.8