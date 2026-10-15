# Day 2 — The production review

> **By the end of today** you have reviewed Desk as if someone else had built it and
> you had to sign it off — and you know what you would fix first.

---

## Read first

- [ ] Your attack suite's last run, your alerts' history, and your incident write-up
- [ ] Simon Willison — [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), again, with Desk in mind · 10 min

---

## What you need to know

### Threat model: assets, attackers, ways in

What is worth protecting (each user's notes, your money), who wants it (another user,
someone with a stolen key, text inside a note), and how they get in. For each way in,
the defence you built — and the test or measurement that shows it works.

### Failure modes: what breaks, and what happens then

The provider, the disk, the deploy, the worker, the alerts themselves. For each one:
what users see, how you find out, and how long until it is fixed. Use your incident.

### What still gets through

The section the reviewer reads first. A review that finds nothing is a review nobody
believes. Your attack rate on fifteen runs, the model you never attacked, the limit
you never set.

### What I would fix first

One thing, and why that one. Not a list.

---

## Exercises

```bash
pytest week-08/day-2 -v
```

Write `PRODUCTION_REVIEW.md`. Then ask the editor to **red-team this**.

---

## Before you close the laptop

Commit, push, fill in the signal log.
