"""Unit tests for EnvLoader.

Test coverage includes:
- valid .env file returns correct DBConfig
- missing variables fall back to defaults
- custom values override defaults
"""

import pytest
from pathlib import Path

from work.library.config.env_loader import EnvLoader, DBConfig

_MYSQL_VARS = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_DB"]


def _write_env(tmp_path: Path, content: str) -> Path:
    env_file = tmp_path / ".env"
    env_file.write_text(content, encoding="utf-8")
    return env_file


@pytest.fixture(autouse=True)
def clear_mysql_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove all MYSQL_* vars so load_dotenv can set them from the temp file."""
    for var in _MYSQL_VARS:
        monkeypatch.delenv(var, raising=False)


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.unit
def test_valid_env_returns_db_config(tmp_path: Path) -> None:
    """All variables present → DBConfig with correct values."""

    env = _write_env(tmp_path, (
        "MYSQL_USER=testuser\n"
        "MYSQL_PASSWORD=secret\n"
        "MYSQL_HOST=192.168.1.1\n"
        "MYSQL_PORT=3307\n"
        "MYSQL_DB=testdb\n"
    ))

    config = EnvLoader(env).get_db_config()

    assert isinstance(config, DBConfig)
    assert config.user == "testuser"
    assert config.password == "secret"
    assert config.host == "192.168.1.1"
    assert config.port == 3307
    assert config.database == "testdb"


# =========================================================
# DEFAULTS
# =========================================================

@pytest.mark.unit
def test_empty_env_uses_defaults(tmp_path: Path) -> None:
    """Empty .env file falls back to built-in defaults."""

    env = _write_env(tmp_path, "")

    config = EnvLoader(env).get_db_config()

    assert config.user == "root"
    assert config.password == ""
    assert config.host == "localhost"
    assert config.port == 3306
    assert config.database == "nvidia_timeseries"


@pytest.mark.unit
def test_partial_env_uses_defaults_for_missing(tmp_path: Path) -> None:
    """Only defined variables are overridden; others keep defaults."""

    env = _write_env(tmp_path, "MYSQL_USER=custom_user\n")

    config = EnvLoader(env).get_db_config()

    assert config.user == "custom_user"
    assert config.host == "localhost"
    assert config.port == 3306


# =========================================================
# PORT TYPE
# =========================================================

@pytest.mark.unit
def test_port_is_integer(tmp_path: Path) -> None:
    """Port is parsed as int regardless of string representation."""

    env = _write_env(tmp_path, "MYSQL_PORT=5432\n")

    config = EnvLoader(env).get_db_config()

    assert isinstance(config.port, int)
    assert config.port == 5432


# =========================================================
# INVALID VALUES
# =========================================================

@pytest.mark.unit
def test_invalid_port_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Non-numeric MYSQL_PORT raises ValueError."""

    env = _write_env(tmp_path, "")
    monkeypatch.setenv("MYSQL_PORT", "not_a_number")

    with pytest.raises(ValueError):
        EnvLoader(env).get_db_config()
