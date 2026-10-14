# Day 2 - the smallest service.
#
#   class NoteIn(BaseModel)     as yesterday: title 1-80 characters, body up to 2000
#
#   create_app() -> FastAPI     a NEW app each time, with its own notes, kept in a
#                               dictionary made inside create_app. Titles are
#                               matched ignoring capitals, and stored lowercased.
#
#   GET    /health              200  {"status": "ok"}
#   POST   /notes               201  {"title": ..., "body": ...}
#                               409  if a note with that title exists
#                               422  if the body is not a valid NoteIn - FastAPI
#                                    does this for you
#   GET    /notes               200  the titles, sorted
#   GET    /notes/{title}       200  {"title": ..., "body": ...}   404 if missing
#   DELETE /notes/{title}       204  and an empty body              404 if missing
#
# Every error has a "detail" that says what went wrong in a sentence.
