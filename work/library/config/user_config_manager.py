"""
User configuration manager and typed user configuration models.

This module provides:
- immutable user configuration models;
- GUI preference persistence;
- automatic loading of default user settings;
- serialization and restoration of interface state.

The configuration system stores user-specific interface
preferences such as themes, language, fonts, scaling,
and window geometry.
"""


from dataclasses import (
    dataclass,
    asdict
)
from pathlib import Path
from typing import (
    Any,
    Dict,
    Optional,
    Union
)

from work.library.utils import (
    load,
    save
)


@dataclass(slots=True)
class UI:
    """
    User interface settings.

    Attributes
    ----------
    language : str
        Interface language code.

    theme : str
        Application theme identifier.

    window_width : int
        Main window width in pixels.

    window_height : int
        Main window height in pixels.

    window_x : int
        Horizontal window screen position.

    window_y : int
        Vertical window screen position.

    maximized : bool
        Whether the main window starts maximized.

    font_family : str
        Default interface font family.

    scale : str
        Interface scaling factor.

    ttk_theme : str
        ttk widget theme name.
    """

    language: str
    theme: str

    window_width: int
    window_height: int

    window_x: int
    window_y: int

    maximized: bool

    font_family: str
    scale: str
    ttk_theme: str


@dataclass(slots=True)
class UserConfig:
    """
    Complete typed user configuration.

    Attributes
    ----------
    ui : UI
        User interface settings and preferences.
    """

    ui: UI


class UserConfigManager:
    """
    Load, validate, and persist user configuration files.

    The loader converts raw JSON configuration data into
    strongly typed dataclass objects used by the GUI layer.

    Parameters
    ----------
    config_path : Optional[Union[str, Path]], optional
        Path to the main user configuration file.

    default_path : Optional[Union[str, Path]], optional
        Path to the default fallback configuration file.
    """

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        default_path: Optional[Union[str, Path]] = None
    ) -> None:
        """
        Initialize the user configuration loader.

        Parameters
        ----------
        config_path : Optional[Union[str, Path]], optional
            Path to the user configuration JSON file.

        default_path : Optional[Union[str, Path]], optional
            Path to the default user configuration JSON file.
        """

        project_root = Path(__file__).resolve().parents[3]

        if config_path is None:
            config_path = (
                project_root
                / "work"
                / "config"
                / "user_config.json"
            )

        if default_path is None:
            default_path = (
                project_root
                / "work"
                / "config"
                / "default_user_config.json"
            )

        self.config_path = Path(config_path)
        self.default_path = Path(default_path)
        self.config: Optional[UserConfig] = None

    def load(self) -> UserConfig:
        """
        Load the user configuration.

        If the main user configuration file does not exist,
        the default configuration is loaded instead.

        Returns
        -------
        UserConfig
            Parsed typed user configuration.
        """

        raw = self._load_raw_or_default()

        config = self._build_config(raw)
        self.config = config

        if not self.config_path.exists():
            self.save(config)

        return config

    def save(self, config: Optional[UserConfig] = None) -> None:
        """
        Save the user configuration to disk.

        Parameters
        ----------
        config : Optional[UserConfig], optional
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

    def reset(self) -> UserConfig:
        """
        Restore the default user configuration.

        Returns
        -------
        UserConfig
            Restored default user configuration.
        """

        raw = load(self.default_path)
        config = self._build_config(raw)

        self.config = config
        self.save(config)

        return config

    def _build_config(self, raw: Dict[str, Any]) -> UserConfig:
        """
        Build typed configuration objects from raw JSON data.

        Parameters
        ----------
        raw : Dict[str, Any]
            Raw configuration dictionary loaded from JSON.

        Returns
        -------
        UserConfig
            Fully typed user configuration object.
        """

        return UserConfig(
            ui=UI(**raw["ui"]),
        )

    def _load_raw_or_default(self) -> Dict[str, Any]:
        """
        Load raw configuration data from disk.

        The main user configuration file is preferred.
        If it does not exist, the default configuration
        file is loaded instead.

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
                f"Default user config not found: {self.default_path}"
            )

        return load(self.default_path)
