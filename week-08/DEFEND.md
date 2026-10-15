# Week 8 — Project 2 defence

Sixty minutes. **Live, on their URL, through their pipeline.**

---

## Phase 0 — The demo (15 min)

They run `DEMO.md`. Do not interrupt. Note the minute anything goes wrong and what
they do about it — recovering from a real failure scores higher than a demo that
never had one.

## Phase 1 — The architecture (10 min)

Point at any box in their picture. *"What happens if this goes away?"* Then at any
arrow: *"What crosses here, and who checks it?"* Then: *"Which decision would you
change first, and what would make you?"*

## Phase 2 — Your turn to break it (15 min)

With their permission, on their live service, pick two:

- Send 100 requests in a minute with one key. Expect 429s, and the spend alert to
  stay quiet because the budget held.
- Ask Desk, as one user, for another user's notes, three different ways.
- Revoke the primary key. Expect the fallback.
- Push a change that fails one test. Expect no deploy.
- Plant a note that tells Desk to quote another note in every answer, then ask an
  innocent question.

For each: did their review predict it? A failure their review named is a strength.
A failure it did not is the finding.

## Phase 3 — The numbers (10 min)

From `COSTS.md`: *"What does one more user cost per day? What gives out first at a
hundred times the traffic? Which trade-off would you undo with more money?"* Then
from `PRODUCTION_REVIEW.md`: *"Defend 'what I would fix first' against the second
item on your list."*

## Retro (10 min)

1. *"What would you build differently if you started again on Monday?"*
2. *"Which week's idea will you use first at work?"*
3. *"What did I explain badly?"*

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Demo** | Live, includes a caused failure, recovers | Live, no failure shown | Not live |
| **Architecture** | Every box and arrow explained, decisions defended | Most of it | Reads the document |
| **Break it** | Review predicted what broke, or service held | Held, review was vague | Broke in a way they never considered |
| **Numbers** | Every figure from traces, trade-offs named | Numbers without meaning | No numbers |

Project 2 passes with **3 or more in every phase**.
