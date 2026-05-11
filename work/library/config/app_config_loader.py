"""Simple application configuration loader and typed models."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple


@dataclass(slots=True)
class Paths:
    data_dir: str
    output_dir: str
    graphics_dir: str
    logs_dir: str


@dataclass(slots=True)
class UI:
    language: str
    theme: str
    window_width: int
    window_height: int


@dataclass(slots=True)
class Reports:
    default_export_format: str
    default_chart_format: str


@dataclass(slots=True)
class Analysis:
    sma_windows: Tuple[int, int]
    ema_windows: Tuple[int, int]
    volatility_window: int
    forecast_horizon: int


@dataclass
class Assets:
    app_icon: str = ""
    data_icon: str = ""
    analysis_icon: str = ""
    reports_icon: str = ""
    settings_icon: str = ""
    display_icon: str = ""
    logo: str = ""


@dataclass
class AppConfig:
    paths: Paths
    ui: UI
    reports: Reports
    analysis: Analysis
    title: str = ""
    assets: Optional[Assets] = None


class AppConfigLoader:
    """Load and parse an application configuration JSON file.

    Parameters
    ----------
    config_path : str | Path
        Path to the JSON configuration file.
    """

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = Path(config_path)

    def load(self) -> AppConfig:
        """Parse the config file and return a typed AppConfig.

        Raises
        ------
        FileNotFoundError
            If the config file does not exist.
        json.JSONDecodeError
            If the file contains malformed JSON.
        KeyError
            If a required section is missing.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, encoding="utf-8") as f:
            raw = json.load(f)

        assets = None
        if "assets" in raw:
            assets = Assets(**raw["assets"])

        title = ""
        if "app" in raw:
            title = raw["app"].get("title", "")

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
            title=title,
            assets=assets,
        )
