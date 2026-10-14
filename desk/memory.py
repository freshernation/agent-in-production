import json
import os
from pathlib import Path


def estimate_tokens(messages):
    characters = 0
    for message in messages:
        characters = characters + len(message["content"])
    return characters // 4


def trim(messages, max_turns):
    starts = []
    for position, message in enumerate(messages):
        if message["role"] == "user":
            starts.append(position)
    if len(starts) <= max_turns:
        return list(messages)

    kept = []
    for message in messages[starts[-max_turns]:]:
        copy = {}
        for key in message:
            if not key.startswith("_"):
                copy[key] = message[key]
        kept.append(copy)
    return kept


def carry(history, result, max_turns=10):
    if result["stopped"] != "done":
        return history
    return trim(result["messages"], max_turns)


def _path():
    return Path(os.environ.get("MEMORY_FILE", "memory.json"))


def _facts():
    path = _path()
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return []


def remember(fact):
    facts = _facts()
    if fact in facts:
        return "I already know that."
    facts.append(fact)
    _path().write_text(json.dumps(facts, indent=2))
    return "Remembered."


def recall(word=""):
    facts = _facts()
    if not facts:
        return "Nothing remembered yet."
    matches = []
    for fact in facts:
        if word.lower() in fact.lower():
            matches.append(fact)
    if not matches:
        return f"Nothing remembered about '{word}'."
    return "\n".join(matches)


MEMORY_SCHEMAS = [
    {
        "name": "remember",
        "description": (
            "Save one lasting fact about the user for future conversations, such "
            "as a preference, a name or a standing arrangement. Do not use for "
            "to-do items - those are notes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "fact": {"type": "string",
                         "description": "One complete sentence, e.g. 'Sam is vegetarian.'"},
            },
            "required": ["fact"],
        },
    },
    {
        "name": "recall",
        "description": (
            "Look up lasting facts saved about the user in earlier conversations. "
            "Call this at the start of any task where the user's preferences or "
            "personal details could matter."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "word": {"type": "string",
                         "description": "A word to search for. Leave out to list everything."},
            },
            "required": [],
        },
    },
]

MEMORY_TOOLS = {"remember": remember, "recall": recall}
