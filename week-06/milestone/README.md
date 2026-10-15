# Week 6 Milestone — Desk stays up

> An alert reaches your phone for a failure you caused, and Desk still answers with
> the primary model switched off.

---

## The files

| File | Where it comes from |
|---|---|
| everything from your week 5 milestone | **copy** |
| `alerts.py`, `fallback.py`, `caching.py`, `budget.py` | **copy from this week's days** |
| `config.py` | week 5's, with `FALLBACK_PROVIDER` and `DAILY_BUDGET` |
| `compose.yaml` | week 5's, with the new settings and an `alerts` service |
| `app.py` | your week 5 milestone, kept up |
| `run_alerts.py` | given |
| `INCIDENT.md` | **copy from day 4** — the incident on your live service |
| `RUNBOOK.md` | new |

## `app.py`

| Change | What it means |
|---|---|
| `create_app(..., cache=None, daily_budget=None)` | both off unless given |
| `POST /chat` | cache hit first, then the budget, then the turn; the honest message on failure |
| `POST /tasks` | the same budget check |
| `alert_once(db_path, pager, now)` | measure the last five minutes, page what fires, resolve what does not |
| `build_model(settings)` | the primary, wrapped in a fallback when one is set |

## `RUNBOOK.md`

One section per alert: what it means, the first thing to look at, the usual fixes.
Written for whoever is woken up — which is you, in six months, having forgotten all
of this.

---

## Check it

```bash
pytest week-06/milestone -v
```

Then push through the pipeline, set `FALLBACK_PROVIDER`, `DAILY_BUDGET` and
`ALERT_WEBHOOK_URL` on your host, and check that the alerts service is running.

## Friday

The defence switches your model off, live.
