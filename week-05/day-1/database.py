# Day 1 - one setting says where the database is.
#
#   dialect(url) -> "sqlite" | "postgres"
#       "sqlite:///data/desk.db"            -> "sqlite"
#       "postgresql://..." or "postgres://" -> "postgres"
#       anything else: ValueError naming the scheme - and NEVER the rest of the
#       URL, which may hold a password
#
#   sqlite_path(url) -> str
#       the path after "sqlite:///". ValueError if it is not a SQLite URL, or
#       the path is empty.
#
#   connect(url)
#       SQLite: sqlite3.connect(path, isolation_level=None), then
#               PRAGMA busy_timeout = 5000
#               PRAGMA journal_mode = WAL
#       WAL lets one process read while another writes - your server and your
#       worker are two processes sharing one file now.
#       Postgres: import psycopg inside the function, and
#               return psycopg.connect(url, autocommit=True)
#       (Not tested here. It is what the deep track uses.)
#
#   adapt(sql, kind) -> str
#       SQLite and Postgres write parameters differently: ? and %s. For
#       "postgres", replace every ? with %s - except a ? inside single quotes,
#       which is text, not a parameter. For "sqlite", return it unchanged.
