# Week 6 milestone - Desk stays up.
#
# Copy everything your week 5 milestone used, and this week's alerts.py,
# fallback.py, caching.py and budget.py. Start from your week-05/milestone/app.py.
#
# Constants:
#   ALERT_WINDOW = 300
#   ALERT_RULES  = errors: error_rate above 0.05, min_requests 20
#                  slow:   p95_seconds above 30.0, min_requests 20
#                  spend:  cost above 2.0
#
# create_app(..., version="dev", cache=None, daily_budget=None)
#   cache          a ResponseCache, or None for no caching
#   daily_budget   dollars per user per day, or None for no limit
#
# POST /chat, in this order:
#   1. a NEW conversation (no conversation_id) with a cache: if the cache has
#      this user's question, return the stored ChatOut at once, with the
#      headers X-Cache: hit and X-Trace-Id. No budget check, no model call.
#   2. over today's budget: 429 with check_budget's message as the detail
#   3. take the turn. On any failure: 503 with DOWN_MESSAGE as the detail
#   4. a new conversation, with a cache, and cacheable(trace): store the
#      ChatOut as a dict (.model_dump())
# POST /tasks: the same budget check before queueing.
# GET /tasks/{id}: a dead task's result is DOWN_MESSAGE.
#
# alert_once(db_path, pager, now, rules=ALERT_RULES) -> list[str]
#   measure the last ALERT_WINDOW seconds. For each rule that is firing,
#   pager.alert(name, message, now) - the message names the metric, its value
#   and the limit. For each rule that is not, pager.resolve(name).
#   Return the firing names. Close the connection.
#
# build_model(settings)
#   connect_model(settings.provider) - and if settings.fallback_provider is set,
#   a FallbackModel of the two with Breaker(3, 60, time.monotonic).
#
# from_environment(): as before, plus build_model, a ResponseCache(3600,
#   time.time) and settings.daily_budget.
