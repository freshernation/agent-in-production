# Week 1 — Behind an API

> **Destination**
> Somebody who is not you sends Desk a message over HTTP, with a key, and gets an
> answer — and somebody without a key gets nothing.

Desk runs in your terminal. One person, one conversation, one laptop. This week it
gets an address.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Read and write the Python FastAPI is written in: classes, type hints, decorators |
| Tue | `day-2/` | Build a small service, with requests checked before your code runs |
| Wed | `day-3/` | Put Desk behind `POST /chat`, and keep each conversation between requests |
| Thu | `day-4/` | Give every caller a key, and keep each person's conversations their own |
| Fri | `milestone/` | Ship it configured from the environment, and explain one request end to end |

---

## What changes

Everything you built ran when you ran it. From this week it runs when somebody else
asks, and four things follow from that:

| Problem | Answer this week |
|---|---|
| The input is not yours | a model that checks every request before your code sees it |
| The conversation has to live somewhere between requests | a store, keyed by conversation |
| Anybody on the internet can call it | a key per caller |
| One caller must not see another's conversation | conversations belong to the user who started them |

---

## Given to you

`desk/` is the hardened Desk from Agent From Zero, week 8 — your code, as a
package. `from desk.app import take_turn` runs one turn of it. `llm/` is the same
model layer as before.

---

## Outside-view question

> *A restaurant takes orders at the pass, not in the kitchen. What does the pass
> refuse, and who decided?*
