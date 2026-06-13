"""
Application configuration manager.

This module provides utilities for loading, validating, and
persisting application configuration files.

The configuration system is used by GUI, analysis, reporting,
and infrastructure layers of the application.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
    Union
)
from dataclasses import asdict

from work.library.utils import (
    load,
    save
)
from work.library.config.app_config_models import (
    App,
    Paths,
    Assets,
    Reports,
    Analysis,
    AppConfig
)

__all__ = ['AppConfigManager', 'AppConfig']


class AppConfigManager:
    """
    Load, validate, and persist application configuration files.

    The loader reads JSON configuration files and converts raw
    dictionary data into immutable typed dataclass objects.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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
                volatility_window=(
                    raw["analysis"]["volatility_window"]
                ),
                forecast_horizon=(
                    raw["analysis"]["forecast_horizon"]
                ),
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
                f"Default app config not found: "
                f"{self.default_path}"
            )

        return load(self.default_path)
