# Week 5 — Friday defence

Forty minutes. **It starts with the live URL.** If it is down, that is the defence.

---

## Phase 0 — From the outside (5 min)

Run `check_live.py` against their URL, on your machine. Then open the repository's
Actions tab and look at the last three runs.

## Phase 1 — Explain (10 min)

1. *"Walk me from `git push` to the new version answering."*
2. *"Why are the requirements copied and installed before the code?"*
3. *"The deploy hook URL — where is it, and what could someone do with it?"*
4. *"`/health` and `/ready`. Which one does your host poll, and why does it matter?"*
5. *"Two API instances on your SQLite file. What breaks?"*

## Phase 2 — Mutate, live, through the pipeline (12 min)

Ask for a small visible change — the version string, a message — and watch it go
through CI to production. **No touching the server.** Then:

- *"Break it on purpose: push a change that fails one test."* It must not deploy.
- *"Roll back to the previous release."* Time it.

## Phase 3 — Debug (10 min)

| Seed | Break | Probes |
|---|---|---|
| Easy | the Dockerfile copies the code before installing | Every build is slow. Do they know why? |
| Medium | `deploy` without `needs: checks` | A failing push deploys. Which file, which line? |
| Medium | uvicorn bound to `127.0.0.1` | Works on the laptop, unreachable in the container |
| Nasty | `load_settings` defaults `DESK_KEYS` to an empty string | Starts happily in production, and nobody can log in — or worse |

The **Nasty** one: a service that starts with a broken configuration is worse than one
that refuses to.

---

## Scoring

| Phase | 5 | 3 | 1 |
|---|---|---|---|
| **Outside** | Live, right version, door shut | Live with a gap | Down |
| **Explain** | Traces push to production with every check named | Knows the order | Cannot say what CI checks |
| **Mutate** | Change, refusal and rollback all through the pipeline | Change works | Touches the server |
| **Debug** | Names the file and the consequence | Finds it | Guesses |
