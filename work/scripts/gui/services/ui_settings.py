"""
User interface settings service.

This module manages runtime GUI preferences such as:
- language;
- UI scale;
- font family;
- application theme;
- ttk theme.

The service also notifies subscribed components when settings change.
"""


from typing import Callable, List

from work.library.config import ConfigManager
from work.scripts.gui.theme import AppTheme
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.services import Translator


class UISettings():
    """
    Manage user interface preferences and notify subscribers on changes.

    Parameters
    ----------
    config_manager : ConfigManager
        Configuration manager used to persist user settings.

    app_theme : AppTheme
        Theme manager responsible for ttk and root styling.

    ui_factory : UIFactory
        Factory used to rebuild or refresh UI widgets.

    translator : Translator
        Translation loader for localized interface strings.
    """

    def __init__(
        self,
        config_manager: ConfigManager,
        app_theme: AppTheme,
        ui_factory: UIFactory,
        translator: Translator
    ) -> None:
        """
        Initialize the UI settings service.
        """

        self.config_manager = config_manager
        self.config = self.config_manager.config
        self.app_theme = app_theme
        self.ui_factory = ui_factory
        self.translator = translator

        self._subscribers: List[Callable[[], None]] = []

    def subscribe(
        self,
        callback: Callable[[], None]
    ) -> None:
        """
        Register a callback to be called after settings changes.

        Parameters
        ----------
        callback : Callable[[], None]
            Function executed when settings are updated.
        """

        self._subscribers.append(callback)

    def _notify(self) -> None:
        """
        Notify all subscribed listeners about a settings change.
        """

        for cb in self._subscribers:
            cb()

    def set_language(
        self,
        language: str
    ) -> None:
        """
        Update the application language.

        Parameters
        ----------
        language : str
            New language code.
        """

        self.config.user.ui.language = language
        self.translator.set_language(language)

        self._notify()

    def set_scale(
        self,
        scale: str
    ) -> None:
        """
        Update the application UI scale.

        Parameters
        ----------
        scale : str
            New scale preset name.
        """

        self.config.user.ui.scale = scale

        self.app_theme.set_scale(scale=scale)
        self.app_theme.update()

        self.ui_factory.set_scale(scale=scale)
        self.ui_factory.update()

        self._notify()

    def set_font(
        self,
        font: str
    ) -> None:
        """
        Update the application font family.

        Parameters
        ----------
        font : str
            New font family name.
        """

        self.config.user.ui.font_family = font

        self._notify()
        self.app_theme.update()

    def set_theme(
        self,
        theme: str
    ) -> None:
        """
        Update the application color theme.

        Parameters
        ----------
        theme : str
            New theme name.
        """

        self.config.user.ui.theme = theme

        self.app_theme.set_theme(theme_name=theme)
        self.app_theme.update()

        self.ui_factory.set_theme(theme_name=theme)
        self.ui_factory.update()

        self._notify()

    def set_ttk_theme(
        self,
        theme: str
    ) -> None:
        """
        Update the underlying ttk theme.

        Parameters
        ----------
        theme : str
            New ttk theme name.
        """

        self.config.user.ui.ttk_theme = theme
        self.app_theme.update()

        self._notify()

    def reset(self) -> None:
        """
        Restore UI settings from the default user configuration.
        """

        default_user_config = self.config_manager.reset_user_config()

        current = self.config.user.ui
        default = default_user_config.ui

        current.language = default.language
        current.theme = default.theme

        current.font_family = default.font_family
        current.scale = default.scale
        current.ttk_theme = default.ttk_theme

        self.translator.set_language(current.language)

        self.app_theme.set_theme(current.theme)
        self.app_theme.set_scale(current.scale)
        self.app_theme.update()

        self.ui_factory.set_theme(current.theme)
        self.ui_factory.set_scale(current.scale)
        self.ui_factory.update()

        self._notify()
