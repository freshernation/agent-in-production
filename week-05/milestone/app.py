# Week 5 milestone - Project 1: deployed, by CI, behind a gate.
#
# Copy everything your week 4 milestone used, and this week's database.py,
# checks.py, config.py and release.py. Start from your week-04/milestone/app.py.
#
#   create_app(model, keys, roles, db_path, limiter, clock=time.time, version="dev")
#       as week 4, plus:
#       GET /health   {"status": "ok", "version": version}   - so you can tell
#                     which release is live
#       GET /ready    readiness({"database": <a function that runs SELECT 1>})
#                     200 when ready, 503 when not. /health says "the process is
#                     up"; /ready says "it can actually serve".
#
#   from_environment() -> FastAPI
#       settings = load_settings()
#       print the redacted settings - never the real ones
#       a Limiter(20, 0.5, time.monotonic)
#       create_app(llm.connect(settings.provider), settings.keys, settings.roles,
#                  sqlite_path(settings.database_url), limiter,
#                  version=settings.version)
#
# Then: Dockerfile, compose.yaml and .dockerignore from day 1 (add VERSION and
# ENVIRONMENT to the api's environment), ci.yml with a deploy job, and the two
# documents.
