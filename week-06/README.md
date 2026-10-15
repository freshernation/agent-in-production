# Week 6 — Keep it up

> **Destination**
> When Desk breaks, you hear about it before your users write in, and when the model
> provider goes down, Desk still answers — or says plainly that it cannot.

Desk has been live since last Friday. This week is about the second day of a
service's life: the one where things go wrong without you touching anything.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Choose what to alert on, with thresholds decided in advance, and not cry wolf |
| Tue | `day-2/` | Fall back to a second provider when the first is down, and stop hammering a dead one |
| Wed | `day-3/` | Use the provider's prompt cache, and keep your own answer cache from leaking |
| Thu | `day-4/` | Cap what one user can spend in a day, break the service on purpose, write it up |
| Fri | `milestone/` | Desk with alerts, a fallback, a cache and a budget — defended live |

---

## The rule from this week on

**Decide the threshold before you look at the graph.** An alert you tune after the
fact fits last week's noise and misses next week's outage. Write the number down,
say why, and change it only with a reason you could defend.

---

## One deliberate overload

On Thursday you break your own live service on purpose: a revoked key, a budget of
one cent, or a loop of requests. Your alert should fire, your runbook should say what
to do, and your write-up should say what happened. Doing this once, on purpose, on a
quiet afternoon, is the cheapest way to find out whether any of it works.

---

## Before Monday

A second provider's key — an OpenAI key if your primary is Claude, or the other way
round — for Tuesday. And an incoming webhook (a Slack workspace of your own is
enough) so alerts reach your phone.

---

## Outside-view question

> *A triage nurse sees forty patients a shift and sends three to a doctor at once. An
> alarm that sounds for every patient is one nobody hears. What would your service's
> triage nurse look at first, and what would they ignore?*
