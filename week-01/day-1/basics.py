# Day 1 - the Python Agent From Zero left out, because FastAPI is written in it.
#
#   class Note
#       Note(title, body="")      title has its surrounding spaces stripped
#       .title, .body             attributes
#       .summary(width=30)        "milk: two litres"  - or, when the body is
#                                 longer than `width`, its first `width`
#                                 characters followed by "..."
#       .matches(word)            True when the word is in the title or the
#                                 body, ignoring capitals
#
#   CALLS                         a list, empty to start with
#
#   logged(function)              a decorator. The function it returns appends
#                                 the decorated function's NAME to CALLS, then
#                                 calls it and returns its result. Use
#                                 functools.wraps so the wrapper keeps the name.
#
#   class NoteIn(BaseModel)       pydantic:
#       title: str                1 to 80 characters
#       body: str                 up to 2000 characters, default ""
#
# Every function and method has type hints. The tests check that too.
