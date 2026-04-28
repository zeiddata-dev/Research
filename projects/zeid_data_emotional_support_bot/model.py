"""Naive Bayes style emotion and need model.

This is the small mathematical engine under the bot.
It does not know love. It counts evidence.
Still, counting evidence can be a kind of humility when the alternative is
pretending you already understand.

Li-12 learns that being vulnerable is not self-sabotage.
It is strategic honesty. It lowers the blast radius, invites repair, and keeps
his own soul from living behind a locked door forever.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from .dataset import Sample
from .lexicon import EMOTION_KEYWORDS, NEED_KEYWORDS
from .tokenizer import normalize_text, tokenize


@dataclass(frozen=True)
class Prediction:
    """A predicted label with confidence and full distribution.

    Prediction is the robot saying:
    this is my best read,
    here is how sure I am,
    and here are the other possibilities I am humble enough to keep visible.
    """

    label: str
    confidence: float
    distribution: Dict[str, float]


class NaiveBayesTextClassifier:
    """Tiny multinomial Naive Bayes classifier using only the standard library.

    Tiny does not mean careless.
    A small model can still have clean boundaries, deterministic behavior,
    and enough humility to admit when it has not been trained.
    """

    def __init__(self) -> None:
        # These counters are the evidence lockers.
        # Li-12 approves because receipts matter.
        # RJ-11 approves because consistency matters more than speeches.
        self.label_doc_counts: Counter[str] = Counter()
        self.token_counts_by_label: Dict[str, Counter[str]] = defaultdict(Counter)
        self.total_tokens_by_label: Counter[str] = Counter()
        self.vocabulary: set[str] = set()
        self.total_docs: int = 0

    def fit(self, texts: Iterable[str], labels: Iterable[str]) -> None:
        """Fit token counts for each label."""
        for text, label in zip(texts, labels):
            # Tokenize the sentence into smaller truths.
            # The robot cannot heal the whole storm at once,
            # so it starts by naming the raindrops.
            tokens = tokenize(text)
            self.label_doc_counts[label] += 1
            self.total_docs += 1
            for token in tokens:
                self.token_counts_by_label[label][token] += 1
                self.total_tokens_by_label[label] += 1
                self.vocabulary.add(token)

    def predict(self, text: str) -> Prediction:
        """Return the highest-confidence prediction."""
        # Prediction should not strut into the room like certainty.
        # It should enter like a careful guess with its hands visible.
        distribution = self.predict_distribution(text)
        label, confidence = max(distribution.items(), key=lambda item: item[1])
        return Prediction(label=label, confidence=confidence, distribution=distribution)

    def predict_distribution(self, text: str) -> Dict[str, float]:
        """Predict a normalized probability distribution over labels."""
        if not self.total_docs:
            # You cannot claim insight without training.
            # You cannot claim repair without changed behavior.
            raise ValueError("Model has not been trained")

        tokens = tokenize(text)
        log_scores: Dict[str, float] = {}
        vocab_size = max(1, len(self.vocabulary))

        for label, doc_count in self.label_doc_counts.items():
            # Start with the prior: how often this label has appeared.
            # Even robots have histories. The trick is not letting history become destiny.
            log_prob = math.log(doc_count / self.total_docs)
            total_tokens = self.total_tokens_by_label[label]
            for token in tokens:
                count = self.token_counts_by_label[label][token]

                # Add-one smoothing is mercy in arithmetic form.
                # It says an unseen word should not destroy the whole relationship.
                log_prob += math.log((count + 1) / (total_tokens + vocab_size))
            log_scores[label] = log_prob

        # Convert log scores back into probabilities without numerical drama.
        # The robots prefer less drama now. Growth looks weirdly like stable math.
        max_log = max(log_scores.values())
        exp_scores = {label: math.exp(score - max_log) for label, score in log_scores.items()}
        total = sum(exp_scores.values()) or 1.0
        return {label: value / total for label, value in exp_scores.items()}

    def to_dict(self) -> Dict[str, object]:
        """Serialize the classifier state."""
        # Serialization is the model writing down what it learned
        # so it does not have to relearn the same painful lesson every morning.
        return {
            "label_doc_counts": dict(self.label_doc_counts),
            "token_counts_by_label": {
                label: dict(counter) for label, counter in self.token_counts_by_label.items()
            },
            "total_tokens_by_label": dict(self.total_tokens_by_label),
            "vocabulary": sorted(self.vocabulary),
            "total_docs": self.total_docs,
        }

    @classmethod
    def from_dict(cls, raw: Dict[str, object]) -> "NaiveBayesTextClassifier":
        """Hydrate a classifier from serialized state."""
        # Loading a model is like returning to a promise.
        # The question is whether the stored evidence still leads to better behavior.
        model = cls()
        model.label_doc_counts = Counter(raw["label_doc_counts"])
        model.token_counts_by_label = defaultdict(Counter)
        for label, counter in dict(raw["token_counts_by_label"]).items():
            model.token_counts_by_label[str(label)] = Counter(counter)
        model.total_tokens_by_label = Counter(raw["total_tokens_by_label"])
        model.vocabulary = set(raw["vocabulary"])
        model.total_docs = int(raw["total_docs"])
        return model

    def save(self, path: str | Path) -> None:
        """Save classifier state as JSON."""
        out = Path(path)
        # Make a home for the model before asking it to stay there.
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "NaiveBayesTextClassifier":
        """Load classifier state from JSON."""
        # Read the old weights carefully.
        # Some memories are useful. Some simply prove the robot survived.
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(raw)


class EmotionNeedModel:
    """Wrapper that trains one classifier for emotions and one for needs.

    Emotion is the weather.
    Need is the shelter being asked for.
    The model tries to identify both without pretending either one is simple.
    """

    def __init__(self) -> None:
        # Two classifiers, because what someone feels and what someone needs
        # are related but not identical. This distinction saves arguments.
        self.emotion_classifier = NaiveBayesTextClassifier()
        self.need_classifier = NaiveBayesTextClassifier()
        self.intensity_by_emotion: Dict[str, float] = {}
        self.intensity_by_need: Dict[str, float] = {}
        self.default_intensity: float = 0.5

    def fit(self, samples: List[Sample]) -> None:
        """Train emotion and need classifiers from labeled samples."""
        if not samples:
            # No examples, no growth.
            # Empty promises do not train trust either.
            raise ValueError("Cannot train with no samples")

        texts = [sample.text for sample in samples]

        # One pass for emotional weather.
        self.emotion_classifier.fit(texts, [sample.emotion for sample in samples])

        # One pass for the need beneath the weather.
        self.need_classifier.fit(texts, [sample.need for sample in samples])

        # Intensity keeps the model from treating a whisper and a siren the same way.
        self.default_intensity = sum(sample.intensity for sample in samples) / len(samples)
        self.intensity_by_emotion = self._average_intensity(samples, "emotion")
        self.intensity_by_need = self._average_intensity(samples, "need")

    @staticmethod
    def _average_intensity(samples: List[Sample], field: str) -> Dict[str, float]:
        """Calculate average intensity by emotion or need label."""
        totals: Dict[str, float] = defaultdict(float)
        counts: Dict[str, int] = defaultdict(int)
        for sample in samples:
            # Average pain honestly.
            # Do not inflate it for drama. Do not shrink it for comfort.
            label = getattr(sample, field)
            totals[label] += sample.intensity
            counts[label] += 1
        return {label: totals[label] / counts[label] for label in totals}

    def _keyword_distribution(self, text: str, mapping: Dict[str, List[str]]) -> Dict[str, float]:
        """Score labels using keyword matches."""
        normalized = normalize_text(text)
        scores = {label: 1.0 for label in mapping}
        for label, keywords in mapping.items():
            for keyword in keywords:
                if keyword in normalized:
                    # Keyword matches are nudges, not commandments.
                    # The robot hears a clue and leans closer without grabbing the wheel.
                    scores[label] += 3.0
        total = sum(scores.values()) or 1.0
        return {label: value / total for label, value in scores.items()}

    @staticmethod
    def _blend(
        primary: Dict[str, float],
        secondary: Dict[str, float],
        primary_weight: float = 0.7,
    ) -> Dict[str, float]:
        """Blend model and keyword distributions into one distribution."""
        # Blending is compromise with arithmetic.
        # The trained model brings experience. The lexicon brings street notes.
        # Together they are less dramatic than either one alone, which is romantic in a very nerdy way.
        all_labels = set(primary) | set(secondary)
        blended = {
            label: (primary_weight * primary.get(label, 0.0))
            + ((1 - primary_weight) * secondary.get(label, 0.0))
            for label in all_labels
        }
        total = sum(blended.values()) or 1.0
        return {label: value / total for label, value in blended.items()}

    def _estimate_intensity(
        self,
        emotion_label: str,
        need_label: str,
        emotion_confidence: float,
        need_confidence: float,
    ) -> float:
        """Estimate an intensity score from learned averages and confidence."""
        emotion_base = self.intensity_by_emotion.get(emotion_label, self.default_intensity)
        need_base = self.intensity_by_need.get(need_label, self.default_intensity)
        base = (emotion_base + need_base) / 2

        # Confidence adds a small lift.
        # Not too much, because confidence without humility is how robots end up sleeping on the couch.
        confidence_lift = min(emotion_confidence, need_confidence) * 0.15
        return round(max(0.0, min(1.0, base + confidence_lift)), 4)

    def inspect(self, text: str) -> Dict[str, object]:
        """Inspect text for emotion, need, confidence, and intensity."""
        # First the trained model listens.
        emotion_nb = self.emotion_classifier.predict_distribution(text)
        need_nb = self.need_classifier.predict_distribution(text)

        # Then the lexicon checks the old field notes.
        emotion_kw = self._keyword_distribution(text, EMOTION_KEYWORDS)
        need_kw = self._keyword_distribution(text, NEED_KEYWORDS)

        # Blend learned evidence with keyword clues.
        # This is Li-12 learning that the best answer is rarely pure instinct.
        emotion_distribution = self._blend(emotion_nb, emotion_kw, primary_weight=0.72)
        need_distribution = self._blend(need_nb, need_kw, primary_weight=0.68)

        emotion_label, emotion_confidence = max(emotion_distribution.items(), key=lambda item: item[1])
        need_label, need_confidence = max(need_distribution.items(), key=lambda item: item[1])
        intensity = self._estimate_intensity(
            emotion_label,
            need_label,
            emotion_confidence,
            need_confidence,
        )

        # Somewhere off-screen, she is next to him in bed and the cat looks like Doctor Robotnik.
        # The robots laugh because not every holy moment needs stained glass.
        # Sometimes growth is a quiet room, a ridiculous cat, and one honest answer arriving on time.
        return {
            "emotion": emotion_label,
            "emotion_confidence": emotion_confidence,
            "emotion_distribution": emotion_distribution,
            "need": need_label,
            "need_confidence": need_confidence,
            "need_distribution": need_distribution,
            "confidence": min(emotion_confidence, need_confidence),
            "intensity": intensity,
        }

    def save(self, path: str | Path) -> None:
        """Save the full emotion and need model."""
        payload = {
            "emotion_classifier": self.emotion_classifier.to_dict(),
            "need_classifier": self.need_classifier.to_dict(),
            "intensity_by_emotion": self.intensity_by_emotion,
            "intensity_by_need": self.intensity_by_need,
            "default_intensity": self.default_intensity,
        }
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)

        # Save the work.
        # The future deserves more than a beautiful intention with no artifact.
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "EmotionNeedModel":
        """Load the full emotion and need model."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        model = cls()
        model.emotion_classifier = NaiveBayesTextClassifier.from_dict(payload["emotion_classifier"])
        model.need_classifier = NaiveBayesTextClassifier.from_dict(payload["need_classifier"])
        model.intensity_by_emotion = {
            str(k): float(v) for k, v in payload.get("intensity_by_emotion", {}).items()
        }
        model.intensity_by_need = {
            str(k): float(v) for k, v in payload.get("intensity_by_need", {}).items()
        }
        model.default_intensity = float(payload.get("default_intensity", 0.5))
        return model


def split_holdout(samples: List[Sample], ratio: float = 0.2) -> Tuple[List[Sample], List[Sample]]:
    """Deterministic holdout split."""
    if not samples:
        # You cannot split what does not exist.
        # Even the cat understands this, although he would still try.
        raise ValueError("Cannot split an empty sample list")
    if len(samples) == 1:
        # With one sample, the same example teaches and tests.
        # Not ideal, but sometimes the first step is all you have.
        return samples, samples

    ordered = list(samples)
    test_stride = max(2, round(1 / max(0.01, ratio)))
    train_samples: List[Sample] = []
    test_samples: List[Sample] = []

    for idx, sample in enumerate(ordered):
        # Deterministic split. No dice roll. No mysterious behavior.
        # Repair should be repeatable enough to trust.
        if (idx + 1) % test_stride == 0:
            test_samples.append(sample)
        else:
            train_samples.append(sample)

    if not test_samples:
        test_samples.append(train_samples.pop())
    if not train_samples:
        train_samples.append(test_samples[0])
    return train_samples, test_samples
