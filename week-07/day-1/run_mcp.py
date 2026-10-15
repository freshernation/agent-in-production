"""Desk's notes as a local MCP server, over stdio - given.

    DESK_USER=you python3 run_mcp.py

You never run this by hand: an MCP host starts it. For Claude Code:

    claude mcp add desk -e DESK_USER=you -e DESK_DB=/full/path/desk.db -- python3 /full/path/run_mcp.py
"""

import os

from desk_mcp import build_server

if __name__ == "__main__":
    build_server(os.environ.get("DESK_DB", "desk.db"), os.environ["DESK_USER"]).run()
