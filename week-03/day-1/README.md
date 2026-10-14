# Day 1 — What blocks

> **By the end of today** you can tell code that waits from code that blocks, and make
> several waits happen at once.

Agent From Zero cut `async` and said why: it was not what you needed then. It is
now. A service waits on things — the model, the database — and while one request
waits, others should run.

---

## Read first

- [ ] Python — [Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html), up to "Running tasks concurrently" and `to_thread` · 25 min
- [ ] FastAPI — [Concurrency and async / await](https://fastapi.tiangolo.com/async/) · 15 min

---

## What you need to know

### Waiting and blocking

```python
await asyncio.sleep(1)     # waits: other work runs meanwhile
time.sleep(1)              # blocks: nothing else runs
```

`await` is a promise to let other work run while you wait. A blocking call makes no
such promise. A model call through an ordinary SDK, a `sqlite3` query, any normal
library function — to asyncio, all of those are `time.sleep`.

### At once, with gather

```python
results = await asyncio.gather(slow_lookup(0.1), slow_lookup(0.1), slow_lookup(0.1))
```

Three 0.1-second waits take about 0.1 seconds, and the results come back in the
order you asked.

### The mistake

```python
async def run_blocking_wrong(delays):
    for seconds in delays:
        blocking_lookup(seconds)          # inside async, still blocks
```

`async def` on the outside does not make the inside wait politely. You will write
this on purpose today, and the test times it.

### The fix: another thread

```python
await asyncio.gather(*[asyncio.to_thread(blocking_lookup, s) for s in delays])
```

`to_thread` runs the blocking call in a thread, and gives you something you can
await. You met it in Agent From Zero week 7 Thursday.

### What this means for FastAPI

A route defined with plain `def` is run in a thread for you. A route defined with
`async def` runs on the event loop — so if it blocks, **every** request waits. The
rule: `async def` only when everything inside is awaited. Otherwise plain `def`.
Every route in this course so far is plain `def`, and now you know why.

---

## Exercises

```bash
pytest week-03/day-1 -v
```

Write `concurrency.py`: `slow_lookup`, `blocking_lookup`, `run_all`,
`run_blocking_wrong`, `run_blocking_right` and `timed`.

---

## Predict-then-run

Change one of week 2's routes to `async def` without changing what is inside it.
Fire ten requests at it at once. Predict the total time against the plain `def`
version.

---

## Before you close the laptop

Commit, push, fill in the signal log.
