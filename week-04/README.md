# Week 4 — See inside it

> **Destination**
> Any request from yesterday can be found in under a minute — what was asked, what the
> model did, what it cost, how the user rated it — and a bad one becomes an eval case.

Desk is running for several people now, in two processes. When somebody says "it got
it wrong", you have nothing to look at. This week every request leaves a record.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Record every model call and tool call in a request, with its time and cost |
| Tue | `day-2/` | Store traces so you can answer the questions an incident asks |
| Wed | `day-3/` | Let users rate an answer, tied to the trace it came from |
| Thu | `day-4/` | Send it all to a tracing platform, and turn a bad trace into an eval case |
| Fri | `milestone/` | Ship a Desk where every request is traced, costed and rateable |

---

## By hand first, then the platform

You write the recorder and the store yourself, on SQLite. Then a given adapter of
forty lines sends the same records to Langfuse. When you open its dashboard on Friday
it will look like a nicer version of the table you queried on Tuesday — which is the
point.

From this week you need a **model key** and a **free Langfuse account**. See
`SETUP.md`.

---

## Outside-view question

> *Why does every airliner carry a recorder that nobody reads unless something goes wrong?*
