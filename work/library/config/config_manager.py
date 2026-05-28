"""
Centralized application configuration management utilities.

This module combines multiple configuration sources into a single
typed configuration object used throughout the application.

The configuration system integrates:
- application configuration loaded from JSON files;
- user interface configuration and preferences;
- database settings loaded from environment variables.
"""


from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from work.library.config.user_config_manager import (
    UserConfigManager,
    UserConfig
)
from work.library.config.app_config_manager import (
    AppConfigManager,
    AppConfig
)
from work.library.config.env_manager import (
    EnvManager,
    DBConfig
)


@dataclass(slots=True)
class Config:
    """
    Complete project configuration container.

    Attributes
    ----------
    app : AppConfig
        Application-level configuration settings.

    user : UserConfig
        User-specific interface and preference settings.

    db : DBConfig
        Database connection configuration loaded
        from environment variables.
    """

    app: AppConfig
    user: UserConfig
    db: DBConfig


class ConfigManager:
    """
    Load and manage all application configuration sources.

    The manager aggregates:
    - application configuration;
    - user interface configuration;
    - database environment settings.

    Parameters
    ----------
    app_config_path : Optional[Union[str, Path]], optional
        Path to the application configuration file.

    user_config_path : Optional[Union[str, Path]], optional
        Path to the user configuration file.

    env_path : Optional[Union[str, Path]], optional
        Path to the environment variable file.
    """

    def __init__(
        self,
        app_config_path: Optional[Union[str, Path]] = None,
        user_config_path: Optional[Union[str, Path]] = None,
        env_path: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize configuration managers and loaders.

        Parameters
        ----------
        app_config_path : Optional[Union[str, Path]], optional
            Path to the application configuration file.

        user_config_path : Optional[Union[str, Path]], optional
            Path to the user configuration file.

        env_path : Optional[Union[str, Path]], optional
            Path to the environment variable file.
        """

        self.app_config_loader = AppConfigManager(app_config_path)
        self.user_config_loader = UserConfigManager(user_config_path)
        self.env_loader = EnvManager(env_path)

    def load(self) -> Config:
        """
        Load and combine all configuration sources.

        Returns
        -------
        Config
            Fully initialized project configuration object.
        """

        self.config = Config(
            app=self.app_config_loader.load(),
            user=self.user_config_loader.load(),
            db=self.env_loader.get_db_config()
        )

        return self.config

    def save(self) -> None:
        """
        Persist all mutable configuration files to disk.

        Notes
        -----
        Environment configuration is not persisted because
        it is managed externally through environment variables.
        """

        self.app_config_loader.save()
        self.user_config_loader.save()

    def reset_user_config(self) -> UserConfig:
        """
        Restore the default user configuration.

        Returns
        -------
        UserConfig
            Restored default user configuration.

        Raises
        ------
        AttributeError
            If configuration has not been loaded yet.
        """

        self.config.user = self.user_config_loader.reset()
        return self.config.user

    def reset_app_config(self) -> AppConfig:
        """
        Restore the default application configuration.

        Returns
        -------
        AppConfig
            Restored default application configuration.

        Raises
        ------
        AttributeError
            If configuration has not been loaded yet.
        """

        self.config.app = self.app_config_loader.reset()
        return self.config.app
