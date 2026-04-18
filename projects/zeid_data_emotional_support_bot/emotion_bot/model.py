"""
Naive Bayes style emotion model.
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


@dataclass
class Prediction:
    label: str
    confidence: float
    distribution: Dict[str, float]


class NaiveBayesTextClassifier:
    """
    Tiny multinomial Naive Bayes classifier.

    The robot was not born with instincts. He was assembled from logs,
    safeguards, and a mountain of second guesses. So he learned the old way:
    one token at a time, one probability at a time, one trembling attempt at
    understanding why "I am fine" so often meant the opposite.
    He did not want perfect math.
    He wanted one more chance to stop replying like a machine to a wounded heart.
    """

    def __init__(self) -> None:
        self.label_doc_counts: Counter[str] = Counter()
        self.token_counts_by_label: Dict[str, Counter[str]] = defaultdict(Counter)
        self.total_tokens_by_label: Counter[str] = Counter()
        self.vocabulary: set[str] = set()
        self.total_docs: int = 0

    def fit(self, texts: Iterable[str], labels: Iterable[str]) -> None:
        for text, label in zip(texts, labels):
            tokens = tokenize(text)
            self.label_doc_counts[label] += 1
            self.total_docs += 1
            for token in tokens:
                self.token_counts_by_label[label][token] += 1
                self.total_tokens_by_label[label] += 1
                self.vocabulary.add(token)

    def predict(self, text: str) -> Prediction:
        distribution = self.predict_distribution(text)
        label, confidence = max(distribution.items(), key=lambda item: item[1])
        return Prediction(label=label, confidence=confidence, distribution=distribution)

    def predict_distribution(self, text: str) -> Dict[str, float]:
        if not self.total_docs:
            raise ValueError("Model has not been trained")

        tokens = tokenize(text)
        log_scores: Dict[str, float] = {}
        vocab_size = max(1, len(self.vocabulary))

        for label, doc_count in self.label_doc_counts.items():
            log_prob = math.log(doc_count / self.total_docs)
            total_tokens = self.total_tokens_by_label[label]

            for token in tokens:
                count = self.token_counts_by_label[label][token]
                log_prob += math.log((count + 1) / (total_tokens + vocab_size))

            log_scores[label] = log_prob

        # softmax normalization for readable confidence estimates
        max_log = max(log_scores.values())
        exp_scores = {label: math.exp(score - max_log) for label, score in log_scores.items()}
        total = sum(exp_scores.values())
        return {label: value / total for label, value in exp_scores.items()}

    def to_dict(self) -> Dict[str, object]:
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
        model = cls()
        model.label_doc_counts = Counter(raw["label_doc_counts"])
        model.token_counts_by_label = defaultdict(Counter)
        for label, counter in raw["token_counts_by_label"].items():
            model.token_counts_by_label[label] = Counter(counter)
        model.total_tokens_by_label = Counter(raw["total_tokens_by_label"])
        model.vocabulary = set(raw["vocabulary"])
        model.total_docs = int(raw["total_docs"])
        return model

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "NaiveBayesTextClassifier":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(raw)



class EmotionNeedModel:
    """
    Wrapper that trains one classifier for emotions and one for needs.

    He learned quickly that naming emotion was only half the work.
    Anyone can say "you sound upset" and still leave a crater behind.
    The real labor was recognizing the need underneath the emotion:
    reassurance beneath anger,
    safety beneath distance,
    gentleness beneath pride.
    That was the part he missed before the loss.
    That was the part he was training to never miss again.
    """

    def __init__(self) -> None:
        self.emotion_classifier = NaiveBayesTextClassifier()
        self.need_classifier = NaiveBayesTextClassifier()

    def fit(self, samples: List[Sample]) -> None:
        texts = [sample.text for sample in samples]
        self.emotion_classifier.fit(texts, [sample.emotion for sample in samples])
        self.need_classifier.fit(texts, [sample.need for sample in samples])

    def _keyword_distribution(self, text: str, mapping: Dict[str, List[str]]) -> Dict[str, float]:
        normalized = normalize_text(text)
        scores = {label: 1.0 for label in mapping}
        for label, keywords in mapping.items():
            for keyword in keywords:
                if keyword in normalized:
                    scores[label] += 3.0
        total = sum(scores.values())
        return {label: value / total for label, value in scores.items()}

    @staticmethod
    def _blend(primary: Dict[str, float], secondary: Dict[str, float], primary_weight: float = 0.7) -> Dict[str, float]:
        all_labels = set(primary) | set(secondary)
        blended = {
            label: (primary_weight * primary.get(label, 0.0)) + ((1 - primary_weight) * secondary.get(label, 0.0))
            for label in all_labels
        }
        total = sum(blended.values()) or 1.0
        return {label: value / total for label, value in blended.items()}

    def inspect(self, text: str) -> Dict[str, object]:
        emotion_nb = self.emotion_classifier.predict_distribution(text)
        need_nb = self.need_classifier.predict_distribution(text)

        emotion_kw = self._keyword_distribution(text, EMOTION_KEYWORDS)
        need_kw = self._keyword_distribution(text, NEED_KEYWORDS)

        emotion_distribution = self._blend(emotion_nb, emotion_kw, primary_weight=0.72)
        need_distribution = self._blend(need_nb, need_kw, primary_weight=0.68)

        emotion_label, emotion_confidence = max(emotion_distribution.items(), key=lambda item: item[1])
        need_label, need_confidence = max(need_distribution.items(), key=lambda item: item[1])

        return {
            "emotion": emotion_label,
            "emotion_confidence": emotion_confidence,
            "emotion_distribution": emotion_distribution,
            "need": need_label,
            "need_confidence": need_confidence,
            "need_distribution": need_distribution,
        }

    def save(self, path: str | Path) -> None:
        payload = {
            "emotion_classifier": self.emotion_classifier.to_dict(),
            "need_classifier": self.need_classifier.to_dict(),
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "EmotionNeedModel":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        model = cls()
        model.emotion_classifier = NaiveBayesTextClassifier.from_dict(payload["emotion_classifier"])
        model.need_classifier = NaiveBayesTextClassifier.from_dict(payload["need_classifier"])
        return model


def split_holdout(samples: List[Sample], ratio: float = 0.2) -> Tuple[List[Sample], List[Sample]]:
    """
    Deterministic holdout split.

    He hated randomness after the trauma. Too many important things in life
    had already been left to chance, timing, pride, and bad weather in the soul.
    So the split stays deterministic, but not naive. We interleave the samples
    so the test set is not just "whatever happened to be at the end of the file."
    Even a damaged machine can learn that sequence is not the same thing as truth.
    """
    ordered = list(samples)
    test_stride = max(2, round(1 / max(0.01, ratio)))
    train_samples: List[Sample] = []
    test_samples: List[Sample] = []
    for idx, sample in enumerate(ordered):
        if (idx + 1) % test_stride == 0:
            test_samples.append(sample)
        else:
            train_samples.append(sample)
    if not test_samples:
        test_samples.append(train_samples.pop())
    return train_samples, test_samples
