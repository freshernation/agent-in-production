# Week 2 Milestone — Desk for many users

> Desk on a database: each user's notes and conversations their own, each user's
> role enforced, and nothing lost when the server restarts.

---

## The files

| File | Where it comes from |
|---|---|
| `store.py`, `migrate.py`, `tenancy.py`, `permissions.py` | **copy from this week's days** |
| `app.py` | your week 1 milestone, rebuilt on the database |

## `app.py`

| Name | What it does |
|---|---|
| `parse_roles(text)` | `"alice:owner, bob:reader"` → `{"alice": "owner", "bob": "reader"}`; `ValueError` for a bad piece or an unknown role |
| `create_app(model, keys, roles, db_path)` | migrates the database, then serves `/health`, `/chat` and `/conversations` |

`ChatIn`, `ChatOut` and `user_for` come from week 1 unchanged.

`POST /chat` now:

1. loads the conversation with `load_history` for **this** user — `None` is a 404
2. runs the agent with `run_agent`: the role's schemas, the role's guarded tools
   bound to this user, Desk's `SYSTEM` and `DANGEROUS`, `approve=None`, the history,
   and `TOKEN_BUDGET`
3. saves `carry(history, result)`
4. replies with the answer — or a 503, never a traceback

**One connection per request.** Write a dependency that connects, `yield`s the
connection, and closes it. SQLite refuses to let a connection made in one thread be
used in another, and FastAPI runs each request in whichever thread is free.

**Anything dangerous is refused over HTTP.** `approve=None` means nobody is there to
say yes. That is deliberate.

---

## Check it

```bash
pytest week-02/milestone -v
```

Then run it, start a conversation, stop the server, start it, and carry on.

## Friday

The defence starts with the restart.
