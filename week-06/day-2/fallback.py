# Day 2 - the model provider is down.
#
#   DOWN_MESSAGE    what a user is told when no model can be reached. Say that
#                   nothing was done, and when to try again. 15 words or more.
#
#   class Breaker(threshold, cooldown, clock)
#       A circuit breaker. After `threshold` failures in a row it OPENS, and the
#       primary is not even tried until `cooldown` seconds have passed.
#       .state -> "closed" | "open" | "half-open"
#           closed      never opened, or a success since
#           open        opened less than `cooldown` seconds ago
#           half-open   opened at least `cooldown` seconds ago: try one call
#       .allows() -> bool      True unless open
#       .succeeded()           back to closed, failures back to 0
#       .failed()              count it. Open (record the time) when failures
#                              reach the threshold - or at once if half-open:
#                              the one trial call failed, so wait again.
#
#   class FallbackModel(primary, secondary, breaker)
#       Stands in for a model, like week 4's Recorder.
#       .last_served -> "primary" | "secondary" | None
#       .chat(messages, system=None, tools=None, max_tokens=None)
#           if the breaker allows: try the primary. On ModelError, tell the
#           breaker it failed and fall through. On success, tell it so, set
#           last_served, return the reply.
#           Otherwise (or after a failure): ask the secondary, set last_served
#           to "secondary", and return its reply. If the secondary raises too,
#           let it raise.
