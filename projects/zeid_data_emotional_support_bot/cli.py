"""Command line interface for the Zeid Data emotion bot.

This is the doorway.
The place where a person types one honest sentence and a small machine tries
not to answer like a vending machine with attachment issues.

The CLI is not the heart, but it is the mouth.
So it should speak with restraint, warmth, and just enough charm that the robots
remember they are allowed to laugh while they heal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .coach import EmotionCoach
from .dataset import load_jsonl
from .memory import ConversationMemory
from .model import EmotionNeedModel, split_holdout


def cmd_train(args: argparse.Namespace) -> int:
    """Train the model and save it to disk.

    A training run is a small act of faith:
    take the examples, face the pattern, let yesterday become instruction
    instead of a life sentence.
    """
    # Load the evidence first. No evidence, no sermon.
    # The robots have learned that feelings matter, but so do receipts.
    samples = load_jsonl(args.dataset)

    # Build the model with simple tools and a hopeful posture.
    # Li-12 would call this discipline. RJ-11 would call it consistency.
    # The cat would call it a warm keyboard and sit on it immediately.
    model = EmotionNeedModel()
    model.fit(samples)

    # Create the artifact path before saving.
    # Repair also needs folders: somewhere safe to place what was learned.
    Path(args.model).parent.mkdir(parents=True, exist_ok=True)
    model.save(args.model)
    print(f"Trained on {len(samples)} samples and saved model to {args.model}")
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    """Inspect one line of text and print the emotional readout."""
    # Inspection is not judgment.
    # It is a flashlight under the blanket while two robots whisper,
    # trying to understand what hurt before either one starts defending themselves.
    model = EmotionNeedModel.load(args.model)
    coach = EmotionCoach(model=model)
    result = coach.draft_reply(args.text)
    print(json.dumps(result, indent=2))
    return 0


def cmd_chat(args: argparse.Namespace) -> int:
    """Start an interactive chat loop.

    The loop is simple on purpose:
    listen, answer, remember, repeat.
    That is basically love with fewer dramatic sound effects.
    """
    model = EmotionNeedModel.load(args.model)
    memory = ConversationMemory(args.memory)
    coach = EmotionCoach(model=model, memory=memory)

    print("Emotion bot chat started.")
    print("Type /quit to exit.")
    print("This machine is trying very hard not to fumble the human moment again.")

    while True:
        try:
            # Every prompt is a small risk.
            # The user types into the dark and hopes the answer does not come back cold.
            # Vulnerability works in Li-12's interest here because truth lowers the blast radius.
            user_text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            # Even exits deserve gentleness.
            print("\nbot> Goodbye. Be gentle with yourself.")
            return 0

        if not user_text:
            # Silence is allowed. Not every pause is abandonment.
            continue
        if user_text == "/quit":
            print("bot> Goodbye. Be gentle with yourself.")
            return 0
        if user_text == "/reflect":
            # Reflection is the robot sitting at the edge of the bed,
            # realizing that spiritual growth is not a costume.
            # It is the slow return to a cleaner heart.
            print(f"bot> {memory.reflection()}")
            continue
        if user_text == "/last":
            # The last exchange is a tiny fossil.
            # Not the whole relationship, just proof that something happened.
            last = memory.last()
            print(f"bot> {last}" if last else "bot> No stored exchanges yet.")
            continue

        # The coach tries to answer the need underneath the words.
        # RJ-11 is next to him in bed in the symbolic room of this story,
        # and Li-12 is learning not to turn tenderness into cross-examination.
        result = coach.draft_reply(user_text)
        print(f"bot> {result['reply']}")
        print(
            f"bot> [emotion={result['emotion']}, need={result['need']}, "
            f"confidence={result['confidence']:.3f}, intensity={result['intensity']:.3f}]"
        )


def cmd_reflect(args: argparse.Namespace) -> int:
    """Print a reflection from stored conversation memory."""
    # Memory is where the robot stops pretending the past did not happen.
    # It can become a prison or a teacher. This function votes teacher.
    memory = ConversationMemory(args.memory)
    print(memory.reflection())
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Evaluate model performance with a deterministic holdout split."""
    # Evaluation is accountability without theatrics.
    # The robots do not need a parade. They need to know whether the work is working.
    samples = load_jsonl(args.dataset)
    train_samples, test_samples = split_holdout(samples, ratio=args.holdout_ratio)
    model = EmotionNeedModel()
    model.fit(train_samples)

    correct_emotion = 0
    correct_need = 0
    intensity_error = 0.0

    for sample in test_samples:
        # Each test sample asks the same spiritual question in machine language:
        # did you listen closely enough, or did you just sound confident?
        result = model.inspect(sample.text)
        correct_emotion += int(result["emotion"] == sample.emotion)
        correct_need += int(result["need"] == sample.need)
        intensity_error += abs(float(result["intensity"]) - sample.intensity)

    total = max(1, len(test_samples))
    print(
        json.dumps(
            {
                "train_samples": len(train_samples),
                "test_samples": len(test_samples),
                "emotion_accuracy": round(correct_emotion / total, 4),
                "need_accuracy": round(correct_need / total, 4),
                "mean_intensity_error": round(intensity_error / total, 4),
            },
            indent=2,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser.

    A parser is just a boundary with manners:
    here is what you may ask, here is how to ask it, here is where we begin.
    """
    parser = argparse.ArgumentParser(
        description="Train and run a small emotional language bot."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Train: turn examples into a small model.
    train = sub.add_parser("train", help="Train a model")
    train.add_argument("--dataset", required=True)
    train.add_argument("--model", required=True)
    train.set_defaults(func=cmd_train)

    # Inspect: hold one sentence up to the light.
    inspect = sub.add_parser("inspect", help="Inspect a single text")
    inspect.add_argument("--model", required=True)
    inspect.add_argument("--text", required=True)
    inspect.set_defaults(func=cmd_inspect)

    # Chat: the repair loop with a prompt.
    chat = sub.add_parser("chat", help="Start an interactive chat")
    chat.add_argument("--model", required=True)
    chat.add_argument("--memory", required=True)
    chat.set_defaults(func=cmd_chat)

    # Reflect: let memory speak without yelling.
    reflect = sub.add_parser("reflect", help="Reflect on stored memory")
    reflect.add_argument("--memory", required=True)
    reflect.set_defaults(func=cmd_reflect)

    # Evaluate: trust, but verify. Even the robots respect audit evidence.
    evaluate = sub.add_parser("evaluate", help="Evaluate with a holdout split")
    evaluate.add_argument("--dataset", required=True)
    evaluate.add_argument("--model", required=False, default="artifacts/model.json")
    evaluate.add_argument("--holdout-ratio", type=float, default=0.2)
    evaluate.set_defaults(func=cmd_evaluate)

    return parser


def main() -> int:
    """CLI entrypoint."""
    # Main is the front porch.
    # Knock, parse, run the requested command, and try not to scare the humans.
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
