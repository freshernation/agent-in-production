# Day 1 — Containers, and one setting for the database

> **By the end of today** Desk and its worker run as two containers sharing one
> database, started with one command.

---

## Read first

- [ ] Docker — [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/), the parts on the build cache, `.dockerignore` and `USER` · 20 min
- [ ] Docker — [Compose: how Compose works](https://docs.docker.com/compose/intro/compose-application-model/) · 15 min
- [ ] SQLite — [Write-Ahead Logging](https://www.sqlite.org/wal.html), the first two sections · 10 min

---

## What you need to know

### An image is your laptop, written down

Everything the service needs — Python, the packages, your code — in a file, so that
the server runs exactly what you tested. `python:3.12-slim` is the starting point.

### Order is speed

Docker rebuilds from the first line that changed. Copy `requirements.txt` and install,
**then** copy the code. A one-line change then reuses the installed packages instead
of reinstalling them all.

### Not as root

`USER desk`. If someone gets code running in your container, they should not be root
in it.

### Two services, one volume

The API and the worker are the same image with different commands. Both mount the
same volume at `/data`, where the database lives. The volume outlives every container:
rebuild, restart, redeploy, and the data is still there.

### Two processes on one SQLite file

`PRAGMA journal_mode = WAL` lets one process read while another writes. With
`busy_timeout`, a second writer waits its turn instead of failing. That is enough for
one API and one worker. It is **not** enough for two machines — that needs Postgres.

### One URL says where the database is

`DATABASE_URL=sqlite:////data/desk.db` (four slashes: the fourth is the root of the
path). `database.py` reads it, and also shows what changes for Postgres: `?` becomes
`%s`, and a few SQLite-only phrases need replacing. Read that list as the port you
would do on the day you need it.

---

## Exercises

```bash
pytest week-05/day-1 -v
```

Write `database.py`, and fill in `Dockerfile`, `compose.yaml` and `.dockerignore`. The
tests read your files; then build them for real:

```bash
docker compose up --build
```

---

## Predict-then-run

Build the image, change one line of `app.py`, build again. Predict how long the
second build takes. Then move the `COPY . .` above the install and repeat.

---

## Before you close the laptop

Commit, push, fill in the signal log.
