# Week 1 — Friday defence

Forty minutes. The student shares `milestone/app.py` and `A_REQUEST.md`, and runs it
with `uvicorn app:from_environment --factory`.

---

## Phase 1 — Explain (10 min)

1. *"Walk me from the socket to the model and back."* — their `A_REQUEST.md`, out
   loud, without reading it.
2. *"An empty message never reaches your function. What stopped it, and who wrote
   that code?"* — the model did, and nobody.
3. *"Why 404 for Bob asking about Alice's conversation, and not 403?"*
4. *"Your key check uses `compare_digest`. What would `==` give away?"*
5. *"Restart the server now. What is lost?"* — every conversation. Then: *"why is
   that acceptable for one week?"*

## Phase 2 — Mutate (12 min)

- **A** — *"Add `DELETE /conversations/{id}`."* Before typing: who may call it, and
  what does Bob get for Alice's id?
- **B** — *"A user loses their key. What do you do, and what does it cost the other
  users?"* Discussion. Looking for: one key per user is what makes revoking one
  possible.
- **C** — *"Make the message limit 500 characters."* One line. Then ask what the
  caller sees, and who wrote that message.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | conversations keyed by id only, not `(user, id)` | Bob continues Alice's conversation. Which test catches it? |
| Medium | `user_for` returns at the first matching key | Every test passes. Do they know what timing would show? |
| Medium | the 503 handler returns `str(error)` | The caller sees a file path |
| Nasty | `parse_keys` skips a piece without a colon instead of refusing | A typo in the setting quietly drops a user's key, and the server starts happily |

The **Nasty** one: a service that starts with a broken configuration is worse than
one that refuses to start.

## Phase 4 — The request (8 min)

Read `A_REQUEST.md` together. Ask for one thing it gets wrong or leaves out.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Explain** | Traces the request and names what each layer refuses | Knows the order | Thinks their function sees every request |
| **Mutate** | Decides who may call it before writing it | Builds it | Leaves it open |
| **Debug** | Names the test that should catch it | Finds it | Guesses |
