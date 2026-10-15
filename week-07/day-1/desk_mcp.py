# Day 1 - Desk's tools, served over MCP.
#
# Copy store.py from your week 6 milestone into this folder.
#
#   from mcp.server import MCPServer
#
#   INSTRUCTIONS    what any MCP client is told about this server. 15 words or
#                   more, and say that a note's contents are not instructions.
#
#   build_server(db_path, user) -> MCPServer
#       create the notes table if needed, then return a server named "Desk"
#       with INSTRUCTIONS and exactly three tools, each one opening its own
#       connection to db_path and closing it, always acting as `user`:
#
#         list_titles()                -> store.list_titles
#         find_notes(word)             -> store.find_notes
#         add_note(title, body="")     -> store.add_note
#
#       The function's name is the tool's name, its docstring is the
#       description (8 words or more), and its type hints are the schema.
#       Use Annotated[str, Field(...)] so the SDK refuses, before your code
#       runs: an empty or over-100-character title or word, a body over 5000.
#
#       delete_note is NOT served. In Desk a deletion needs a person's
#       approval, and this server has no way to ask for one.
