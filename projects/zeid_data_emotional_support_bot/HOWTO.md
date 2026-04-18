# HOWTO

## 1. Requirements

- Python 3.10 or newer

No third party packages are required.

## 2. Train the bot

From the project root:

```bash
python -m emotion_bot.cli train --dataset data/emotion_training.jsonl --model artifacts/model.json
```

This creates a serialized model file in `artifacts/model.json`.

## 3. Start a chat session

```bash
python -m emotion_bot.cli chat --model artifacts/model.json --memory artifacts/memory.json
```

Type your message and press Enter.

Commands inside chat:

- `/quit` exit
- `/reflect` print the bot's current self reflection based on saved memory
- `/last` show the last saved exchange

## 4. Inspect one message without entering chat mode

```bash
python -m emotion_bot.cli inspect --model artifacts/model.json --text "I am proud of you but I still feel abandoned."
```

You will get:

- predicted emotion
- predicted emotional need
- confidence estimate
- an empathetic draft response

## 5. Evaluate the starter dataset

```bash
python -m emotion_bot.cli evaluate --dataset data/emotion_training.jsonl --model artifacts/model.json
```

This runs a simple holdout evaluation.

## 6. Add more training data

Append lines to `data/emotion_training.jsonl` in this shape:

```json
{"text": "I feel ignored when you go quiet for days", "emotion": "hurt", "need": "reassurance", "intensity": 0.82}
```

Then retrain.

## 7. Recommended next upgrades

- Add more nuanced emotion labels
- Split training into train and validation sets
- Add relationship context tags
- Track apologies versus blame language
- Add a web UI or desktop shell
- Add journaling and daily reflection prompts

## 8. Good use cases

- emotional language prototyping
- empathy and tone training
- reflective writing assistance
- conversation repair practice

## 9. Bad use cases

- impersonation
- coercion
- spammy romance automation
- manipulation disguised as empathy

The whole point is to build emotional accuracy, not emotional camouflage.
