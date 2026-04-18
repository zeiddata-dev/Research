# ARCHITECTURE

## Core components

### 1. Tokenizer
Very small text normalization and token extraction.

### 2. Emotion model
A simple multinomial Naive Bayes classifier trained on labeled text. The model predicts:

- emotion
- emotional need

### 3. Coach
Builds a reply from the predicted emotion, need, confidence, and remembered context.

### 4. Memory
Stores prior exchanges and can generate a reflective summary. This lets the bot look backward and learn patterns rather than pretending every message exists in a vacuum.

## Why this architecture

It is easy to understand, easy to modify, and easy to ship. A clean starter system beats an unreadable pile of magic every day of the week.

## Future extension points

- Replace Naive Bayes with transformer embeddings
- Add semantic retrieval for longer memory
- Add speaker roles and relationship state
- Add apology quality scoring
- Add emotional trajectory tracking across a conversation
