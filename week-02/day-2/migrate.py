# Day 2 - a schema that can change without losing anything.
#
#   MIGRATIONS      a list of SQL statements, oldest first. Never edit one that
#                   has run anywhere; add a new one at the end. Yours:
#                     1. CREATE TABLE notes - as day 1's SCHEMA, without IF NOT EXISTS
#                     2. CREATE TABLE conversations:
#                          user TEXT not null, id TEXT not null,
#                          history TEXT not null default '[]',
#                          PRIMARY KEY (user, id)
#                     3. ALTER TABLE notes ADD COLUMN created TEXT NOT NULL DEFAULT ''
#
#   current_version(db) -> int
#                   makes the table schema_version (version INTEGER NOT NULL) if
#                   it is not there, and returns the highest version in it -
#                   0 when it is empty
#
#   migrate(db, migrations) -> int
#                   runs every migration after the current version, in order,
#                   and returns how many it ran. Each one runs INSIDE a
#                   transaction together with recording its version number:
#
#                       BEGIN
#                       the migration
#                       INSERT INTO schema_version (version) VALUES (?)
#                       COMMIT
#
#                   If either statement fails: ROLLBACK, and raise. The version
#                   stays at the last migration that worked.
#
# The connection comes from day 1's connect(), so you control BEGIN and COMMIT
# yourself. Running migrate twice must do nothing the second time.
