# Week 3 milestone - long work in the background, and nobody hogs the service.
#
# Copy into this folder: store.py, migrate.py, tenancy.py, permissions.py from
# your week 2 milestone, and jobs.py, worker.py, limits.py from this week.
# Start from your week-02/milestone/app.py.
#
#   STALE_AFTER = 300           seconds before a running job is presumed abandoned
#
#   take_turn(model, db, roles, user, message, conversation_id, history) -> str
#       What week 2's /chat did inside its try: run the agent for this user and
#       role, save carry(history, result), and return result["answer"]. Pull it
#       out into this function, because the worker needs it too.
#       One change: if the run stopped with "error" - the model could not be
#       reached - RAISE instead of returning. Desk's answer in that case
#       contains the error text, which must never reach a user, and a job that
#       raises is retried; one that returns is marked done.
#
#   create_app(model, keys, roles, db_path, limiter, clock=time.time)
#       When made: migrate, and jobs' create_tables.
#       The key dependency now also rate-limits: after finding the user, if
#       limiter.allow(user) is False, 429 "Too many requests. Slow down." with
#       a Retry-After header of limiter.retry_after(user).
#
#       GET  /health              open
#       POST /chat                as week 2, using take_turn
#       POST /tasks               ChatIn in. The same conversation rules as /chat
#                                 (unknown id: 404), but instead of running it,
#                                 enqueue a "chat" job with payload
#                                 {"user", "message", "conversation_id"} and
#                                 now=clock(). 202:
#                                 {"task_id", "conversation_id", "status": "queued"}
#       GET  /tasks/{task_id}     {"task_id", "status", "result"} - but 404 if there
#                                 is no such job OR it belongs to another user.
#                                 A dead job's result is "The task could not be
#                                 completed." - never its error text.
#       GET  /conversations       as week 2
#
#   work_once(model, roles, db_path, worker, now) -> str
#       What the worker process runs in a loop. Connect; requeue_stale(db, now,
#       STALE_AFTER); then run_once with one handler, "chat", that loads the
#       conversation's history and calls take_turn. Return run_once's answer.
#       Close the connection afterwards.
