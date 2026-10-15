# Week 6 — Friday defence

Forty minutes. **It is live.** You switch things off; they keep Desk up.

---

## Phase 0 — Break it (8 min)

Ask them to do each of these on their live service, through its settings, while you
watch their phone and their URL:

1. Set the primary provider's key to a revoked one. Send a question. **It must still
   be answered** — by the fallback.
2. Revoke the fallback's key too. Send a question. The answer must be the honest down
   message, and **within the alert window the alert must reach their phone.**
3. Put both keys back. The next alert check must resolve it.

If the alert never arrives, that is the defence.

## Phase 1 — Explain (10 min)

1. *"Read me your three thresholds. Why those numbers?"* "It seemed right" is a 1.
   "One failure in twenty is when a user notices" is a 5.
2. *"Why `min_requests`?"* — one failure in two requests at 3am is 50%.
3. *"Your breaker is open. What happens to the next request, and the one sixty
   seconds later?"*
4. *"Which answers do you not cache, and why?"* — tool answers, failures, and
   anything for anyone but the person who asked.
5. *"Your budget check is before the turn. How far over can a user go?"* — one turn,
   at most the token budget priced as output. They should know the number.

## Phase 2 — The incident (10 min)

Read `INCIDENT.md` aloud. Ask:

- *"Is there a person's name in it?"* There should not be. Blameless means about
  the system.
- *"What would have found it faster?"*
- *"What did you change, and how do you know it worked?"* The only good answer is
  a repeat of the break.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `firing` uses `>=` | Alerts on the line itself. Fires when error rate is exactly 5% |
| Medium | the breaker never goes half-open | A recovered provider is never tried again |
| Medium | `cache_key` without the user | Bob gets Alice's answer. Ask what was leaked |
| Nasty | the cache stores answers that used a tool | Right on Monday, wrong on Tuesday, and nothing errors |

The **Nasty** one: a stale cached answer looks exactly like a correct one.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Break it** | Fallback answers, alert arrives, resolves | Two of the three | Desk goes down and nobody knows |
| **Explain** | Every threshold has a reason | Knows what each does | Cannot say why a number |
| **Incident** | Blameless, timed, and the fix was re-tested | Clear but not re-tested | A story with no timeline |
| **Debug** | Suspects the cache | Finds it | Guesses |

---

## Instructor: framing week 7

> **Next week Desk talks to things it did not write.** Its tools go behind an MCP
> server, it uses someone else's, and then you attack it — the live one — and measure
> how often the attack works.
