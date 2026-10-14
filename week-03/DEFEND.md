# Week 3 — Friday defence

Forty minutes. The student runs the server and `run_worker.py` side by side.

---

## Phase 0 — Kill the worker (3 min)

Submit a task. Kill the worker with Ctrl+C before it finishes. Start it again. The
task must finish, once.

## Phase 1 — Explain (10 min)

1. *"An `async def` route calls `time.sleep(5)`. What happens to every other request?"*
2. *"Two workers call `claim` at the same instant. Walk me through why they get
   different jobs."* — `BEGIN IMMEDIATE` takes the write lock first.
3. *"A worker finishes the work and dies before calling `finish`. What happens next,
   and why does that make `once` necessary?"*
4. *"Why does a job with no handler die at once, but one that raised gets retried?"*
5. *"Alice sends a hundred requests a second. What does Bob notice?"* — nothing.

## Phase 2 — Mutate (12 min)

- **A** — *"Add a `share` job kind that calls `share_note`."* Before typing: where
  does `once` go, and what is the key?
- **B** — *"A task should be cancellable."* Discussion first: which status, and what
  if the worker already has it?
- **C** — *"Raise the limit for one user."* Where does the number live?

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `claim` uses plain `BEGIN` | Passes alone. The six-thread test sometimes catches it. Do they know why only sometimes? |
| Medium | `requeue_stale` also resets `attempts` | A job that crashes its worker every time is retried for ever |
| Medium | the bucket refills without the `min` | An idle hour buys a burst of a thousand |
| Nasty | `take_turn` returns the answer when the run stopped with `error` | The task shows "done", with the model's error text, to the user |

The **Nasty** one is the week's theme: success is a status you have to earn, not the
default when nothing raised.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Kill** | Finishes once | Finishes twice | Lost |
| **Explain** | Explains the lock, not just the keyword | Knows it is atomic | Believes the check and the update can be separate |
| **Mutate** | Puts the side effect behind `once` unprompted | Builds it | Sends twice on a retry |
| **Debug** | Says why the race test is flaky | Finds it | Guesses |
