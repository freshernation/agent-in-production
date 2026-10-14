# Day 4 - a key per caller.
#
# Start from your day-3 chat.py: ChatIn, ChatOut and the /chat logic come with it.
#
#   user_for(header, keys) -> str | None
#       `keys` maps an API key to the user it belongs to:
#           {"k-alice-123": "alice", "k-bob-456": "bob"}
#       `header` is the whole Authorization header: "Bearer k-alice-123".
#       Returns the user, or None for a missing, malformed or wrong key.
#       Compare with secrets.compare_digest - and compare against EVERY key,
#       without stopping at the first match, so the time taken says nothing.
#
#   create_app(model, keys, turn=take_turn) -> FastAPI
#
#   GET  /health            open to anybody: {"status": "ok"}
#   POST /chat              needs a key. As day 3, except:
#                             - conversations belong to the user who started
#                               them. Keep them under (user, conversation_id).
#                             - another user's conversation id is 404, exactly
#                               like one that does not exist
#   GET  /conversations     needs a key. The caller's own conversation ids, sorted
#
#   No key, or a wrong one:  401, "Missing or wrong API key.", and the header
#                            WWW-Authenticate: Bearer
#
# Write the key check once, as a dependency, and use it on both routes.
