# Day 2 — Traces you can search

> **By the end of today** you can answer, in one query each, the questions every
> incident starts with.

---

## Read first

- [ ] SQLite — [Aggregate functions](https://www.sqlite.org/lang_aggfunc.html) · 10 min

---

## What you need to know

### The questions come first

Somebody will ask you, eventually:

| Question | Query |
|---|---|
| What did Alice's request at 3pm do? | her traces in a time window |
| What happened in this conversation? | one session's traces |
| Who is costing us the most? | cost by user |
| What is slow? | the slowest traces |
| How often is it failing? | the error rate in a window |

Design the table for those, and only those.

### Pull out what you search by

```
id | user | session | started | duration | cost | tokens | error | body
```

The columns you filter and sort on get their own column. Everything else stays in
`body` as JSON. You will never search by the arguments of the third tool call, so it
does not need a column.

### A window includes its start, not its end

`start <= started < end`. Then 2pm–3pm and 3pm–4pm never both count the request at
exactly 3pm.

### `exported`

Every trace starts at 0. On Thursday a background process sends the unexported ones
to the platform and sets 1. If the platform is down, nothing is lost: they are still
0, and go next time.

---

## Exercises

```bash
pytest week-04/day-2 -v
```

Write `tracestore.py`: `SCHEMA`, `create_tables`, `save`, `get`, and the five
questions.

---

## Predict-then-run

Make twenty real requests with a mix of short and long conversations. Predict which
user `costs_by_user` will put first, then run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
