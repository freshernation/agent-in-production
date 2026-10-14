# Week 3 Milestone — Background tasks, and fair shares

> Desk accepts a slow task at once and finishes it in a worker process that can be
> killed and restarted, and every user has their own limit.

---

## The files

| File | Where it comes from |
|---|---|
| `store.py`, `migrate.py`, `tenancy.py`, `permissions.py` | **copy from your week 2 milestone** |
| `jobs.py`, `worker.py`, `limits.py` | **copy from this week's days** |
| `app.py` | your week 2 milestone, extended |
| `run_worker.py` | given: the worker process |

## `app.py`

| Name | What it does |
|---|---|
| `STALE_AFTER` | `300` — seconds before a running job is presumed abandoned |
| `take_turn(model, db, roles, user, message, conversation_id, history)` | runs the agent, saves the history, returns the answer — **raises** if the run stopped with `error` |
| `create_app(model, keys, roles, db_path, limiter, clock=time.time)` | the service |
| `work_once(model, roles, db_path, worker, now)` | one pass of the worker |

The routes:

| Route | What it does |
|---|---|
| `GET /health` | open |
| `POST /chat` | as week 2, through `take_turn`; 503 if the model is down |
| `POST /tasks` | queues a `chat` job and answers **202** at once with `task_id` |
| `GET /tasks/{task_id}` | its status and result — 404 for somebody else's |
| `GET /conversations` | as week 2 |

Every route that needs a key is also rate-limited per user: **429** with
`Retry-After`.

Why `take_turn` raises on `error`: when the model cannot be reached, Desk's answer
contains the error text. Returned, it would become a "done" task showing internal
detail to the user. Raised, the worker retries it, and after three tries the user
sees *"The task could not be completed."*

## Run it

Add a `from_environment()` as in week 1 — `DESK_KEYS`, `DESK_ROLES`, and `DESK_DB`
for the database path, which the worker reads too. It is not tested; it is how you
run the thing. Then, in two terminals:

```bash
uvicorn app:from_environment --factory
python3 run_worker.py
```

---

## Check it

```bash
pytest week-03/milestone -v
```

## Friday

Your instructor kills the worker in the middle of a task.
