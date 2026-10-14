def tokens(text):
    return len(text) // 4


def sizes(messages):
    found = {"user": 0, "assistant": 0, "tool": 0, "total": 0}
    for message in messages:
        size = tokens(message["content"])
        found[message["role"]] = found[message["role"]] + size
        found["total"] = found["total"] + size
    return found


def shorten_old_results(messages, keep_last=2, limit=200):
    positions = []
    for position, message in enumerate(messages):
        if message["role"] == "tool":
            positions.append(position)
    if keep_last > 0:
        recent = positions[-keep_last:]
    else:
        recent = []

    shortened = []
    for position, message in enumerate(messages):
        copy = dict(message)
        if message["role"] == "tool" and position not in recent:
            content = message["content"]
            if len(content) > limit:
                removed = len(content) - limit
                copy["content"] = content[:limit] + f" [shortened: {removed} characters removed]"
        shortened.append(copy)
    return shortened


def split_turns(messages):
    turns = []
    for message in messages:
        if message["role"] == "user" or not turns:
            turns.append([])
        turns[-1].append(message)
    return turns


SUMMARY_SYSTEM = (
    "You summarise the earlier part of a conversation between a user and an "
    "assistant that manages their notes. Keep every fact the assistant will need "
    "later: what the user asked for, what was saved, deleted or shared, exact "
    "titles, and anything the user said about themselves. Leave out greetings and "
    "the wording of tool calls. Write five sentences or fewer."
)


def transcript(messages):
    lines = []
    for message in messages:
        lines.append(f"{message['role']}: {message['content']}")
    return "\n".join(lines)


def summarise(model, messages):
    reply = model.chat([{"role": "user", "content": transcript(messages)}],
                       system=SUMMARY_SYSTEM)
    return reply["text"]


def compact(model, messages, keep_turns=3):
    turns = split_turns(messages)
    if len(turns) <= keep_turns:
        return list(messages)

    older = []
    for turn in turns[:-keep_turns]:
        older.extend(turn)
    summary = summarise(model, older)

    kept = []
    for turn in turns[-keep_turns:]:
        for message in turn:
            copy = {}
            for key in message:
                if not key.startswith("_"):
                    copy[key] = message[key]
            kept.append(copy)
    kept[0]["content"] = (
        f"Summary of the conversation so far: {summary}\n\n{kept[0]['content']}"
    )
    return kept


def should_compact(used, window, fraction=0.5):
    return used >= window * fraction
