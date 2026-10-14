# Day 3 — Many users

> **By the end of today** each user's agent works on their own notes and nobody
> else's, and their conversations are stored.

---

## Read first

- [ ] OWASP — [Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) · 15 min

---

## What you need to know

### The tools still have Desk's names

The model's schemas say `add_note(title, body)`. Today's functions need
`add_note(db, user, title, body)`. You do not change the schemas. You **bind** the
first two arguments:

```python
def bound(function, db, user):
    def run(**args):
        return function(db, user, **args)
    return run
```

It is Agent From Zero week 8's `watched`, doing a different job: a function that
builds a function with something remembered inside it.

### The user comes from the key, never from the model

```python
tools = tools_for(db, user)      # user from the key
```

None of the schemas has a `user` argument. So there is nothing the model can write —
however it was persuaded — that reaches another user's notes. If it invents one, the
call fails with an error sentence. **The thing that decides whose data is touched is
never anything the model produced.**

This is the most important line of the week. Systems get it wrong by putting
`user_id` in a tool's schema "so the model can be helpful".

### Conversations go in the database

`save_history` stores the message list as JSON. Two details:

- **Drop keys starting with `_`** first. Since Agent From Zero they have held a
  provider's private data, which is not yours to store.
- **Saving again replaces it**: `INSERT ... ON CONFLICT (user, id) DO UPDATE`.

And `load_history` for another user's id returns `None`, exactly like an id that does
not exist.

---

## Exercises

```bash
pytest week-02/day-3 -v
```

Copy `store.py` and `migrate.py` here. Write `tenancy.py`: `bound`, `tools_for`,
`clean`, `save_history`, `load_history`, `conversation_ids`.

---

## Predict-then-run

Look at the test where the model asks to delete `"bank"` with `"user": "alice"` in its
arguments, run by Bob. Predict the tool result the model sees before you run it.

---

## Before you close the laptop

Commit, push, fill in the signal log.
