# Week 4 milestone - every request traced, costed and rateable.
#
# Copy into this folder: everything your week 3 milestone used (store, migrate,
# tenancy, permissions, jobs, worker, limits) and this week's recorder,
# tracestore, feedback and exporter. langfuse_client.py is given.
# Start from your week-03/milestone/app.py.
#
#   PRICE = {"input": 3.0, "output": 15.0}    dollars per million tokens. Put in
#                                             your real model's price.
#
#   take_turn(model, db, roles, user, message, conversation_id, history,
#             clock=time.time) -> (answer, trace)
#       As week 3, but every run is recorded:
#         - wrap the model in a Recorder, and the guarded tools in record_tools
#         - a new trace id: uuid.uuid4().hex - 32 hex characters, the form the
#           platform uses
#         - build the trace (session = the conversation id) and SAVE it - for
#           a failed run too, before raising. The failures are the traces you
#           will most want to look at.
#       A run that stopped with "error" is saved with an empty output, then raises.
#
#   ChatOut now has a third field: trace_id. /chat also sets the header
#   X-Trace-Id. A user who reports a problem can quote it.
#
#   class FeedbackIn(BaseModel)  trace_id: str, score: int, comment: str (max 1000, default "")
#
#   POST /feedback              needs a key. score not 1 or -1: 422. A trace that
#                               is not the caller's: 404 "No such trace.".
#                               Otherwise {"status": "recorded"}.
#
#   create_app also creates the traces and feedback tables.
#   work_once is unchanged except that take_turn now returns two things.
#
#   export_once(db_path, client) -> dict
#       connect, export_pending(db, client), close. run_exporter.py calls it.
