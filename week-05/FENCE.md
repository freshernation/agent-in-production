# Week 5 — Concept fence

## Allowed

**Everything from weeks 1 to 4**, plus:

- A Dockerfile: `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `USER`, `CMD`
- Compose: services, `build`, `environment`, `volumes`, `restart`, `healthcheck`
- `.dockerignore`
- GitHub Actions: `on`, `jobs`, `needs`, `if`, `steps`, `uses`, `run`, `secrets`, `vars`
- `subprocess.run` and its `returncode`
- SQLite's WAL mode
- Reading a URL apart; the Postgres driver, in `database.py` only

## Not yet

Kubernetes · Terraform · more than one instance of the API · Postgres for the whole
app (deep track) · alerts (week 6) · blue-green or canary deploys · building images
in CI and pushing them to a registry

---

## Why the host builds the image, not CI

Building in CI and pushing to a registry is how larger teams do it, and it is one more
account, one more secret and one more thing to break in the week you deploy for the
first time. This week CI decides *whether* to deploy and checks the result; the host
builds. Moving the build into CI is a good first change after the course.
