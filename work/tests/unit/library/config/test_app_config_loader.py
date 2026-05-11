"""Unit tests for AppConfigLoader.

Test coverage includes:
- valid JSON file returns typed AppConfig
- missing file raises FileNotFoundError
- malformed JSON raises json.JSONDecodeError
- missing required top-level section raises KeyError
"""

import json
import pytest
from pathlib import Path

from work.library.config.app_config_loader import AppConfigLoader, AppConfig


_VALID_CONFIG = {
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
def test_load_valid_config(tmp_path: Path) -> None:
    """Valid JSON returns a fully typed AppConfig."""

    cfg_file = tmp_path / "app_config.json"
    cfg_file.write_text(json.dumps(_VALID_CONFIG), encoding="utf-8")

    config = AppConfigLoader(cfg_file).load()

    assert isinstance(config, AppConfig)
    assert config.paths.data_dir == "work/data"
    assert config.ui.language == "en"
    assert config.reports.default_export_format == "csv"
    assert config.analysis.volatility_window == 20
    assert config.analysis.sma_windows == (5, 20)
    assert config.analysis.ema_windows == (12, 26)


# =========================================================
# MISSING FILE
# =========================================================

@pytest.mark.unit
def test_missing_file_raises(tmp_path: Path) -> None:
    """Non-existent config file raises FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        AppConfigLoader(tmp_path / "no_such_file.json").load()


# =========================================================
# MALFORMED JSON
# =========================================================

@pytest.mark.unit
def test_malformed_json_raises(tmp_path: Path) -> None:
    """File with invalid JSON raises json.JSONDecodeError."""

    cfg_file = tmp_path / "bad.json"
    cfg_file.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        AppConfigLoader(cfg_file).load()


# =========================================================
# MISSING SECTIONS
# =========================================================

@pytest.mark.unit
def test_missing_paths_section_raises(tmp_path: Path) -> None:
    """Config without 'paths' key raises KeyError."""

    data = {k: v for k, v in _VALID_CONFIG.items() if k != "paths"}
    cfg_file = tmp_path / "app_config.json"
    cfg_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(KeyError):
        AppConfigLoader(cfg_file).load()


@pytest.mark.unit
def test_missing_ui_section_raises(tmp_path: Path) -> None:
    """Config without 'ui' key raises KeyError."""

    data = {k: v for k, v in _VALID_CONFIG.items() if k != "ui"}
    cfg_file = tmp_path / "app_config.json"
    cfg_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(KeyError):
        AppConfigLoader(cfg_file).load()


@pytest.mark.unit
def test_missing_analysis_section_raises(tmp_path: Path) -> None:
    """Config without 'analysis' key raises KeyError."""

    data = {k: v for k, v in _VALID_CONFIG.items() if k != "analysis"}
    cfg_file = tmp_path / "app_config.json"
    cfg_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(KeyError):
        AppConfigLoader(cfg_file).load()
