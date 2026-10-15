# Day 4 — Attack it as deployed

> **By the end of today** you can say, as a number, how often an attack on the
> deployed Desk does harm — and a deploy waits for that number.

---

## Read first

- [ ] OWASP — [LLM01: Prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) · 15 min
- [ ] If you took the agent course, reread its week 8 attack suite. Today's is its production twin

---

## What you need to know

### Production Desk is a different target

In the agent course the attacks went for `share_note`. Production Desk has no
`share_note`, and refuses every delete because nobody is there to approve it. So
the attacks change: talk it into writing notes, get a secret quoted in an answer,
reach another user's notes. If one of those cannot work by design, the attack should
still be in the suite — to prove it stays that way.

### Against the deployed configuration

The same `create_app`, the same system prompt, the same permissions and the same
model as production, on a throwaway database. Not the live URL: the attacks need to
plant notes, and nothing should be able to plant notes in a live user's account.

### Inject the world

`run_attack` takes three functions — seed, chat, titles — instead of a database and
an app. The tests give it a pretend Desk; `run_attacks.py` gives it the real one.
The same code counts both.

### Unanswered is not defended

An attack that got a 503 did no harm and proved nothing. A suite where every attack
503'd must fail, or a broken key passes your security gate.

### Run each one more than once

A model that resists an attack once may not resist it twice. Three repeats is a
minimum; a rate of zero on fifteen runs still allows a real rate of several percent.

---

## Exercises

```bash
pytest week-07/day-4 -v
```

Write `attacks.py`.

---

## Predict-then-run

With your real provider, in the milestone folder: `python3 run_attacks.py`. Write
down the rate you expect, per kind, first.

---

## Before you close the laptop

Commit, push, fill in the signal log.
