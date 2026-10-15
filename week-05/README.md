# Week 5 — Ship it on every push

> **Destination**
> A push to `main` is tested, deployed and checked from the outside, with no hands on
> the server — and a push that fails its checks never reaches anyone.

**Project 1.** By Friday Desk has a public URL, and every change after this one
reaches it the same way: through the pipeline.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Package Desk and its worker as containers that share one database |
| Tue | `day-2/` | Run every check with one command, on every push, in CI |
| Wed | `day-3/` | Take everything that differs between your laptop and the server from the environment |
| Thu | `day-4/` | Deploy only what passed, confirm it is the release you meant, and go back fast |
| Fri | `milestone/` | **Project 1** — deployed from CI, with a live URL |

---

## The rule from this week on

**Nothing reaches the live service except through the pipeline.** No copying files to
the server, no editing in place, no "just this once". A change that did not go through
the checks is a change nobody checked.

---

## SQLite in production, and when it stops being enough

The service and the worker run as two containers sharing one volume, and SQLite in
WAL mode handles two processes on one disk well. What it cannot do is two machines.
The day Desk needs a second API instance, it needs Postgres — and Monday's
`database.py` shows exactly what that port involves. It is this week's deep track.

---

## Before Monday

Docker running on your laptop, and an account on the host your instructor named.
See `SETUP.md`.

---

## Outside-view question

> *A pharmaceutical batch cannot leave the factory until a person who did not make it
> signs it off. What would that person check for your code?*
