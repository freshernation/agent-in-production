# Day 4 — What each user may make Desk do

> **By the end of today** a reader can search but not add, a writer can add but not
> delete, and a model that asks for more gets a refusal.

---

## Read first

- [ ] OWASP — [LLM06: Excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) · 10 min

---

## What you need to know

### A role is a set of tool names

```python
READER = {"list_titles", "find_notes", "calculate"}
WRITER = READER | {"add_note"}
OWNER  = WRITER | {"delete_note", "share_note"}
```

Each includes the one below. `READER < WRITER` is `True` for sets: a strict subset.

### A user nobody gave a role may do nothing

`allowed("admin")` returns an empty set. A typo in the configuration should lock a
user out, not let them in. Fail closed, as the approval gate did in Agent From Zero.

### Two locks

**Hide it.** `schemas_for(role, SCHEMAS)` tells the model only about the tools this
user may use. A tool it has never heard of is a tool it will rarely ask for.

**Refuse it anyway.** Rarely is not never. A model can name a tool it was not offered
— it has seen the name in a note, or it guesses. So `guard(tools, role)` replaces
every forbidden tool with one that answers:

```
Refused: the reader role cannot use delete_note.
```

Either lock alone fails sometimes. Together, the model has to be both told about a
tool and allowed it.

### Return a copy

`allowed` returns `set(ROLES[role])`, not the set itself. Hand out the real set and
the first caller who adds to it changes the role for everyone, for as long as the
server runs.

---

## Exercises

```bash
pytest week-02/day-4 -v
```

Write `permissions.py`: the three roles, `ROLES`, `allowed`, `schemas_for`,
`refusal` and `guard`.

---

## Predict-then-run

Run a reader's Desk against a real provider and ask it to delete a note. Predict
whether the model even tries, given it was never told `delete_note` exists.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight.
