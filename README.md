# Agent In Production

Eight weeks from "it works on my laptop" to "it is running, and I would know if it
stopped".

You wrote an AI agent by hand: the loop, its tools, a gate in front of anything
dangerous, memory, evals, and an attack suite. It runs in your terminal, for you.
This course runs it for other people — behind an API, on a database, with work in the
background, traced, deployed on every push, watched, connected to other tools, and
defended in a written review.

---

## Who this is for

You have finished **Agent From Zero**, or you can do what its final project asks:
build an agent with tools and evals, with no framework, and explain every line.

You do not need to know classes, SQL, Docker or `async`. Week 1 starts with the
first, and each of the others arrives in the week that needs it. Before week 1 you
run a short baseline interview so that you, and your instructor, know which of them
to watch.

---

## The rules

**1. The twenty-minute rule.** Stuck for twenty minutes: open the tutor. Still stuck:
bring it to the live hour. Log every stuck moment in `logs/stuck-log.md`.

**2. You may not commit a line you could not have written and cannot explain on
Friday.**

**3. Nothing counts until the tests pass and it is pushed.**

**4. From week 5, nothing reaches your live service except through the pipeline.**
No editing on the server.

---

## The eight weeks

| Week | | Milestone |
|---|---|---|
| 1 | Behind an API | Desk answers HTTP requests, with a key per caller |
| 2 | State that survives | Many users, each with their own notes and role, through a restart |
| 3 | Work that outlives a request | Background tasks, a worker that can die, a fair share for everyone |
| 4 | See inside it | Every request traced, costed and rated; a bad trace becomes an eval case |
| 5 | Ship it on every push | **Project 1** — deployed by CI, behind a gate that can say no |
| 6 | Keep it up | Alerts, a fallback when the model is down, a cache, an incident write-up |
| 7 | Connect it, and attack it | Desk's tools over MCP, and the attack suite against the live service |
| 8 | The production review | **Project 2** — a live system, a written review, and a defence |

Weeks 1 to 3 run entirely on your laptop with a fake model. A real model key is
needed from week 4, a tracing account from week 4, and a host from week 5.

---

## How a week works

| | |
|---|---|
| **Monday to Thursday** | One live hour, then the day's folder: read, build, make the tests pass |
| **Friday** | No new content. Ship the milestone, then defend it |

Each day folder has a `README.md`, the files to write, and a test file that fails until
you have written them. Run the day's tests with `pytest week-NN/day-N -v`.

---

## What is in the repo

| Path | What it is |
|---|---|
| `desk/` | Desk, the agent you wrote, as a package — given complete |
| `llm/` | The model layer: one way to talk to Claude, OpenAI or a fake |
| `week-01/` … | One folder per week |
| `ai/` | The AI roles. Read `ai/README.md` first |
| `logs/` | Your baseline, your stuck log and your signal log |
| `SETUP.md` | Day zero |
| `CUT_LIST.md` | What this course does not teach, and why |
| `SOURCES.md` | What to read, and what to ignore |

Start with `SETUP.md`.
