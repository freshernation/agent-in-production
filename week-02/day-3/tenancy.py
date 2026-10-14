# Day 3 - many users, and tools that cannot reach past their own.
#
# Copy store.py from day 1 and migrate.py from day 2 into this folder.
#
#   bound(function, db, user)
#       returns a NEW function. Calling it with keyword arguments calls
#           function(db, user, **those_arguments)
#       Agent From Zero week 8's `watched`, doing a different job.
#
#   tools_for(db, user) -> dict
#       a dispatch table with exactly the names Desk's schemas use:
#           add_note, list_titles, find_notes, delete_note   - bound to db and user
#           calculate                                         - desk.kit's, as it is
#       The model sees the same schemas as before. None of them has a "user"
#       argument, so there is nothing it can write to reach another user.
#
#   clean(history) -> list
#       copies of the messages without any key starting with "_" - those hold a
#       provider's private data and are not safe to store
#
#   save_history(db, user, conversation_id, history)
#       stores clean(history) as JSON in `conversations`. Saving the same
#       (user, id) again replaces it:  INSERT ... ON CONFLICT (user, id) DO UPDATE
#   load_history(db, user, conversation_id) -> list | None
#       None when there is no such conversation FOR THIS USER
#   conversation_ids(db, user) -> list[str]
#       this user's conversation ids, sorted
