"""Week 5, Day 3 - settings from the environment.

Run me:  pytest week-05/day-3 -v
"""

import pytest

GOOD = {"DATABASE_URL": "sqlite:////data/desk.db",
        "DESK_KEYS": "alice:k-alice-0123456789, bob:k-bob-0123456789"}


@pytest.fixture
def config(load):
    return load("config.py")


class TestLoad:
    def test_defaults(self, config):
        s = config.load_settings(GOOD)
        assert s.keys == {"k-alice-0123456789": "alice", "k-bob-0123456789": "bob"}
        assert s.roles == {} and s.provider == "fake" and s.port == 8000
        assert s.environment == "development" and s.version == "dev"

    def test_everything_set(self, config):
        s = config.load_settings({**GOOD, "DESK_ROLES": "alice:owner", "AGENT_PROVIDER": "claude",
                                  "PORT": "9000", "ENVIRONMENT": "production", "VERSION": "1.4.0"})
        assert s.roles == {"alice": "owner"} and s.port == 9000 and s.version == "1.4.0"

    def test_every_missing_setting_at_once(self, config):
        with pytest.raises(RuntimeError) as caught:
            config.load_settings({})
        message = str(caught.value)
        assert "DATABASE_URL" in message and "DESK_KEYS" in message, (
            f"'{message}'. Name everything that is missing in one go: whoever is "
            "fixing the deploy should not discover them one restart at a time."
        )

    def test_blank_is_missing(self, config):
        with pytest.raises(RuntimeError):
            config.load_settings({**GOOD, "DATABASE_URL": "   "})

    def test_a_short_key(self, config):
        with pytest.raises(ValueError):
            config.load_settings({**GOOD, "DESK_KEYS": "alice:short"})

    @pytest.mark.parametrize("extra", [{"PORT": "0"}, {"PORT": "70000"}, {"ENVIRONMENT": "prod"}])
    def test_bad_values(self, config, extra):
        with pytest.raises(Exception):
            config.load_settings({**GOOD, **extra})


class TestProduction:
    def test_no_fake_model(self, config):
        with pytest.raises(ValueError):
            config.load_settings({**GOOD, "ENVIRONMENT": "production", "VERSION": "1.0.0"})

    def test_needs_a_version(self, config):
        with pytest.raises(ValueError):
            config.load_settings({**GOOD, "ENVIRONMENT": "production", "AGENT_PROVIDER": "claude"})


class TestRedacted:
    def test_mask_url(self, config):
        assert config.mask_url("postgresql://desk:hunter2@db:5432/desk") == (
            "postgresql://desk:****@db:5432/desk")
        assert config.mask_url("sqlite:////data/desk.db") == "sqlite:////data/desk.db"

    def test_no_secret_survives(self, config):
        s = config.load_settings({**GOOD, "DATABASE_URL": "postgresql://desk:hunter2@db/desk"})
        shown = config.redacted(s)
        text = str(shown)
        assert "hunter2" not in text and "k-alice" not in text, (
            "This dictionary gets logged at startup, into a system the whole "
            "team can read. Nothing in it may be a secret."
        )
        assert shown["users"] == ["alice", "bob"]


class TestReadiness:
    def test_all_good(self, config):
        assert config.readiness({"db": lambda: True}) == {"ready": True, "failing": []}

    def test_one_failing(self, config):
        result = config.readiness({"db": lambda: True, "model": lambda: False})
        assert result == {"ready": False, "failing": ["model"]}

    def test_a_check_that_raises_is_failing(self, config):
        def broken():
            raise ConnectionError("no database")
        assert config.readiness({"db": broken}) == {"ready": False, "failing": ["db"]}

    def test_only_true_is_true(self, config):
        assert config.readiness({"db": lambda: "yes"})["ready"] is False
