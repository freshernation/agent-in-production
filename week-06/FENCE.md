# Week 6 — Concept fence

## Allowed

**Everything from weeks 1 to 5**, plus:

- Percentiles by nearest rank
- A circuit breaker: closed, open, half-open
- `hashlib.sha256`
- `copy.deepcopy`
- Claude's `cache_control` on a system prompt, and the usage fields that report it
- An incoming webhook: one `httpx.post` with JSON
- `float` settings with a lower bound in Pydantic

## Not yet

A metrics system (Prometheus, Grafana, Datadog) · on-call rotations and escalation ·
Redis or any shared cache · cost forecasting · load-testing tools · SLO burn rates ·
MCP and attacks (week 7)

---

## Why no metrics system

Every number this week's alerts need is already in your trace store: when each
request started, how long it took, whether it failed and what it cost. A query over
that table is a metrics system with one user. Adding Prometheus would be another
service to deploy and keep up — the opposite of this week's point. When you have
more than one service to watch, that changes.
