"""Application configuration loader and typed config models.

This module reads the JSON application configuration file, validates its
structure through dataclasses, and converts raw JSON data into typed objects
used by the GUI and analysis layers.
"""


from pathlib import Path
import json
from typing import Any
from dataclasses import dataclass


# =========================
# CONFIG MODELS
# =========================

@dataclass(frozen=True)
class Paths:
    """File system paths used by the application.

    Attributes
    ----------
    data_dir : str
        Path to the input data directory.
    output_dir : str
        Path to the directory for text reports and exported tables.
    graphics_dir : str
        Path to the directory for generated figures.
    logs_dir : str
        Path to the directory for log files.
    """

    data_dir: str
    output_dir: str
    graphics_dir: str
    logs_dir: str


@dataclass(frozen=True)
class UI:
    """User interface settings.

    Attributes
    ----------
    language : str
        Interface language code.
    theme : str
        Visual theme name.
    window_width : int
        Main window width in pixels.
    window_height : int
        Main window height in pixels.
    """

    language: str
    theme: str
    window_width: int
    window_height: int


@dataclass(frozen=True)
class Reports:
    """Default report export settings.

    Attributes
    ----------
    default_export_format : str
        Default format for text report export.
    default_chart_format : str
        Default format for chart export.
    """

    default_export_format: str
    default_chart_format: str


@dataclass(frozen=True)
class Analysis:
    """Analysis parameter settings.

    Attributes
    ----------
    sma_windows : tuple[int, int]
        Window sizes for simple moving averages.
    ema_windows : tuple[int, int]
        Window sizes for exponential moving averages.
    volatility_window : int
        Rolling window size used for volatility calculation.
    forecast_horizon : int
        Number of future steps used in forecasting.
    """

    sma_windows: tuple[int, int]
    ema_windows: tuple[int, int]
    volatility_window: int
    forecast_horizon: int


@dataclass(frozen=True)
class AppConfig:
    """Complete application configuration.

    Attributes
    ----------
    paths : Paths
        File system paths used by the application.
    ui : UI
        Interface-related settings.
    reports : Reports
        Default export settings for reports and figures.
    analysis : Analysis
        Parameters used in statistical analysis and forecasting.
    """

    paths: Paths
    ui: UI
    reports: Reports
    analysis: Analysis


# =========================
# LOADER
# =========================

class AppConfigLoader:
    """Load and build the application configuration from JSON.

    Parameters
    ----------
    config_path : str | Path | None, optional
        Path to the configuration JSON file. If None, the default file in
        the project configuration directory is used.
    """

    def __init__(self, config_path: str | Path | None = None):
        """Initialize the configuration loader.

        Parameters
        ----------
        config_path : str | Path | None, optional
            Path to the configuration JSON file. If omitted, the default
            project configuration file is used.
        """

        if config_path is None:
            project_root = Path(__file__).resolve().parents[3]
            config_path = project_root / "work" / "config" / "app_config.json"

        self.config_path = Path(config_path)

    def load(self) -> AppConfig:
        """Load the application configuration.

        Returns
        -------
        AppConfig
            Parsed and typed application configuration.
        """

        raw = self._load_json()
        return self._build_config(raw)

    def _load_json(self) -> dict[str, Any]:
        """Read and parse the configuration JSON file.

        Returns
        -------
        dict[str, Any]
            Raw configuration data loaded from JSON.

        Raises
        ------
        FileNotFoundError
            If the configuration file does not exist.
        json.JSONDecodeError
            If the file contains invalid JSON.
        """

        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _build_config(self, raw: dict[str, Any]) -> AppConfig:
        """Convert raw JSON data into a typed application configuration.

        Parameters
        ----------
        raw : dict[str, Any]
            Raw configuration data loaded from JSON.

        Returns
        -------
        AppConfig
            Typed application configuration object.
        """

        return AppConfig(
            paths=Paths(**raw["paths"]),
            ui=UI(**raw["ui"]),
            reports=Reports(**raw["reports"]),
            analysis=Analysis(
                sma_windows=tuple(raw["analysis"]["sma_windows"]),
                ema_windows=tuple(raw["analysis"]["ema_windows"]),
                volatility_window=raw["analysis"]["volatility_window"],
                forecast_horizon=raw["analysis"]["forecast_horizon"],
            ),
        )
