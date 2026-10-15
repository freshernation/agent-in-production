# Day 2 — The model provider is down

> **By the end of today** Desk answers from a second provider when the first one
> fails, stops trying a provider that is clearly down, and tells users the truth
> when both are.

---

## Read first

- [ ] Martin Fowler — [CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) · 10 min
- [ ] Claude — [Errors](https://platform.claude.com/docs/en/api/errors) · 10 min

---

## What you need to know

### Three layers, in order

1. **Retry** — already in Desk, from `desk/retry.py`. Good for a blip: a 529, a
   dropped connection. Useless when the key was revoked.
2. **Fall back** — a second provider. Today's `FallbackModel` stands in front of the
   model exactly like week 4's `Recorder`, so nothing else in Desk changes.
3. **Say so** — when nothing answers, a message that says nothing was done and when
   to try again. Not a stack trace, not silence, and never a made-up answer.

### Why a different provider

A second model from the same provider shares the same outage, the same key and the
same rate limit. A fallback that goes down with the primary is not a fallback. The
milestone refuses to start if they are the same.

### The circuit breaker

Without one, every request waits for the dead provider to time out before falling
back — slow for everyone, and more load on a provider that is already struggling.
After three failures in a row, the breaker **opens**: the primary is skipped
entirely. After a cooldown it goes **half-open** and lets one request through. A
success closes it; a failure opens it again.

### The fallback is a different model

It answers differently, follows instructions differently and costs differently.
Run your eval set against it once before you trust it.

---

## Exercises

```bash
pytest week-06/day-2 -v
```

Write `fallback.py`.

---

## Predict-then-run

With a real key for each provider: set the primary's key to nonsense and send
five questions. Predict how many times the primary is called. Then count it in your
traces.

---

## Before you close the laptop

Commit, push, fill in the signal log.
