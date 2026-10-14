# Day 3 - Desk behind POST /chat.
#
# from desk.app import take_turn      (given - you wrote it in Agent From Zero)
#
#   class ChatIn(BaseModel)     message: 1-2000 characters
#                               conversation_id: str or None, default None
#   class ChatOut(BaseModel)    conversation_id: str, reply: str
#
#   new_id() -> str             12 hex characters, different every time
#                               (uuid.uuid4().hex[:12])
#
#   create_app(model, turn=take_turn) -> FastAPI
#       Its conversations live in a dictionary made inside create_app:
#       {conversation_id: history}.
#
#   GET  /health    {"status": "ok"}
#   POST /chat      ChatIn in, ChatOut out
#       no conversation_id         a new conversation, with a new id and an
#                                  empty history
#       a conversation_id it has   continue that conversation's history
#       one it does not have       404, "No such conversation."
#       Then: turn(model, history, message) returns {"text", "history"}. Store
#       the new history under the id, and reply with the text.
#       If turn RAISES anything: 503, "Desk is unavailable right now." - and
#       never a traceback.
#
# `turn` is passed in so the tests can hand you a fake one. Dependency
# injection, as in every week of Agent From Zero.
