# Day 4 - what each user may make Desk do.
#
#   READER          {"list_titles", "find_notes", "calculate"}
#   WRITER          READER and "add_note"
#   OWNER           WRITER and "delete_note" and "share_note"
#   ROLES           {"reader": READER, "writer": WRITER, "owner": OWNER}
#
#   allowed(role) -> set[str]
#       a COPY of that role's set. An unknown role gets an empty set: a user
#       whose role nobody recorded may do nothing.
#
#   schemas_for(role, schemas) -> list[dict]
#       only the schemas this role may use, in their original order. A tool the
#       model is never told about is a tool it will rarely ask for.
#
#   refusal(name, role)
#       returns a function that takes any keyword arguments and returns
#           "Refused: the reader role cannot use delete_note."
#
#   guard(tools, role) -> dict
#       a NEW table with every name kept, where each tool the role may NOT use
#       is replaced by refusal(name, role). Rarely is not never: if the model
#       asks for a tool it was not offered, this is what stops it.
#
# Two locks, on purpose: hide what is not allowed, and refuse it anyway.
