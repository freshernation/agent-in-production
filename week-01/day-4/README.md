# Day 4 — A key per caller

> **By the end of today** a request without a key gets nothing, and each person's
> conversations are theirs alone.

---

## Read first

- [ ] FastAPI — [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) · 20 min
- [ ] Python — [`secrets.compare_digest`](https://docs.python.org/3/library/secrets.html#secrets.compare_digest) · 5 min

---

## What you need to know

### Every call costs you money

An open `/chat` is a model you pay for, available to anybody who finds the URL. So
the caller sends a key, in a header:

```
Authorization: Bearer k-alice-0123456789
```

Never in the URL. URLs end up in logs, browser history and screenshots.

### One key per person

```python
KEYS = {"k-alice-0123456789": "alice", "k-bob-0123456789": "bob"}
```

One shared key would let you in or out. A key per person tells you **who**, which is
what everything after this needs: whose conversations, and from week 2, whose notes.
It also means you can take one person's key away without changing everyone's.

### Compare in constant time

`==` stops at the first character that differs, so how long it takes says how much
of a guessed key was right. `secrets.compare_digest` takes the same time either way.
And check **every** key, not stopping at the first match, for the same reason.

### Write the check once

A **dependency** is a function FastAPI runs before your route, and whose result it
hands in:

```python
def caller(authorization: str = Header(default="")) -> str:
    ...                                   # 401 if no user

@app.post("/chat")
def chat(request: ChatIn, user: str = Depends(caller)) -> ChatOut:
    ...
```

Any route that takes `user: str = Depends(caller)` is protected. `/health` does not
take it, because the platform that checks your service has no key.

### Not found, not forbidden

Bob sends Alice's conversation id. **404**, exactly as for an id that does not exist.
A 403 would tell Bob the conversation is real. To him, it does not exist.

---

## Exercises

```bash
pytest week-01/day-4 -v
```

Write `keys.py`, starting from yesterday's `chat.py`: `user_for(header, keys)`, and
`create_app(model, keys, turn=take_turn)` with `/health`, `/chat` and
`/conversations`. The rules are in the file's comments.

---

## Predict-then-run

Time `user_for` a million times with a key that is wrong in the first character, then
with one wrong in the last. Use `==` instead and do it again. Predict which pair
differs.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight.
