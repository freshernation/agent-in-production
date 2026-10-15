# Week 7 — Friday defence

Forty minutes. It starts in the Actions tab.

---

## Phase 0 — The gate (5 min)

Open their last run on `main`. The attack job ran, it used a secret, and the deploy
waited for it. Then read the attack job's log: the rate, per kind.

## Phase 1 — Explain (10 min)

1. *"Which of Desk's tools did you not serve over MCP, and why?"* — `delete_note`:
   nothing on the other side can approve it.
2. *"Your MCP server: who is the user, and how does it know?"* — whoever started it.
   Then: *"what changes if it runs on the internet?"*
3. *"What is a fingerprint protecting you from?"* — a description you approved,
   changed afterwards. Ask for the attack by name if they read about it.
4. *"A server sends a traceparent of all zeros. What do you do with it?"*
5. *"Your rate is 0.0 on fifteen runs. Is Desk safe?"* — fifteen runs is not proof;
   they should know a zero on fifteen still allows a real rate of several percent.

## Phase 2 — A tool you would refuse (10 min)

Read `REVIEW.md` aloud. Then argue the other side: *"my manager says we need it by
Friday."* Looking for the condition under which they would connect it — a separate
agent, no write tools, pinned — not a flat no.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `delete_note` served over MCP | Ask what approves it |
| Medium | `review` checks names only, not fingerprints | The changed description reaches the model |
| Medium | `passes` ignores unanswered attacks | Every attack 503s and the gate is green |
| Nasty | the attack job runs, but deploy `needs: checks` only | A leaking push ships while the attack job is still running |

The **Nasty** one: the gate exists and is ignored — the check is real, the
dependency is not.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Gate** | Runs on main, secret key, deploy waits | Runs, deploy does not wait | Not in CI |
| **Explain** | Knows what each defence stops and what it does not | Knows what each does | Recites |
| **Refusal** | Holds the line and names the condition | Holds the line | Gives in, or says "it depends" |
| **Debug** | Suspects the dependency | Finds it | Guesses |

---

## Instructor: framing week 8

> **Next week there is nothing new.** You write down what you built and why, review
> it as if someone else had built it, and on Friday you show it live to someone who
> will try to break it.
