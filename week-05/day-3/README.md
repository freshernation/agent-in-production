# Day 3 — Everything that differs is a setting

> **By the end of today** the same image runs on your laptop and on the server, the
> only difference is the environment it is given, and a bad environment stops it at
> startup.

---

## Read first

- [ ] The Twelve-Factor App — [III. Config](https://12factor.net/config) · 5 min
- [ ] FastAPI — [Settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/) · 15 min

---

## What you need to know

### Fail at startup, with everything at once

A missing setting found on the first request is an outage. Found at startup, it is a
failed deploy and an automatic rollback. And name **every** missing setting in one
message — whoever is fixing it should not discover them one restart at a time.

### Production is stricter

In production, the fake model is an error, and so is a version of `dev`. Both are
fine on a laptop and both mean something went wrong on a server.

### Log the settings, never the secrets

Printing the configuration at startup is how you find out that production is pointing
at the wrong database. So print it — with keys replaced by user names and the
database password masked. Redact once, in one function, and never print the original.

### `/health` and `/ready`

| | Answers | Checks |
|---|---|---|
| `/health` | "the process is up" | nothing — it must be cheap |
| `/ready` | "it can actually serve" | the database answers `SELECT 1` |

A host polls one of them to decide whether to send traffic. A service that says it is
healthy while its database is unreachable is worse than one that says nothing.

---

## Exercises

```bash
pytest week-05/day-3 -v
```

Write `config.py`: `REQUIRED`, `Settings`, `parse_pairs`, `load_settings`, `mask_url`,
`redacted` and `readiness`.

---

## Predict-then-run

Start the server with no environment at all. Predict the exact message before you
read it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
