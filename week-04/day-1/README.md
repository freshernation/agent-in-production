# Day 1 — A record of every request

> **By the end of today** every model call and tool call in a request is recorded, with
> when it started, how long it took, and what it cost.

---

## Read first

- [ ] Langfuse — [Observability overview](https://langfuse.com/docs/observability/overview) · 15 min
- [ ] Google SRE book — [Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/), the first half · 20 min

---

## What you need to know

### You already wrote a trace

Agent From Zero's `run_agent` keeps `run["trace"]`: calls, results, answers. It has
no timings and no per-call cost, and it lives in memory for one request. Today's
record fixes all three.

### Something that stands in for the model

```python
recorder = Recorder(model, clock)
run_agent(recorder, task, schemas, tools)
```

`run_agent` calls `recorder.chat(...)` exactly as it called `model.chat(...)`. The
recorder calls the real model, writes down what happened, and hands the reply back
unchanged. The loop never knows. This is the same move as the fake model in your
tests, the other way round: a class with the same method, doing something extra.

### Spans

Each model call is a **generation**; each tool call is a **tool** span. Both have a
start and an end. Put together, they show where the time went:

```
generation   0.0 – 1.8s   1,200 in / 40 out
tool         1.8 – 1.9s   list_titles
generation   1.9 – 3.4s   1,400 in / 25 out
```

*"Desk is slow"* becomes *"the second model call is 1.5 seconds of a 3.4-second
request"*.

### Cost

Tokens times price, per million, input and output priced separately:

```python
cost = (input * price["input"] + output * price["output"]) / 1_000_000
```

Output costs several times input. A trace shows which requests are expensive, and
nearly always it is because the history is long, not because the answer is.

### Record the failures

If the model raises, the recorder writes a span with the error, then re-raises. The
requests that failed are the ones you will be asked about.

---

## Exercises

```bash
pytest week-04/day-1 -v
```

Write `recorder.py`: `Recorder`, `recorded`, `record_tools`, `cost` and `build_trace`.

---

## Predict-then-run

Run one real request through a `Recorder` and print the spans. Predict which span is
longest before you look.

---

## Before you close the laptop

Commit, push, fill in the signal log.
