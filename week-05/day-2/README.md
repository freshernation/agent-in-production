# Day 2 — Every check, on every push

> **By the end of today** one command runs every check and answers yes or no, and
> GitHub runs it on every push.

---

## Read first

- [ ] GitHub — [Quickstart for GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart) · 15 min
- [ ] GitHub — [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) · 10 min

---

## What you need to know

### One exit code

CI reads exactly one thing from your checks: whether the command exited 0. So
`checks.py` runs every check and turns them into one answer.

### Run all of them, even after one fails

Stopping at the first failure means one problem per push. Running everything means
the whole picture in one run.

### The smoke test

`smoke.py`, given in the milestone, starts the whole service in-process with a fake
model and checks three things: it is up, it refuses a stranger, it answers someone
with a key. No network, no key, no cost — so it can run on every push.

### Why not the evals?

Your evals mean something only against a real model, which costs money and needs a
key in CI. They join the checks in week 7, with the key held as a secret. Until then,
a green CI means "the code does what the tests say", not "the agent is good". Know
which one you are claiming.

### A workflow lives in `.github/workflows/`

Write `ci.yml` in the day folder so the tests can read it, then copy it to
`.github/workflows/ci.yml` at the top of your repository. Push, and open the Actions
tab.

---

## Exercises

```bash
pytest week-05/day-2 -v
```

Write `checks.py` and `ci.yml`.

---

## Predict-then-run

Push a change that breaks one test. Predict which step goes red and what the summary
line says. Then fix it and push again.

---

## Before you close the laptop

Commit, push, fill in the signal log.
