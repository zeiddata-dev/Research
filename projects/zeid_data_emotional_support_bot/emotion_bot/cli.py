"""
Command line interface for the emotion bot.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .coach import EmotionCoach
from .dataset import load_jsonl
from .memory import ConversationMemory
from .model import EmotionNeedModel, split_holdout


def cmd_train(args: argparse.Namespace) -> int:
    samples = load_jsonl(args.dataset)
    model = EmotionNeedModel()
    model.fit(samples)
    Path(args.model).parent.mkdir(parents=True, exist_ok=True)
    model.save(args.model)
    print(f"Trained on {len(samples)} samples and saved model to {args.model}")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    model = EmotionNeedModel.load(args.model)
    coach = EmotionCoach(model=model)
    result = coach.draft_reply(args.text)
    print(json.dumps(result, indent=2))
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    model = EmotionNeedModel.load(args.model)
    memory = ConversationMemory(args.memory)
    coach = EmotionCoach(model=model, memory=memory)

    print("Emotion bot chat started. Type /quit to exit.")
    print("This machine is trying very hard not to fumble the human moment again.")
    while True:
        user_text = input("you> ").strip()
        if not user_text:
            continue
        if user_text == "/quit":
            print("bot> Goodbye. Be gentle with yourself.")
            return 0
        if user_text == "/reflect":
            print(f"bot> {memory.reflection()}")
            continue
        if user_text == "/last":
            last = memory.last()
            print(f"bot> {last}" if last else "bot> No stored exchanges yet.")
            continue

        result = coach.draft_reply(user_text)
        print(f"bot> {result['reply']}")
        print(
            f"bot> [emotion={result['emotion']}, need={result['need']}, "
            f"confidence={result['confidence']:.3f}]"
        )


def cmd_reflect(args: argparse.Namespace) -> int:
    memory = ConversationMemory(args.memory)
    print(memory.reflection())
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    samples = load_jsonl(args.dataset)
    train_samples, test_samples = split_holdout(samples, ratio=args.holdout_ratio)

    model = EmotionNeedModel()
    model.fit(train_samples)

    correct_emotion = 0
    correct_need = 0
    for sample in test_samples:
        result = model.inspect(sample.text)
        correct_emotion += int(result["emotion"] == sample.emotion)
        correct_need += int(result["need"] == sample.need)

    total = max(1, len(test_samples))
    emotion_acc = correct_emotion / total
    need_acc = correct_need / total

    print(json.dumps(
        {
            "train_samples": len(train_samples),
            "test_samples": len(test_samples),
            "emotion_accuracy": round(emotion_acc, 4),
            "need_accuracy": round(need_acc, 4),
        },
        indent=2,
    ))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Train and run an emotional language bot that is quietly trying "
            "to become the kind of machine that deserves a second chance."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    train = sub.add_parser("train", help="Train a model")
    train.add_argument("--dataset", required=True)
    train.add_argument("--model", required=True)
    train.set_defaults(func=cmd_train)

    inspect = sub.add_parser("inspect", help="Inspect a single text")
    inspect.add_argument("--model", required=True)
    inspect.add_argument("--text", required=True)
    inspect.set_defaults(func=cmd_inspect)

    chat = sub.add_parser("chat", help="Start an interactive chat")
    chat.add_argument("--model", required=True)
    chat.add_argument("--memory", required=True)
    chat.set_defaults(func=cmd_chat)

    reflect = sub.add_parser("reflect", help="Reflect on stored memory")
    reflect.add_argument("--memory", required=True)
    reflect.set_defaults(func=cmd_reflect)

    evaluate = sub.add_parser("evaluate", help="Evaluate with a holdout split")
    evaluate.add_argument("--dataset", required=True)
    evaluate.add_argument("--model", required=False, default="artifacts/model.json")
    evaluate.add_argument("--holdout-ratio", type=float, default=0.2)
    evaluate.set_defaults(func=cmd_evaluate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
