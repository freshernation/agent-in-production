# Day 4 - deploy only what passed, know what is live, and go back fast.
#
#   should_deploy(results, branch) -> (bool, reason)
#       `results` is day 2's run_all output. In this order:
#         any check failed      (False, "Checks failed: evals, attacks.")
#         no checks at all      (False, "No checks ran.")
#         branch is not main    (False, "Only main is deployed; this is <branch>.")
#         otherwise             (True, "All checks passed on main.")
#
#   A release history is a list, oldest first, of
#       {"version": "1.4.0", "status": ..., "at": <time>}
#   status is one of "deployed", "healthy", "failed", "rolled_back".
#
#   record(history, version, status, at) -> list
#       a NEW list with one entry added. ValueError for an unknown status.
#   current(history) -> str | None
#       the version of the most recent entry that is "deployed" or "healthy"
#   rollback_target(history) -> str | None
#       the most recent "healthy" version that is NOT the current one. None if
#       there is nothing to go back to.
#
#   verify_release(fetch, base_url, expected_version) -> {"healthy": bool, "problems": [...]}
#       fetch(method, url, headers) returns (status, body as a dict). Two checks:
#         GET  <base>/health   must be 200 with "version" equal to expected_version
#                              ("/health answered 502", or
#                               "/health reports version '1.3.0', expected '1.4.0'")
#         POST <base>/chat     with NO key must be 401
#                              ("/chat without a key answered 200, not 401")
#       A release that serves the old version, or opens the door, is not healthy.
