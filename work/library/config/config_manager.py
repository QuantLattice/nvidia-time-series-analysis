"""Central configuration manager for the application.

This module combines environment-based database settings and JSON-based
application settings into a single typed configuration object.
"""


from dataclasses import dataclass
from pathlib import Path

from work.library.config.env_loader import EnvLoader, DBConfig
from work.library.config.app_config_loader import AppConfigLoader, AppConfig


@dataclass(frozen=True)
class Config:
    """Complete project configuration.

    Attributes
    ----------
    app : AppConfig
        Application settings loaded from the JSON configuration file.
    db : DBConfig
        Database connection settings loaded from environment variables.
    """

    app: AppConfig
    db: DBConfig


class ConfigManager:
    """Load and combine all project configuration sources.

    Parameters
    ----------
    env_path : str | None, optional
        Path to the .env file.
    app_config_path : str | Path | None, optional
        Path to the application configuration file.
    """

    def __init__(
        self,
        env_path: str | None = None,
        app_config_path: str | Path | None = None
    ):
        """Initialize configuration loaders.

        Parameters
        ----------
        env_path : str | None, optional
            Path to the .env file.
        app_config_path : str | Path | None, optional
            Path to the application configuration file.
        """

        self.env_loader = EnvLoader(env_path)
        self.app_config_loader = AppConfigLoader(app_config_path)

    def load(self) -> Config:
        """Load and return the full project configuration.

        Returns
        -------
        Config
            Combined application and database configuration.
        """

        return Config(
            app=self.app_config_loader.load(),
            db=self.env_loader.get_db_config()
        )
