# Day 4 — Deploy what passed, and know the way back

> **By the end of today** only a passing push to `main` is deployed, the deploy is
> checked from the outside, and you know which release to go back to.

---

## Read first

- [ ] Google SRE book — [Release engineering](https://sre.google/sre-book/release-engineering/) · 20 min

---

## What you need to know

### The gate is a condition

```
deploy only if   every check passed   and   this is a push to main
```

In the workflow that is `needs: checks` and an `if`. Without `needs`, the deploy job
runs at the same time as the checks and does not care how they end.

### Check what is live, from the outside

The host says the deploy succeeded. That means it started *something*. So after every
deploy, `check_live.py` asks the live URL two questions: is `/health` reporting the
version I just deployed, and does `/chat` refuse a request with no key? A release that
serves the old version, or opens the door, failed — whatever the host says.

### Know what is live, and what was last good

A history of releases — deployed, healthy, failed, rolled back — answers the only two
questions that matter during an incident: what is running, and what to go back to.

### Roll back the code, not the data

Going back to the previous release is fast. Going back on the database is not. So a
change to the database must never break the release before it: add a column in one
release, start using it in the next, remove the old one after that.

---

## Exercises

```bash
pytest week-05/day-4 -v
```

Write `release.py`: `should_deploy`, `record`, `current`, `rollback_target` and
`verify_release`.

---

## Predict-then-run

Deploy, then roll back on purpose. Predict how long it takes before you start a timer.

---

## Before you close the laptop

Commit, push, fill in the signal log. Read the milestone tonight — and deploy
something, anything, before Friday.
