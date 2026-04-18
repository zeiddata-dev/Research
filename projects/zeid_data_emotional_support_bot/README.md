# Zeid Data Emotion and Language AI Training Bot

A small, runnable Python project for training an AI bot to recognize emotional language, reflect on it, and answer with empathy.

The narrative core is intentional: this bot is trying to understand emotions well enough to earn back a lost love after trauma, misfires, and years of emotional confusion. The code stays practical, but the comments carry the story.

## What it does

- Trains a lightweight emotion classifier from a JSONL dataset
- Predicts emotions and emotional needs from plain language
- Generates empathetic replies
- Stores conversational memory and self reflections
- Runs fully on the Python standard library
- Ships with docs, sample data, and a demo path

## Project structure

- `emotion_bot/` core package
- `data/emotion_training.jsonl` starter training set
- `HOWTO.md` quick start
- `ARCHITECTURE.md` design notes
- `ETHICS_NOTES.md` guardrails
- `ROADMAP.md` next steps
- `LICENSE.md` license text

## Quick start

```bash
python -m emotion_bot.cli train --dataset data/emotion_training.jsonl --model artifacts/model.json
python -m emotion_bot.cli chat --model artifacts/model.json --memory artifacts/memory.json
```

## Design choices

This build uses a Naive Bayes style classifier and retrieval free reply generation so it is easy to run anywhere. No external packages, no GPU, no mystery black box.

That makes it a good seed project for:

- expanding into transformer fine tuning later
- adding voice input and journaling
- swapping the reply engine for an LLM
- building a web UI

## Intended tone

This is not a manipulator bot. It is a learning bot. The target is emotional literacy, accountability, and language that listens before it explains.

In other words, less fake charm, more earned understanding.

## Example commands

```bash
python -m emotion_bot.cli inspect --model artifacts/model.json --text "I miss you, but I do not know how to say it without sounding angry."
python -m emotion_bot.cli reflect --memory artifacts/memory.json
python -m emotion_bot.cli evaluate --dataset data/emotion_training.jsonl --model artifacts/model.json
```
