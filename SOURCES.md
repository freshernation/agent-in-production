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

## Week 4 — See inside it

| Read | Why |
|---|---|
| [Langfuse — Observability overview](https://langfuse.com/docs/observability/overview) | What a trace, a span and a generation are |
| [Langfuse — Python SDK instrumentation](https://langfuse.com/docs/observability/sdk/python/instrumentation) | What `langfuse_client.py` does, call by call |
| [Google SRE book — Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/) | Why the failures are the records that matter |

**Ignore for now:** OpenTelemetry directly, sampling, dashboards.

## Week 5 — Ship it on every push

| Read | Why |
|---|---|
| [Docker — Dockerfile best practices](https://docs.docker.com/build/building/best-practices/) | The build cache, and not running as root |
| [GitHub — Quickstart for Actions](https://docs.github.com/en/actions/get-started/quickstart) | Where a workflow lives and how to read a run |
| [The Twelve-Factor App — Config](https://12factor.net/config) | Why every difference is a setting |
| [Google SRE book — Release engineering](https://sre.google/sre-book/release-engineering/) | What a release process is for |

**Ignore for now:** Kubernetes, Terraform, canary deploys.

## Week 6 — Keep it up

| Read | Why |
|---|---|
| [Google SRE workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/) | What makes an alert worth waking for |
| [Martin Fowler — CircuitBreaker](https://martinfowler.com/bliki/CircuitBreaker.html) | Stop calling what is broken |
| [Claude — Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | The prefix rule, the minimum length, the prices |
| [Google SRE book — Postmortem culture](https://sre.google/sre-book/postmortem-culture/) | How to write an incident without blame |

**Ignore for now:** Prometheus, Grafana, on-call tooling, Redis.

## Week 7 — Connect it, and attack it

| Read | Why |
|---|---|
| [MCP — Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture) | Hosts, clients, servers, and what crosses between them |
| [MCP Python SDK — Get started](https://py.sdk.modelcontextprotocol.io/get-started/) | The server and client you write, in the SDK's own words |
| [MCP — Security best practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) | What a server can do to you |
| [Simon Willison — The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) | The combination of tools to avoid |
| [W3C — Trace Context](https://www.w3.org/TR/trace-context/) | The one header that joins two traces |

**Ignore for now:** MCP over HTTP with OAuth, MCP registries, red-teaming tools.

## Week 8 — The production review

No new reading. Reread what you would cite in your own review.
