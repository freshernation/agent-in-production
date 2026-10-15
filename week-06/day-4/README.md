# Day 4 — A budget, and an incident

> **By the end of today** no user can spend more than a set amount a day, you have
> broken your live service on purpose, and you have written up what happened.

---

## Read first

- [ ] Google SRE — [Postmortem Culture: Learning from Failure](https://sre.google/sre-book/postmortem-culture/) · 20 min
- [ ] Claude — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) · 5 min

---

## What you need to know

### Why a budget per user

The rate limit from week 3 caps requests. It does not cap money: twenty requests a
minute that each read a long conversation cost far more than twenty short ones. A
daily budget per user, read from the trace store you already have, caps what any one
person — or one stolen key — can cost you.

### It resets at midnight UTC

Pick one clock and say it in the message. "Tomorrow" in whose time zone is a support
ticket.

### Checked before the turn, so it can go over

The check runs before the model is called, because after is too late to refuse. So
one turn can go past the limit. By how much? At most Desk's token budget priced as
output. Know that number, and set the budget with it in mind.

### Break it on purpose

Pick one, on your live service, on a quiet afternoon:

- set the model key to a revoked one
- set `DAILY_BUDGET` to `0.01` and use it up
- send requests in a loop until the rate limit and the alert both fire

Watch what happens from the outside: what users see, when the alert arrives, what
the traces say. Then put it back.

### Write it up blameless

`INCIDENT.md` is about what happened and why the system let it, not who did it. A
timeline with times. What users saw, in their words. How you found out — and whether
the alert beat the first complaint. What you changed, and how you know it worked.

---

## Exercises

```bash
pytest week-06/day-4 -v
```

Copy `tracestore.py`, write `budget.py`, then break the live service and write
`INCIDENT.md`.

---

## Predict-then-run

Before you break it: write down when you expect the alert to arrive. After: how far
off were you, and why?

---

## Before you close the laptop

Commit, push, fill in the signal log.
