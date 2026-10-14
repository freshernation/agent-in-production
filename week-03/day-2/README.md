# Day 2 — A job queue is a table

> **By the end of today** you have a queue that any number of workers can take jobs
> from, and no job is ever taken by two.

---

## Read first

- [ ] SQLite — [BEGIN TRANSACTION](https://www.sqlite.org/lang_transaction.html), the part on DEFERRED, IMMEDIATE and EXCLUSIVE · 10 min
- [ ] Brandur Leach — [Transactionally staged job drains in Postgres](https://brandur.org/job-drain) · 15 min — the same idea, at scale

---

## What you need to know

### Accept now, do later

The caller asks for something slow. You write down that it was asked for, answer
**202 Accepted** with a ticket number, and do the work later. The ticket is a row:

```
id | kind | payload           | status  | attempts
 7 | chat | {"message": ...}  | queued  | 0
```

### A job's life

```
queued  →  running  →  done
                    →  queued again   (it failed, try later)
                    →  dead           (it failed too often)
```

### The claim must be atomic

Two workers both look for the oldest queued job. Both find job 7. Both mark it
running. Both do it. That is the bug every queue exists to prevent.

```python
db.execute("BEGIN IMMEDIATE")
row = db.execute("SELECT id FROM jobs WHERE status = 'queued' ORDER BY id LIMIT 1").fetchone()
db.execute("UPDATE jobs SET status = 'running', ... WHERE id = ?", (row[0],))
db.execute("COMMIT")
```

`IMMEDIATE` takes the database's write lock at `BEGIN`, so the second worker waits
at its own `BEGIN` until the first has committed — and then finds job 7 already
running. Week 2's lesson again: the look and the change must happen together.

### Failing is normal

A model is overloaded; the job fails. Put it back on the queue with the error
recorded. But not for ever: after `max_attempts`, it is **dead** — kept, so you can
read why, and never handed out again.

### Time comes in

`enqueue(db, kind, payload, now)` takes the time as an argument. Your tests decide
what time it is. Your server passes `time.time()`.

---

## Exercises

```bash
pytest week-03/day-2 -v
```

Write `jobs.py`: `SCHEMA`, `create_tables`, `enqueue`, `get`, `claim`, `finish` and
`fail`. One test runs six threads against sixty jobs and checks that no job is taken
twice.

---

## Predict-then-run

Change `BEGIN IMMEDIATE` to `BEGIN` and run the six-thread test ten times. Predict how
many runs fail. Then explain why the answer is not "all of them".

---

## Before you close the laptop

Commit, push, fill in the signal log.
