"""Desk - the hardened notes agent from Agent From Zero, week 8, given complete.

You wrote every line of this in that course. It is handed back as a package so
that this course can be about one thing: running it for other people.

    from desk.app import take_turn           one turn of the agent
    from desk.agent import run_agent         the loop
    from desk.kit import SCHEMAS, TOOLS      the notes tools

    kit.py       the six tools, their schemas, run_tool
    agent.py     run_agent: the loop, its guards, the approval gate, the budget
    guards.py    repeat detection and clipping
    retry.py     call_with_retry
    memory.py    carry, trim, remember and recall
    context.py   sizes, shortening old results, compact
    leak.py      watch and make_approver
    app.py       Desk itself: SYSTEM, DANGEROUS, take_turn

The notes, memory and outbox live in files named by NOTES_FILE, MEMORY_FILE and
OUTBOX_FILE. Week 2 moves them into a database.
"""
