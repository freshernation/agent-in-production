# Day 3 — Two caches

> **By the end of today** you can mark Desk's system prompt for the provider's
> cache and price what it saves, and Desk serves a repeated question from its own
> cache — only to the person who asked it.

---

## Read first

- [ ] Claude — [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), up to "Pricing" and the section on minimum length · 20 min
- [ ] MDN — [HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching), the sections on private and shared caches · 10 min

---

## What you need to know

### The provider's cache

Every turn sends the same tools and the same system prompt before the conversation.
Mark the end of that prefix with `cache_control` and the provider keeps it: the next
request that starts with the same bytes reads it for a fraction of the price. On
Claude Sonnet 5.5 a cache read is a twentieth of the input price; a write costs a
quarter more than input. Read the table — the multipliers differ by model.

### It is a prefix match

Any byte that changes before the marker breaks it: a timestamp in the system prompt,
the user's name, tools in a different order. Desk's system prompt is fixed, which is
why it caches.

### It might not cache at all

Below a minimum length — 512 tokens on current Claude models — nothing is cached and
nothing tells you. Desk's tools and system prompt together may fall either side of that line.
The response's `cache_creation_input_tokens` and `cache_read_input_tokens` say what
happened. Measure before you claim a saving.

### Your own cache

Some questions repeat word for word: "what can you do?", "how do I share a note?".
Answering from memory costs nothing and takes no time. Three rules keep it honest:

1. **Key it by who asked.** A cache that does not know the user is a data leak with
   good latency.
2. **Never cache an answer that used a tool.** It depended on the notes at that
   moment.
3. **Let it expire.** An hour is plenty.

---

## Exercises

```bash
pytest week-06/day-3 -v
```

Write `caching.py`.

---

## Predict-then-run

Deep track, with a Claude key: send Desk's request twice with the system prompt
marked, using the `anthropic` SDK directly, and print `response.usage`. Predict both
cache fields for each request. If both are zero, work out why.

---

## Before you close the laptop

Commit, push, fill in the signal log.
