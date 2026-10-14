# Week 3 — Work that outlives a request

> **Destination**
> A slow task is accepted at once and done in the background, survives a worker that
> dies halfway, and runs only once — and no single caller can use up the service.

Every request so far waits for the agent to finish. Agents are slow: several model
calls, each seconds long. This week the slow part moves out of the request.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Tell blocking code from waiting code, and run waits at the same time |
| Tue | `day-2/` | Build a job queue on a database table that two workers can never both take a job from |
| Wed | `day-3/` | Run jobs in a worker that can die, retry what failed, and do side effects only once |
| Thu | `day-4/` | Give each caller a fair share, and send a reply as it is written |
| Fri | `milestone/` | Ship background tasks, a worker process, and per-user limits |

---

## By hand first

There are good queue libraries. You will build one on a table first, because every
one of them is doing what you will write on Tuesday: a status column, an atomic
claim, and a rule for what happens when a worker disappears. Once you have written
those three, the library is a convenience rather than a mystery.

---

## Outside-view question

> *A dry cleaner gives you a ticket and your shirt on Thursday. What does the ticket
> promise, and what happens if the shop burns down on Wednesday?*
