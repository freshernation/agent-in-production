# Week 1 Milestone — Desk behind an API

> Desk answers HTTP requests from people with keys, keeps each person's
> conversations, and refuses to start on a broken configuration.

---

## The files

| File | What it is |
|---|---|
| `app.py` | your day-4 service, plus `parse_keys` and `from_environment` |
| `A_REQUEST.md` | one request, followed by hand |

## `app.py`

Everything from day 4, unchanged, and two new functions:

| Function | What it does |
|---|---|
| `parse_keys(text)` | reads `DESK_KEYS` — `"alice:k-alice-0123456789, bob:k-bob-0123456789"` — into `{key: user}`, or raises `ValueError` saying what is wrong |
| `from_environment()` | `create_app(connect(), parse_keys(os.environ.get("DESK_KEYS", "")))` |

`parse_keys` refuses: a piece with no colon, an empty name, a key shorter than 16
characters, two users with the same key, and no keys at all. A service that starts
with a broken setting lets the wrong people in, or quietly locks the right ones out.

Run it:

```bash
DESK_KEYS="alice:k-alice-0123456789" uvicorn app:from_environment --factory
```

## `A_REQUEST.md`

Four sections, at least forty words each. Follow one `POST /chat` from arrival to
reply:

| Section | What goes in it |
|---|---|
| `## What arrives` | The bytes, the route, and what FastAPI checks before your code |
| `## Who is asking` | The key, the dependency, and what a key does not prove |
| `## What Desk does with it` | The conversation, the turn, the history |
| `## What goes back, and what does not` | The reply — and everything you keep from the caller |

---

## Check it

```bash
pytest week-01/milestone -v
```

## Friday

Your instructor restarts your server in the middle of the defence. Know what happens.
