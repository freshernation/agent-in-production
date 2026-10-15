# Day 1 — The architecture document

> **By the end of today** someone who joins tomorrow could change Desk without you,
> starting from one page.

---

## Read first

- [ ] Your own `DEPLOYMENT.md`, `RUNBOOK.md` and `ATTACKS.md`, end to end
- [ ] Paste `ai/advisor.md` into a fresh chat and use its **week 8** section to plan
      this week's review · 20 min

---

## What you need to know

### Who it is for

Not your instructor. The person who has to change Desk next month, at 5pm, without
asking you. They need to know what runs where, what talks to what, and which choices
were deliberate — so that they do not undo one by accident.

### The picture first

Every process, every store, every outside service, and the arrows between them. Plain
text in a code block is fine; Mermaid is fine. If something runs in production and is
not in the picture, the picture is wrong.

### Decisions, with the road not taken

"SQLite in WAL mode" is a fact. "SQLite in WAL mode, not Postgres, because two
processes on one disk is all Desk needs, and the day it needs a second machine it
needs Postgres" is a decision. Three at least: what you chose, what you did not, why,
and when you would change your mind.

### What was cut

The things you deliberately did not build. Writing them down stops the next person
from adding them on a whim, and stops you from being asked why they are missing.

---

## Exercises

```bash
pytest week-08/day-1 -v
```

Write `ARCHITECTURE.md`. Then give it to the editor (`ai/editor.md`).

---

## Before you close the laptop

Commit, push, fill in the signal log.
