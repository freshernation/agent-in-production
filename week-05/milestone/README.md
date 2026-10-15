# Week 5 Milestone — Project 1: Desk, deployed

> Desk on a public URL, deployed by CI from a passing push to `main`, checked from the
> outside after every deploy.

**Deploy before you polish.** Getting a first version live on Tuesday makes Friday
about the project rather than about signup forms.

---

## The files

| File | Where it comes from |
|---|---|
| everything from your week 4 milestone | **copy** |
| `database.py`, `checks.py`, `config.py`, `release.py` | **copy from this week's days** |
| `Dockerfile`, `compose.yaml`, `.dockerignore` | **copy from day 1**, and add `VERSION` and `ENVIRONMENT` to the api |
| `smoke.py`, `run_worker.py`, `run_exporter.py`, `langfuse_client.py` | given |
| `app.py` | your week 4 milestone, configurable and versioned |
| `ci.yml` | day 2's, with a deploy job |
| `DEPLOYMENT.md`, `PROJECT_README.md` | new |

`check_live.py` is at the top of the repository.

## `app.py`

| Change | What it means |
|---|---|
| `create_app(..., version="dev")` | `/health` reports the version |
| `GET /ready` | 200 when the database answers, 503 when not |
| `from_environment()` | `load_settings()`, print the redacted settings, build the app |

## `ci.yml`

Two jobs. `checks` on every push and pull request. `deploy` with `needs: checks`, only
on a push to `main`: call the host's deploy hook from a **secret**, wait, then run
`check_live.py` with the live URL and the commit as the expected version.

## The documents

| Document | Sections |
|---|---|
| `DEPLOYMENT.md` | Where it runs · Configuration · How a change reaches it · Going back |
| `PROJECT_README.md` | What it is · Try it (**the live URL**) · How it is built · How I know it works · What I would do next |

---

## Check it

```bash
pytest week-05/milestone -v
python3 check_live.py https://your-url.example
```

## Friday

The defence starts with the live URL, on your instructor's machine.
