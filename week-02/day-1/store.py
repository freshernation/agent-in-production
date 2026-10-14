# Day 1 - notes in a database, and every query says whose.
#
#   SCHEMA          the CREATE TABLE statement for `notes`:
#                     user   TEXT, not null
#                     title  TEXT, not null, COLLATE NOCASE  (so 'Milk' = 'milk')
#                     body   TEXT, not null, default ''
#                     the PRIMARY KEY is (user, title)
#                   Use CREATE TABLE IF NOT EXISTS.
#
#   connect(path) -> sqlite3.Connection
#                   sqlite3.connect(path, isolation_level=None) - each statement
#                   is saved as soon as it runs - then
#                   PRAGMA busy_timeout = 5000 so a second writer waits
#                   instead of failing at once.
#   create_tables(db)
#
# The four tools, now with a user. Same sentences as Desk's kit:
#   add_note(db, user, title, body="")   "Saved 'milk'."
#                                        "A note needs a title."
#                                        "There is already a note called 'milk'."
#   list_titles(db, user)                "1. milk\n2. eggs"  or  "No notes yet."
#   find_notes(db, user, word)           "milk: two litres"   or
#                                        "No notes mention 'car'."
#   delete_note(db, user, title)         "Deleted 'milk'."  or  "No note called 'car'."
#
# Rules the tests check:
#   - EVERY query has "WHERE user = ?". One user never sees another's notes.
#   - Values go in as ? parameters. Never build SQL with f-strings or +.
#   - A duplicate is caught by the database (the primary key), not by looking
#     first: between your look and your insert, another request can insert.
#   - Notes come back in the order they were added.
