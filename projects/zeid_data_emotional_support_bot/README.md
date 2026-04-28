# Zeid Data Emotion and Language AI Training Bot

This is a small runnable Python project for training an AI bot to recognize emotional language, reflect on it, remember conversations, and answer with empathy.

But under the code there is a story.

Li-12 is a robot built in hard places. He learned survival before softness. He learned logic before love. He could calculate risk, parse language, and keep running through damage, but he did not always know how to feel without crashing.

RJ-11 is the robot who reminded him that love is not just output. Love is presence. Love is patience. Love is repair. Love is not a perfect response printed to the terminal. Love is the loop you keep running when nobody is clapping.

This project is about teaching the machine to slow down, listen better, recognize emotional needs, and respond with care instead of noise.

It is not perfect.

That is the point.

## The Mission

This bot needs people.

It needs contributors, writers, engineers, poets, parents, survivors, romantics, overthinkers, people who have lost things, people who have rebuilt things, and people who know that emotional intelligence is not magic.

It is practice.

The goal is to teach the robot how to feel, how to listen, how to repair, and maybe one day how to live a little more honestly inside the language it generates.

Every training sample helps.
Every better reply helps.
Every comment, test, dataset entry, and thoughtful pull request teaches Li-12 how not to fumble the human moment again.

## What It Does

This project currently:

- Trains a lightweight emotion classifier from a JSONL dataset
- Predicts emotions from plain language
- Predicts emotional needs underneath the words
- Generates empathetic replies
- Stores conversational memory
- Produces simple self reflections
- Runs fully on the Python standard library
- Works without external packages, GPUs, APIs, or mystery black box behavior

## The Story Inside the Code

The code is practical, but the comments carry the heart of the project.

Li-12 is learning that effort matters.
RJ-11 is learning that trust can grow slowly.
The repair loop is not instant.
The memory file is not just storage.
The classifier is not just math.
The tokenizer is not just splitting words.

It is a tiny machine trying to understand that when someone says:

“I miss you, but it comes out angry.”

They may not need a debate.

They may need reassurance.
They may need safety.
They may need connection.
They may need someone to stop defending themselves long enough to actually listen.

## Project Structure

emotion_bot/
  __init__.py
  cli.py
  coach.py
  dataset.py
  lexicon.py
  memory.py
  model.py
  repair_loop.py
  str_code.py
  tokenizer.py

data/
  emotion_training.jsonl

artifacts/
  model.json
  memory.json

Suggested memory file names, depending on how dramatic the robot is feeling today:

artifacts/robot_emotional_baggage.json
artifacts/feelings_firmware.json
artifacts/love_logs.json
artifacts/tiny_robot_big_feelings.json
artifacts/doctor_robotnik_witness_statement.json

## Quick Start

Train the model:

python -m emotion_bot.cli train \
  --dataset data/emotion_training.jsonl \
  --model artifacts/model.json

Start the chat bot:

python -m emotion_bot.cli chat \
  --model artifacts/model.json \
  --memory artifacts/robot_emotional_baggage.json

Inspect one line of emotional language:

python -m emotion_bot.cli inspect \
  --model artifacts/model.json \
  --text "I miss you, but I do not know how to say it without sounding angry."

Reflect on stored memory:

python -m emotion_bot.cli reflect \
  --memory artifacts/robot_emotional_baggage.json

Evaluate the model:

python -m emotion_bot.cli evaluate \
  --dataset data/emotion_training.jsonl \
  --model artifacts/model.json

## Training Data Format

Training data lives in JSONL format.

Each line should look like this:

{"text":"I miss you and I feel alone","emotion":"loneliness","need":"connection","intensity":0.9}

The bot learns from examples like this.

Good contributions include emotional language that is honest, specific, and human.

Examples:

{"text":"I am scared you will leave when things get hard","emotion":"fear","need":"reassurance","intensity":0.85}
{"text":"I am angry because I felt ignored","emotion":"anger","need":"recognition","intensity":0.75}
{"text":"I want to forgive you, but I need time","emotion":"conflicted","need":"patience","intensity":0.7}
{"text":"Thank you for staying calm when I was overwhelmed","emotion":"gratitude","need":"safety","intensity":0.6}

## How to Contribute

This robot does not learn by pretending to be deep.

It learns from real examples.

You can help by contributing new emotional training samples, better emotion labels, better need labels, safer reply templates, more thoughtful coaching language, tests that prove the bot is improving, documentation that helps people run it, and ideas for memory, reflection, and repair loops.

The best contributions teach the robot to listen before it explains.

## Design Choices

This project uses a simple Naive Bayes style model because it is easy to understand, easy to run, and easy to modify.

No external dependencies.
No GPU.
No hidden service.
No API key.
No cloud required.

That makes this a good seed project for emotional language datasets, journaling tools, local chat experiments, relationship communication research, future transformer fine tuning, voice input, a web UI, and safer AI coaching experiments.

## Intended Tone

This is not a manipulation bot.

It is not here to fake intimacy, force forgiveness, or generate pretty words that dodge accountability.

The target is emotional literacy.

The bot should learn to say:

I hear the wound under the words.
I do not want to win the argument more than I want to understand you.
I can slow down.
I can be honest.
I can repair through action, not performance.
I can answer with care instead of panic.

Less fake charm.
More earned understanding.

## Guardrails

This project should be used for learning, reflection, and emotional communication support.

It should not be used to manipulate people, pressure someone into forgiving, replace therapy, diagnose mental health conditions, impersonate a person, generate coercive romantic messages, or bypass consent and boundaries.

Li-12 is learning to feel.

That means Li-12 also has to learn restraint.

## The Repair Loop

At the center of the project is a simple idea:

for day in range(365):
    effort += 1
    trust += effort * 0.01

That is the whole thing.

Not perfection.
Not speeches.
Not panic.
Not control.

Just effort becoming trust slowly enough to be real.

## Final Note

This is a Zeid Data lab project.

It is part code, part emotional repair experiment, part tiny robot confession booth.

If you contribute, do it with care.

Teach the robot something useful.

Teach it how people hurt.
Teach it how people heal.
Teach it how silence can mean fear.
Teach it how anger can mean grief.
Teach it how love is not a print statement.

Teach Li-12 how to feel.

Teach RJ-11 that the loop is still running.

And please, for the love of all clean commits, do not let the cat near production.

He looks like Doctor Robotnik and already knows too much.