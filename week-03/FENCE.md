# Week 3 — Concept fence

## Allowed

**Everything from weeks 1 and 2**, plus:

- `async def`, `await`, `asyncio.run`, `asyncio.gather`, `asyncio.sleep`,
  `asyncio.to_thread`
- `BEGIN IMMEDIATE`, and `cursor.lastrowid`, `cursor.rowcount`
- `threading.Thread`, in tests and in the worker
- Generators: `yield`
- `StreamingResponse`
- `math.ceil`
- A clock passed in as a function

## Not yet

A queue library (Celery, RQ, arq, Dramatiq) · Redis · Postgres · Docker · logging
and tracing · deploying anywhere · `async` database drivers

---

## Why no queue library

Read any of them and you will find a status, an atomic claim, a visibility timeout
and a retry count. You will have written all four by Wednesday. Name one library on
Friday, read its documentation for those four things, and you will understand it in
an hour.
