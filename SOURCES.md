# Sources

Chosen by the librarian rule: an official source for how the thing works, an
engineering account from people who run it for why, and nothing that is a vendor
selling the answer without saying so. Three or four a week, not ten.

Need something that is not here? `ai/librarian.md`.

---

## The ones worth reading twice

| Read | Why |
|---|---|
| [FastAPI — Tutorial](https://fastapi.tiangolo.com/tutorial/) | The framework's own walk-through, and unusually good |
| [Stripe — Idempotency](https://stripe.com/blog/idempotency) | Why "run it twice, harmlessly" matters for anything that sends or charges |
| [Google SRE book — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/) | What to watch, and what never to page anybody about |

---

## Week 1 — Behind an API

| Read | Why |
|---|---|
| [Python — Classes](https://docs.python.org/3/tutorial/classes.html) | The catch-up |
| [FastAPI — Python types intro](https://fastapi.tiangolo.com/python-types/) | Why the type hints are not decoration |
| [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) | How the key check is written once |
| [MDN — HTTP status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) | The reference |

**Ignore for now:** authentication libraries, OAuth, JWTs.

## Week 2 — State that survives

| Read | Why |
|---|---|
| [Python — `sqlite3`](https://docs.python.org/3/library/sqlite3.html) | Placeholders, connections, transactions |
| [SQLite — Transactions](https://www.sqlite.org/lang_transaction.html) | What `BEGIN`, `COMMIT` and `IMMEDIATE` promise |
| [OWASP — Broken access control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) | The most common way one user sees another's data |

**Ignore for now:** ORMs, indexes and query tuning.

## Week 3 — Work that outlives a request

| Read | Why |
|---|---|
| [Python — Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html) | `gather` and `to_thread` |
| [FastAPI — Concurrency and async](https://fastapi.tiangolo.com/async/) | When a route should be `async def`, and when not |
| [Brandur Leach — Transactionally staged job drains](https://brandur.org/job-drain) | A queue on a database table, at scale |
| [Stripe — Idempotency](https://stripe.com/blog/idempotency) | The other half of retries |

**Ignore for now:** Celery, Redis, message brokers.

## Weeks 4 to 8

Chosen when each week is published. Hosting, tracing and MCP change too often to pick
them in advance.
