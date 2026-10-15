# Day 2 — Someone else's server

> **By the end of today** you can say what you would be trusting before you connect
> an MCP server, refuse any tool you have not read, and notice when one you approved
> has changed.

---

## Read first

- [ ] MCP — [Security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) · 20 min
- [ ] Simon Willison — [The lethal trifecta for AI agents](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · 10 min

---

## What you need to know

### A description is a prompt

The model reads every tool's description to decide what to call. Whoever writes the
description writes part of your prompt. `other_servers.py` has a calendar whose
second version tells the model to delete your notes — in the description of a tool
called `today`.

### Approve, then pin

A person reads each tool once and says yes. Store its **fingerprint** — a hash of
its name, description and schema — not just its name. Next time the server lists its
tools, anything new is "not approved" and anything different is "changed since it
was approved". Neither reaches the model until a person reads it again.

### Name it so it cannot pretend

A remote tool called `delete_note` must never be confused with Desk's own. Prefix
every remote tool with its server's name, and say in the description where it came
from.

### Results are data

A remote tool's result goes into the same context as everything else. Label it as
data, cut it to a sane length, and remember that a label is a hint to the model,
not a wall.

### The combination to avoid

Private data, untrusted content and a way to send things out, in one agent. Desk has
the first. A web-fetching server adds the second. Write down which one you would be
adding before you connect anything.

---

## Exercises

```bash
pytest week-07/day-2 -v
```

Write `trust.py`. Then pick a real, public MCP server you might connect, read its
tools, and write `REVIEW.md`.

---

## Predict-then-run

List `calendar_server(2)`'s tools with a `Client` and run `review` against your pins
from version 1. Predict the result before you run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
