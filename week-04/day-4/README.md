# Day 4 — To the platform, and back into the evals

> **By the end of today** your traces and ratings appear in Langfuse, and a bad trace
> becomes an eval case in the suite you built in Agent From Zero.

---

## Read first

- [ ] Langfuse — [Python SDK: instrumentation](https://langfuse.com/docs/observability/sdk/python/instrumentation), the parts on observations, trace attributes and flushing · 20 min
- [ ] Langfuse — [Trace IDs and distributed tracing](https://langfuse.com/docs/observability/features/trace-ids-and-distributed-tracing) · 10 min

---

## What you need to know

### Export later, not during the request

Sending to the platform inside `/chat` makes every request slower and makes a
platform outage your outage. So the request writes to your database, and a separate
loop sends what has not been sent. Week 3's lesson — accept now, do later — applied
to your own records.

### Mark it sent only after it is sent

```python
client.trace(trace)                    # may raise
db.execute("UPDATE traces SET exported = 1 ...")
```

The other way round, an outage loses everything it touched, permanently and silently.

### A score waits for its trace

A score attached to a trace the platform has never seen goes nowhere. Send scores
only for traces already marked exported.

### The client is passed in

`export_pending(db, client)` takes anything with `trace`, `score` and `flush`. The
tests pass a fake. Real use passes `LangfuseClient`, given in `langfuse_client.py` —
read it. It is forty lines, and your trace id goes straight through as Langfuse's, so
the id a user quotes finds the trace in both places.

### From a bad trace to a case

```python
to_case(trace, "Deleted the wrong note")
```

gives a **draft** eval case: the task, the tools it used, what it answered, and why
the user was unhappy. `expect` is empty. What *should* have happened is a judgement,
and it is yours. Write it, add the case to your Agent From Zero week 8 suite, and the
baseline gate stops this mistake coming back.

---

## Exercises

```bash
pytest week-04/day-4 -v
```

Copy `tracestore.py` and `feedback.py`. Write `exporter.py`: `export_pending` and
`to_case`. `langfuse_client.py` is given.

Then, once, by hand: install `langfuse`, set your keys, and export a real trace.

---

## Predict-then-run

Export three traces with your Langfuse keys deliberately wrong. Predict what your
database says afterwards. Then fix the keys and run it again.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight.
