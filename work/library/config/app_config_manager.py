"""
Application configuration manager and typed configuration models.

This module provides:
- immutable dataclass-based configuration models;
- JSON configuration loading utilities;
- automatic fallback to default configuration files;
- serialization and persistence of application settings.

The configuration system is used by GUI, analysis, reporting,
and infrastructure layers of the application.
"""


from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Union
)
from dataclasses import (
    dataclass,
    asdict
)

from work.library.utils import (
    load,
    save
)


@dataclass(slots=True)
class App:
    """
    General application metadata.

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
    """Analysis parameter settings.

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


class AppConfigManager:
    """
    Load, validate, and persist application configuration files.

    The loader reads JSON configuration files and converts raw
    dictionary data into immutable typed dataclass objects.

    Parameters
    ----------
    config_path : Optional[Union[str, Path]], optional
        Path to the main application configuration file.

    default_path : Optional[Union[str, Path]], optional
        Path to the fallback default configuration file.
    """

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        default_path: Optional[Union[str, Path]] = None
    ) -> None:
        """
        Initialize the application configuration loader.

        Parameters
        ----------
        config_path : Optional[Union[str, Path]], optional
            Path to the user application configuration file.

        default_path : Optional[Union[str, Path]], optional
            Path to the default fallback configuration file.
        """

        project_root = Path(__file__).resolve().parents[3]

        if config_path is None:
            config_path = (
                project_root
                / "work"
                / "config"
                / "app_config.json"
            )
        if default_path is None:
            default_path = (
                project_root
                / "work"
                / "config"
                / "default_app_config.json"
            )

        self.config_path = Path(config_path)
        self.default_path = Path(default_path)
        self.config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """
        Load the application configuration.

        If the main configuration file does not exist,
        the default configuration is loaded instead.

        Returns
        -------
        AppConfig
            Parsed typed application configuration.
        """

        raw = self._load_raw_or_default()

        config = self._build_config(raw)
        self.config = config

        if not self.config_path.exists():
            self.save(config)

        return config

    def reset(self) -> AppConfig:
        """
        Reset the application configuration to default values.

        Returns
        -------
        AppConfig
            Restored default application configuration.
        """

        raw = load(self.default_path)

        config = self._build_config(raw)

        self.config = config
        self.save(config)

        return config

    def save(self, config: Optional[AppConfig] = None) -> None:
        """
        Save the application configuration to disk.

        Parameters
        ----------
        config : Optional[AppConfig], optional
            Configuration object to save. If omitted,
            the currently loaded configuration is used.

        Raises
        ------
        ValueError
            If no configuration is available for saving.
        """

        if config is None:
            if self.config is None:
                raise ValueError("No config loaded to save.")
            config = self.config

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        save(path=self.config_path, data=asdict(config))

        save(
            path=self.config_path,
            data=asdict(config)
        )

    def _build_config(self, raw: Dict[str, Any]) -> AppConfig:
        """
        Build typed configuration objects from raw JSON data.

        Parameters
        ----------
        raw : Dict[str, Any]
            Raw configuration dictionary loaded from JSON.

        Returns
        -------
        AppConfig
            Fully typed application configuration object.
        """

        return AppConfig(
            app=App(**raw["app"]),
            paths=Paths(**raw["paths"]),
            assets=Assets(**raw["assets"]),
            reports=Reports(**raw["reports"]),
            analysis=Analysis(
                sma_windows=tuple(raw["analysis"]["sma_windows"]),
                ema_windows=tuple(raw["analysis"]["ema_windows"]),
                volatility_window=raw["analysis"]["volatility_window"],
                forecast_horizon=raw["analysis"]["forecast_horizon"],
            ),
        )

    def _load_raw_or_default(self) -> Dict[str, Any]:
        """
        Load raw configuration data from disk.

        The main configuration file is preferred. If it does not
        exist, the default configuration file is loaded instead.

        Returns
        -------
        Dict[str, Any]
            Raw configuration dictionary.

        Raises
        ------
        FileNotFoundError
            If the default configuration file does not exist.
        """

        if self.config_path.exists():
            return load(self.config_path)

        if not self.default_path.exists():
            raise FileNotFoundError(
                f"Default app config not found: {self.default_path}"
            )

        return load(self.default_path)
