# Day 2 - a job queue is a table.
#
#   SCHEMA      CREATE TABLE IF NOT EXISTS jobs:
#                 id          INTEGER PRIMARY KEY      (SQLite numbers it for you)
#                 kind        TEXT not null            e.g. "chat"
#                 payload     TEXT not null            the job's input, as JSON
#                 status      TEXT not null default 'queued'
#                             queued -> running -> done
#                                              -> queued again, or dead
#                 attempts    INTEGER not null default 0
#                 result      TEXT                     set when done
#                 error       TEXT                     the last failure
#                 claimed_by  TEXT                     which worker has it
#                 claimed_at  REAL                     when it took it
#                 created_at  REAL not null
#
#   create_tables(db)
#   enqueue(db, kind, payload, now) -> int     payload is a dict; the new job's id
#   get(db, job_id) -> dict | None             every column, with "payload" as a
#                                              dict again; None for no such job
#
#   claim(db, worker, now) -> dict | None
#       Take the OLDEST queued job: set status 'running', claimed_by, claimed_at,
#       and add one to attempts. Return it (as get would), or None if nothing is
#       queued. Two workers must NEVER get the same job, so the look and the
#       update happen inside one BEGIN IMMEDIATE ... COMMIT. IMMEDIATE takes the
#       write lock at BEGIN, so a second worker waits until the first is done.
#
#   finish(db, job_id, result)      status 'done', the result stored
#   fail(db, job_id, error, max_attempts=3) -> str
#       store the error and clear claimed_by and claimed_at. If attempts is below
#       max_attempts the job goes back to 'queued'; otherwise it is 'dead'.
#       Return the new status.
#
# `now` is passed in, not read from the clock, so the tests can control time.
