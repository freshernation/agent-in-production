# Day 4 — Fair shares, and replies as they are written

> **By the end of today** one caller cannot use up the service for everyone else, and a
> long reply starts arriving before it is finished.

---

## Read first

- [ ] Wikipedia — [Token bucket](https://en.wikipedia.org/wiki/Token_bucket), the overview and the algorithm · 10 min
- [ ] FastAPI — [Custom response: StreamingResponse](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse) · 10 min

---

## What you need to know

### A bucket of tokens

Each caller has a bucket that holds, say, five tokens. Every request takes one. The
bucket refills at a steady rate — one a second — but never past full.

| | |
|---|---|
| a burst of five | allowed: the bucket was full |
| a sixth at once | refused: 429 |
| a minute later | allowed again |
| an hour of quiet | still only five: it stops filling when full |

One bucket **per caller**. A shared bucket would let Alice's script use up Bob's
requests, which is the thing you are preventing.

### Say when to come back

```
429 Too Many Requests
Retry-After: 2
```

A client that respects `Retry-After` stops hammering you. Round up: telling it to
come back in 0 seconds is telling it to try again now.

### Time is passed in

`Bucket(capacity, per_second, clock)` takes a function that returns the time. The
tests move a fake clock forward; the server passes `time.monotonic`.

### Streaming

A long reply takes seconds to generate. Instead of waiting for all of it:

```python
def chunks(text, size):
    for start in range(0, len(text), size):
        yield text[start:start + size]

return StreamingResponse(chunks(text, 5), media_type="text/plain")
```

`yield` makes a **generator**: a function that hands back one piece at a time, when
asked. FastAPI sends each piece as it comes. Agent From Zero cut generators; this is
the one you need.

---

## Exercises

```bash
pytest week-03/day-4 -v
```

Write `limits.py`: `Bucket`, `Limiter`, `chunks` and `create_app(limiter)`.

---

## Predict-then-run

Run the app and `curl -N` the stream with `size=1` on a long text. Then put a
`time.sleep(0.1)` inside the generator. Predict what you see in the terminal.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight.
