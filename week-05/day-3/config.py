# Day 3 - everything that differs between your laptop and the server is a setting.
#
#   REQUIRED = ("DATABASE_URL", "DESK_KEYS")
#
#   class Settings(BaseModel)
#       database_url: str, keys: dict[str, str] ({key: user}),
#       roles: dict[str, str] ({user: role}), provider: str,
#       port: int (1-65535), environment: "development" | "staging" | "production",
#       version: str
#
#   parse_pairs(text) -> dict      "alice:x, bob:y" -> {"alice": "x", "bob": "y"};
#                                  empty pieces skipped; ValueError without a colon
#
#   load_settings(env=None) -> Settings      env defaults to os.environ
#       - every REQUIRED name that is missing or blank goes in ONE RuntimeError:
#             "Not set: DATABASE_URL, DESK_KEYS. See .env.example."
#         Somebody fixing a deploy should learn everything that is wrong at once.
#       - DESK_KEYS is user:key pairs; a key under 16 characters is a ValueError.
#         keys is stored the other way round: {key: user}.
#       - DESK_ROLES (default ""), AGENT_PROVIDER (default "fake"),
#         PORT (default "8000"), ENVIRONMENT (default "development"),
#         VERSION (default "dev")
#       - in production: the fake model is a ValueError, and so is VERSION "dev"
#
#   mask_url(url) -> str
#       "postgresql://desk:hunter2@db:5432/desk" -> "postgresql://desk:****@db:5432/desk"
#       a URL with no password in it comes back unchanged
#
#   redacted(settings) -> dict       safe to log at startup:
#       {"database_url": <masked>, "users": <sorted user names - never keys>,
#        "roles", "provider", "port", "environment", "version"}
#
#   readiness(checks) -> {"ready": bool, "failing": [names]}
#       checks maps a name to a function returning True. A check that returns
#       anything else, or RAISES, is failing.
