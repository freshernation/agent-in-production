# Week 4 — Friday defence

Forty minutes. The student runs the server, the worker and the exporter, and has
Langfuse open.

---

## Phase 0 — Find it (5 min)

Make three requests as two users. Then: *"Alice says the second answer was wrong.
Find it."* — in their database, then on the platform. Under a minute each.

## Phase 1 — Explain (10 min)

1. *"Your `Recorder` stands in for the model. How does `run_agent` not notice?"*
2. *"A request failed. Is there a trace? Why does that matter more than the ones
   that worked?"*
3. *"Bob rates Alice's trace. What happens, and what does Bob learn?"*
4. *"Langfuse is down for an hour. What is lost?"* — nothing; traces stay unexported.
5. *"Why does a score wait for its trace to be exported?"*

## Phase 2 — Mutate (12 min)

- **A** — *"Add the model name to every generation span."* Where does it come from?
- **B** — *"A user asks to have everything about them deleted."* Discussion: which
  tables, and the platform too. Looking for: they know where their data is.
- **C** — *"Turn the last bad trace into a case and write its expectation."* Live.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | the trace is saved only when the run succeeds | The failures vanish. Which test? |
| Medium | `export_pending` marks traces exported before calling the client | One outage, and those traces never arrive |
| Medium | `rate` returns "Not your trace." for Bob | Now Bob knows the trace exists |
| Nasty | `record_tools` defines the wrapper inside the loop | Every tool span is named after the last tool. Nothing crashes |

The **Nasty** one is week 8 of Agent From Zero, coming back: the closure trap, in a
place where the only symptom is a misleading record.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Find it** | Under a minute, both places | Finds it slowly | Cannot find it |
| **Explain** | Explains why failures must be traced | Knows they are | Thinks only successes matter |
| **Mutate** | Knows every place a user's data lives | Finds most | Forgets the platform |
| **Debug** | Explains why the bug hides | Finds it | Guesses |
