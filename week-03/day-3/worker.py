# Day 3 - a worker, and a worker that dies.
#
# Copy jobs.py from day 2 into this folder.
#
#   run_once(db, handlers, worker, now, max_attempts=3) -> str
#       Claim one job and run it. `handlers` maps a job's kind to a function
#       that takes the payload and returns a string.
#         nothing to claim               "idle"
#         the handler returns            finish it; "done"
#         the handler raises             fail it with "<ErrorType>: <message>",
#                                        passing max_attempts on; "failed"
#         no handler for that kind       fail it with "No handler for 'kind'."
#                                        and max_attempts=1 - trying again will
#                                        not grow a handler; "failed"
#
#   requeue_stale(db, now, timeout) -> int
#       A worker that crashed never calls finish or fail; its job sits in
#       'running' for ever. Put every running job claimed more than `timeout`
#       seconds before `now` back to 'queued', clear claimed_by and claimed_at,
#       set error to "worker stopped responding", and return how many.
#       attempts is NOT changed: the claim already counted it.
#
#   EFFECTS      CREATE TABLE IF NOT EXISTS effects (key TEXT PRIMARY KEY, result TEXT NOT NULL)
#
#   once(db, key, function) -> result
#       Run function() at most once per key, ever. Create the table if needed.
#       If the key is in effects, return the stored result (json.loads) WITHOUT
#       calling function. Otherwise call it, store json.dumps(result) under the
#       key, and return it.
#
# A job can run twice: a worker can finish the work and die before it calls
# finish. `once` is how a job that sends something sends it only once.
