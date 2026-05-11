"""Unit tests for ConfigManager.

Test coverage includes:
- combined config returns both AppConfig and DBConfig
- missing app config file propagates FileNotFoundError
"""

import json
import pytest
from pathlib import Path

from work.library.config.config_manager import ConfigManager, Config
from work.library.config.app_config_loader import AppConfig
from work.library.config.env_loader import DBConfig

_MYSQL_VARS = ["MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_PORT", "MYSQL_DB"]


@pytest.fixture(autouse=True)
def clear_mysql_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove all MYSQL_* vars so load_dotenv reads from the temp file."""
    for var in _MYSQL_VARS:
        monkeypatch.delenv(var, raising=False)


_VALID_APP_CONFIG = {
    "paths": {
        "data_dir": "work/data",
        "output_dir": "work/output",
        "graphics_dir": "work/graphics",
        "logs_dir": "work/logs",
    },
    "ui": {
        "language": "en",
        "theme": "dark",
        "window_width": 1200,
        "window_height": 800,
    },
    "reports": {
        "default_export_format": "csv",
        "default_chart_format": "png",
    },
    "analysis": {
        "sma_windows": [5, 20],
        "ema_windows": [12, 26],
        "volatility_window": 20,
        "forecast_horizon": 30,
    },
}


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.unit
def test_load_returns_combined_config(tmp_path: Path) -> None:
    """ConfigManager.load() merges AppConfig and DBConfig correctly."""

    app_cfg = tmp_path / "app_config.json"
    app_cfg.write_text(json.dumps(_VALID_APP_CONFIG), encoding="utf-8")

    env_file = tmp_path / ".env"
    env_file.write_text("MYSQL_USER=admin\nMYSQL_DB=prod_db\n", encoding="utf-8")

    config = ConfigManager(
        env_path=str(env_file),
        app_config_path=app_cfg,
    ).load()

    assert isinstance(config, Config)
    assert isinstance(config.app, AppConfig)
    assert isinstance(config.db, DBConfig)
    assert config.db.user == "admin"
    assert config.db.database == "prod_db"
    assert config.app.ui.language == "en"


# =========================================================
# ERROR PROPAGATION
# =========================================================

@pytest.mark.unit
def test_missing_app_config_raises(tmp_path: Path) -> None:
    """Missing app config file propagates FileNotFoundError."""

    env_file = tmp_path / ".env"
    env_file.write_text("", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        ConfigManager(
            env_path=str(env_file),
            app_config_path=tmp_path / "nonexistent.json",
        ).load()
