# Day 3 — Desk behind POST /chat

> **By the end of today** Desk answers over HTTP, and remembers a conversation from
> one request to the next.

---

## Read first

- [ ] FastAPI — [Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) · 15 min
- [ ] FastAPI — [Testing](https://fastapi.tiangolo.com/tutorial/testing/) · 10 min

---

## What you need to know

### HTTP forgets

Every request arrives on its own. The server does not know that this message follows
the last one unless the request says so. So the first reply hands back a
**conversation id**, and every later message sends it:

```
POST /chat  {"message": "Remember milk"}
→           {"conversation_id": "9f3c1a7b2d04", "reply": "Saved."}

POST /chat  {"message": "What do I have?", "conversation_id": "9f3c1a7b2d04"}
```

### The history lives on the server

Desk's history is the message list from Agent From Zero. Between requests it has to
live somewhere. Today: a dictionary inside `create_app`, `{conversation_id: history}`.

Why not a global variable? Two reasons. Every test would share it. And it is still a
dictionary in one process: restart the server and every conversation is gone. That
is next week's problem, and you should see it happen first.

### Hand the app what it needs

```python
def create_app(model, turn=take_turn) -> FastAPI:
```

The model and the turn function come in as arguments. The tests pass a fake turn
that just remembers; the real server passes Desk. Agent From Zero's oldest rule,
one level up.

### When something inside breaks

If the turn raises, the caller must get a **503** and a sentence — not a traceback.
A traceback shows file paths and library versions to whoever sent the request. The
detail belongs in your logs. You have no logs yet; week 4.

---

## Exercises

```bash
pytest week-01/day-3 -v
```

Write `chat.py`: `ChatIn`, `ChatOut`, `new_id`, and `create_app(model, turn=take_turn)`
with `GET /health` and `POST /chat`. The rules are in the file's comments.

---

## Predict-then-run

Run it against a real provider: `AGENT_PROVIDER=claude uvicorn ...`. Send two
messages in one conversation. Then stop the server, start it again, and send a third
with the same id. Predict the status code first.

---

## Before you close the laptop

Commit, push, fill in the signal log.
