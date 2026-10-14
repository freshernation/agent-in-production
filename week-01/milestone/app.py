# Week 1 milestone - Desk behind an API, configured from the environment.
#
# Start from your day-4 keys.py. Everything in it comes across unchanged:
# ChatIn, ChatOut, user_for, create_app. Then add:
#
#   parse_keys(text) -> dict[str, str]
#       Reads the DESK_KEYS setting:  "alice:k-alice-0123456789, bob:k-bob-0123456789"
#       Returns {key: user}. Spaces around names and keys are ignored, and an
#       empty piece (a trailing comma) is skipped. ValueError, saying what is
#       wrong, when:
#         - a piece has no colon
#         - a name is empty, or a key is shorter than 16 characters
#         - two users have the same key
#         - there are no keys at all
#
#   from_environment() -> FastAPI
#       create_app(connect(), parse_keys(os.environ.get("DESK_KEYS", "")))
#       This is what uvicorn runs:
#           uvicorn app:from_environment --factory
#
# A service that starts with no keys, or a weak one, should refuse to start,
# not start and let everyone in.
