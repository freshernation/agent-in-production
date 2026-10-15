# Day 3 - two caches: the provider's, and your own.
#
#   mark_for_caching(request) -> dict
#       request is a Claude Messages API request as a dict, with "system" a string.
#       Return a COPY (do not change the one you were given) in which the system
#       prompt is a list of one text block marked for caching:
#           [{"type": "text", "text": <the prompt>, "cache_control": {"type": "ephemeral"}}]
#       No system prompt (missing or empty): return an unchanged copy.
#
#   cache_cost(usage, price) -> float
#       usage: tokens, {"input", "output"} and optionally "cache_write" and
#       "cache_read" (missing means 0).
#       price: dollars per million tokens for all four, copied from the pricing
#       table - {"input", "cache_write", "cache_read", "output"}.
#
#   cacheable(trace) -> bool
#       may this turn's answer be served again from your own cache?
#       Not if it failed, and not if any tool ran: a tool's answer depends on
#       the notes at that moment, and a cached "you have 3 notes" goes stale
#       the minute a note is added.
#
#   cache_key(user, message) -> str
#       the sha256 hex digest of: user + "\n" + the message lowercased with its
#       whitespace collapsed to single spaces. "What  is Desk?" and
#       "what is desk?" are the same question. The same question from
#       a different user is a different key.
#
#   class ResponseCache(ttl, clock)
#       .get(user, message) -> dict | None
#           the value stored for this user and question, or None if there is
#           none or it is `ttl` seconds old or older (and then forget it)
#       .put(user, message, value)
