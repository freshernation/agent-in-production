# Day 4 - one caller cannot starve another, and a reply that arrives as it is written.
#
#   class Bucket(capacity, per_second, clock)
#       A token bucket. It starts full: `capacity` tokens. It gains `per_second`
#       tokens every second, never holding more than `capacity`. `clock` is a
#       function returning the time in seconds - time.monotonic in real use, a
#       fake in the tests.
#       .take() -> bool        refill for the time passed; if a whole token is
#                              there, spend it and return True; otherwise False
#       .wait_time() -> float  refill; 0.0 if a token is there, otherwise how
#                              many seconds until one will be
#
#   class Limiter(capacity, per_second, clock)
#       One Bucket PER CALLER, made the first time that caller is seen.
#       .allow(caller) -> bool
#       .retry_after(caller) -> int    that caller's wait_time, rounded UP to a
#                                      whole second, and never less than 1
#
#   chunks(text, size)
#       a GENERATOR: `yield` the text `size` characters at a time
#
#   create_app(limiter) -> FastAPI
#       POST /ping     the caller is the X-Caller header (default "anonymous").
#                      Allowed: 200 {"ok": true}. Not: 429, "Too many requests.
#                      Slow down.", and a Retry-After header in whole seconds.
#       GET  /stream?text=...&size=5
#                      StreamingResponse(chunks(text, size), media_type="text/plain")
