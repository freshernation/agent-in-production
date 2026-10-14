# Week 2 — Friday defence

Forty minutes. The student runs `milestone/app.py` on a database file.

---

## Phase 0 — The restart (3 min)

Start a conversation. **Stop the server.** Start it again. Continue the conversation.
If it does not carry on, that is the defence.

## Phase 1 — Explain (10 min)

1. *"Show me a query in your code that does not say whose data it touches."* — there
   should be none.
2. *"Where does the user in `tools_for(db, user)` come from? Could the model change
   it?"* — from the key, and no: the schemas have no user argument.
3. *"Why catch the duplicate with the primary key instead of checking first?"*
4. *"A migration fails halfway. What state is the database in?"*
5. *"A reader's model asks for `delete_note`. Name the two things that stop it."* —
   it was never offered, and the guard refuses it anyway.

## Phase 2 — Mutate (12 min)

- **A** — *"Add a `pinned` column to notes."* Before typing: which file, and what
  must never happen to the migrations that already ran?
- **B** — *"Bob should be able to read Alice's shopping note, and nothing else of
  hers."* Discussion. Looking for: sharing is a new table and a deliberate rule, not
  removing `WHERE user = ?`.
- **C** — *"Make a new role, `editor`, that can add and delete but never share."*

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | `find_notes` drops `WHERE user = ?` | Bob finds Alice's bank note. Which test? |
| Medium | one connection made in `create_app` and shared by every request | Works in a quick test; fails under real requests, in another thread |
| Medium | an existing migration edited instead of a new one added | Fresh databases are fine; Friday's database is not |
| Nasty | `allowed()` returns the role's set itself, not a copy | One request adds to it and every reader can delete from then on |

The **Nasty** one is shared mutable state, the bug week 2 is about, hiding in a
place nobody thinks of as state.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Restart** | Carries on | Carries on with a fix during the defence | Lost |
| **Explain** | Shows every query is scoped | Knows the rule | Finds an unscoped query |
| **Mutate** | Adds a migration, never edits one | Gets the column in | Edits the first migration |
| **Debug** | Explains why it hides in tests | Finds it | Guesses |
