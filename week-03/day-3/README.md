# Day 3 — A worker that dies

> **By the end of today** a worker runs jobs, a job whose worker vanished is picked up
> again, and something that must happen once happens once.

---

## Read first

- [ ] Stripe — [Designing robust and predictable APIs with idempotency](https://stripe.com/blog/idempotency) · 15 min

---

## What you need to know

### One job at a time

```python
outcome = run_once(db, {"chat": handle_chat}, "worker-1", now)    # "idle", "done" or "failed"
```

Claim, look up the handler by the job's kind, run it, finish or fail. A handler that
raises fails the job — it does not crash the worker, which goes on to the next one.
A job whose kind has no handler dies at once: no retry will grow one.

### The worker that never comes back

A worker claims job 7 and the machine is switched off. It never calls `finish` or
`fail`. Job 7 says `running` for ever.

So running jobs have a deadline. Anything claimed more than `timeout` seconds ago is
put back on the queue:

```python
requeue_stale(db, now, timeout=300)
```

The claim already counted an attempt, so a job that kills its worker every time
still runs out of attempts and dies.

### Which means a job can run twice

Worse: the worker did the work — sent the email — and died before `finish`. The job
goes back on the queue and the next worker sends it again.

You cannot prevent a job running twice. You can make running it twice harmless:

```python
once(db, f"share:{job_id}", lambda: share_note("bank", "sam@example.com"))
```

The first time, it runs and records the result under the key. Every later time, it
returns the recorded result and does nothing. This is **idempotency**, and it is why
payment APIs ask you for an idempotency key.

---

## Exercises

```bash
pytest week-03/day-3 -v
```

Copy `jobs.py` here. Write `worker.py`: `run_once`, `requeue_stale`, `EFFECTS` and
`once`.

---

## Predict-then-run

Put a `once` around a print, with a fixed key. Run it, stop the program, run it
again. Predict what prints the second time.

---

## Before you close the laptop

Commit, push, fill in the signal log.
