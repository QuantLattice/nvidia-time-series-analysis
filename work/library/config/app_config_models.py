"""
Typed dataclass models for application configuration.

This module defines all immutable configuration model classes
used by the application configuration system.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Tuple


@dataclass(slots=True)
class App:
    """
    General application metadata.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    title : str
        Main application window title.
    """

    title: str


@dataclass(slots=True)
class Paths:
    """
    File system paths used by the application.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    data_dir : str
        Path to the input dataset directory.
    output_dir : str
        Path to the directory for exported reports and tables.
    graphics_dir : str
        Path to the directory for generated charts and figures.
    logs_dir : str
        Path to the application log directory.
    """

    data_dir: str
    output_dir: str
    graphics_dir: str
    logs_dir: str


@dataclass(slots=True)
class Assets:
    """
    Graphical asset paths used by the GUI.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    app_icon : str
        Main application icon path.
    data_icon : str
        Icon used for data-related sections.
    analysis_icon : str
        Icon used for analysis sections.
    reports_icon : str
        Icon used for reporting sections.
    settings_icon : str
        Icon used for settings sections.
    display_icon : str
        Icon used for display and visualization sections.
    logo : str
        Application logo image path.
    """

    app_icon: str
    data_icon: str
    analysis_icon: str
    reports_icon: str
    settings_icon: str
    display_icon: str
    logo: str


@dataclass(slots=True)
class Reports:
    """
    Default report export settings.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    default_export_format : str
        Default format for text report export.
    default_chart_format : str
        Default format for chart export.
    """

    default_export_format: str
    default_chart_format: str


@dataclass(slots=True)
class Analysis:
    """
    Analysis parameter settings.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    sma_windows : Tuple[int, int]
        Window sizes for simple moving averages.
    ema_windows : Tuple[int, int]
        Window sizes for exponential moving averages.
    volatility_window : int
        Rolling window size used for volatility calculation.
    forecast_horizon : int
        Number of future steps used in forecasting.
    """

    sma_windows: Tuple[int, int]
    ema_windows: Tuple[int, int]
    volatility_window: int
    forecast_horizon: int


@dataclass(slots=True)
class AppConfig:
    """
    Complete typed application configuration.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    app : App
        General application metadata.
    paths : Paths
        File system path configuration.
    assets : Assets
        GUI asset configuration.
    reports : Reports
        Report export settings.
    analysis : Analysis
        Statistical analysis and forecasting parameters.
    """

    app: App
    paths: Paths
    assets: Assets
    reports: Reports
    analysis: Analysis
