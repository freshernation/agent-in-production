# Day 3 — What the user thought

> **By the end of today** a user can rate an answer, the rating is tied to the exact
> trace it is about, and you can list everything rated bad.

---

## Read first

- [ ] Langfuse — [Scores via SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk) · 10 min

---

## What you need to know

### A rating is only useful attached to something

*"Users gave 70% thumbs up this week"* tells you almost nothing. *"This trace got a
thumbs down, with the comment 'deleted the wrong note'"* tells you where to look.
So a rating is stored against a **trace id**, and that is why every reply carries one.

### Up or down

`1` or `-1`. A five-star scale gives you numbers people use differently; a thumbs
gives you a decision. Anything else is refused.

### Only your own answers

Bob cannot rate Alice's trace, and gets the same reply as for a trace that does not
exist: *"No such trace."* Week 1's rule, applied to a new table.

### Changing your mind

Rating the same trace again replaces the rating and marks it for sending again. The
platform should hold the latest opinion, not the first.

### Bad traces are the list to work from

`bad_traces` is every trace rated down, newest first. It is the input to tomorrow's
second half: turning one into an eval case.

---

## Exercises

```bash
pytest week-04/day-3 -v
```

Copy `tracestore.py` here. Write `feedback.py`: `SCHEMA`, `create_tables`, `rate`,
`summary` and `bad_traces`.

---

## Predict-then-run

Use Desk for ten real requests and rate each one honestly. Predict how many you will
rate down before you start.

---

## Before you close the laptop

Commit, push, fill in the signal log.
