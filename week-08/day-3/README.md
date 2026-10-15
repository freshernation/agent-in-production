# Day 3 — Cost against performance

> **By the end of today** you can say what Desk costs, how fast it is, which you
> traded for which, and what gives out first as it grows.

---

## Read first

- [ ] Claude — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing), again · 5 min
- [ ] Your week 4 trace store and your week 6 cache measurement

---

## What you need to know

### The numbers come from your traces

`numbers.py` reads the traces table and prints requests, error rate, median and 95th
percentile time, cost per request, tokens per request, cost per day, and the most one
user spent in a day. Run it on a copy of your production database. If production is
quiet, run it on a week of your own use, and say so.

### Trade-offs, named

Every choice you made traded something: a cheaper model for some quality, a cache for
some freshness, a budget for some users' convenience. Name the trade and what told
you it was worth it — an eval score, a measurement — or say that nothing did.

### The next bottleneck

As traffic grows, what gives out first: the money, the latency, SQLite's single
writer, the provider's rate limit? Say which, at roughly what traffic, and what you
would do.

---

## Exercises

```bash
python3 week-08/day-3/numbers.py path/to/desk.db
pytest week-08/day-3 -v
```

Write `COSTS.md`.

---

## Before you close the laptop

Commit, push, fill in the signal log.
