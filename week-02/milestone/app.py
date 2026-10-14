# Week 2 milestone - Desk for many users, on a database that outlives the server.
#
# Copy store.py, migrate.py, tenancy.py and permissions.py from this week's days.
# Start this file from your week-01/milestone/app.py: ChatIn, ChatOut and
# user_for come across unchanged.
#
#   parse_roles(text) -> dict[str, str]
#       "alice:owner, bob:reader"  ->  {"alice": "owner", "bob": "reader"}
#       ValueError for a piece with no colon, or a role that is not in ROLES.
#       A trailing comma is fine. A user who is not listed has no role.
#
#   create_app(model, keys, roles, db_path) -> FastAPI
#       When it is made: connect to db_path and run migrate(db, MIGRATIONS).
#
#       GET  /health           open: {"status": "ok"}
#       POST /chat             needs a key.
#            - a conversation id is looked up with load_history for THIS user;
#              None is a 404
#            - the agent runs with run_agent from desk.agent:
#                  schemas   schemas_for(role, SCHEMAS)
#                  tools     guard(tools_for(db, user), role)
#                  system    desk.app's SYSTEM
#                  dangerous desk.app's DANGEROUS, with approve=None
#                  history   the loaded history, and token_budget=TOKEN_BUDGET
#            - save carry(history, result) with save_history
#            - reply with result["answer"]
#            - anything raised by the agent: 503, never a traceback
#       GET  /conversations    needs a key: conversation_ids for the caller
#
#   One connection per REQUEST, not one for the whole app: write a dependency
#   that connects, yields the connection, and closes it afterwards. SQLite will
#   not let a connection made in one thread be used in another, and FastAPI
#   runs each request in whichever thread is free.
#
#   approve=None means anything in DANGEROUS is refused over HTTP. There is
#   nobody at the keyboard to ask. That is deliberate, and it stays that way
#   until there is a way to ask.
