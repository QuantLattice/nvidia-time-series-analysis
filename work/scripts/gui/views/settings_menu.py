"""
Settings menu for GUI interface customization.

This module provides a popup settings menu that allows the user to:
- change the application language;
- change interface scaling;
- switch between color themes;
- select ttk themes;
- open the font selector popup;
- reset interface settings to defaults.
"""


import tkinter as tk
from tkinter.ttk import Frame, Button
from tkinter import messagebox

from work.library.config import Config
from work.scripts.gui.services.ui_settings import UISettings
from work.scripts.gui.services.translator import Translator
from work.scripts.gui.constants import resolve_ui_scale
from work.scripts.gui.views.font_selector_popup import FontSelectorPopup
from work.scripts.gui.views.settings_menu_builders import (
    build_language_menu,
    build_scale_menu,
    build_theme_menu,
    build_ttk_theme_menu,
    build_font_menu,
)


class SettingsMenu:
    """
    Popup settings menu for GUI customization.

    Parameters
    ----------
    parent : Frame
        Parent container widget.

    ui_settings : UISettings
        Interface settings manager.

    translator : Translator
        Translation service used for localized menu labels.

    config : Config
        Application configuration object.
    """

    def __init__(
        self,
        parent: Frame,
        ui_settings: UISettings,
        translator: Translator,
        config: Config
    ) -> None:
        self.parent = parent
        self.config = config
        self.ui_settings = ui_settings
        self.translator = translator

        ui = self.config.user.ui

        self.language_var = tk.StringVar(value=ui.language)
        self.scale_var = tk.StringVar(value=ui.scale)
        self.theme_var = tk.StringVar(value=ui.theme)
        self.ttk_theme_var = tk.StringVar(value=ui.ttk_theme)

        self._menu = tk.Menu(
            master=self.parent,
            tearoff=False
        )

        self._apply_menu_style(menu=self._menu)

        self._build()

    # --------------------------------
    # BUILD
    # --------------------------------

    def _build(self) -> None:
        """Build the complete settings menu structure."""

        self._build_language_menu()
        self._build_scale_menu()
        self._build_theme_menu()
        self._build_ttk_theme_menu()
        self._build_font_menu()
        self._build_reset_button()

    def _build_language_menu(self) -> None:
        """Build the language selection submenu."""

        font = self._get_font()
        language_menu_data = \
            self.translator.get_data().settings_menu.language_menu

        language_menu = build_language_menu(
            parent_menu=self._menu,
            translator=self.translator,
            ui_settings=self.ui_settings,
            font=font,
            variable=self.language_var,
        )

        self._menu.add_cascade(
            label=language_menu_data.label,
            menu=language_menu
        )

    def _build_scale_menu(self) -> None:
        """Build the interface scale selection submenu."""

        font = self._get_font()
        scale_menu_data = \
            self.translator.get_data().settings_menu.scale_menu

        scale_menu = build_scale_menu(
            parent_menu=self._menu,
            translator=self.translator,
            ui_settings=self.ui_settings,
            font=font,
            variable=self.scale_var,
        )

        self._menu.add_cascade(
            label=scale_menu_data.label,
            menu=scale_menu
        )

    def _build_theme_menu(self) -> None:
        """Build the application theme selection submenu."""

        font = self._get_font()
        theme_menu_data = \
            self.translator.get_data().settings_menu.theme_menu

        theme_menu = build_theme_menu(
            parent_menu=self._menu,
            translator=self.translator,
            ui_settings=self.ui_settings,
            font=font,
            variable=self.theme_var,
        )

        self._menu.add_cascade(
            label=theme_menu_data.label,
            menu=theme_menu
        )

    def _build_ttk_theme_menu(self) -> None:
        """Build the ttk theme selection submenu."""

        font = self._get_font()
        ttk_theme_menu_data = \
            self.translator.get_data().settings_menu.ttk_theme_menu

        ttk_theme_menu = build_ttk_theme_menu(
            parent_menu=self._menu,
            ui_settings=self.ui_settings,
            font=font,
            variable=self.ttk_theme_var,
        )

        self._menu.add_cascade(
            label=ttk_theme_menu_data.label,
            menu=ttk_theme_menu
        )

    def _build_font_menu(self) -> None:
        """Build the font settings submenu."""

        font = self._get_font()
        font_menu_data = \
            self.translator.get_data().settings_menu.font_menu

        font_menu = build_font_menu(
            parent_menu=self._menu,
            translator=self.translator,
            ui_settings=self.ui_settings,
            font=font,
            open_selector_callback=self._open_font_selector,
        )

        self._menu.add_cascade(
            label=font_menu_data.label,
            menu=font_menu
        )

    def _build_reset_button(self) -> None:
        """Build the settings reset command."""

        self._menu.add_separator()

        reset_buttong_data = \
            self.translator.get_data().settings_menu.reset_button

        self._menu.add_command(
            label=reset_buttong_data.label,
            command=self._on_reset
        )

    # --------------------------------
    # ACTIONS
    # --------------------------------

    def _on_reset(self) -> None:
        """Reset interface settings after user confirmation."""

        reset_buttong_data = \
            self.translator.get_data().settings_menu.reset_button

        confirm = messagebox.askyesno(
            title=reset_buttong_data.title,
            message=reset_buttong_data.message
        )

        if not confirm:
            return

        self.ui_settings.reset()

    def _open_font_selector(self) -> None:
        """Open the font selection popup window."""

        anchor = getattr(self, "_anchor", self.parent)  # type: ignore
        anchor: Button

        FontSelectorPopup(
            parent=self.parent,
            anchor=anchor,
            ui_settings=self.ui_settings,
            current_font=self.config.user.ui.font_family,
            translator=self.translator,
            config=self.config
        )

    # --------------------------------
    # HELPERS
    # --------------------------------

    def _get_font(self) -> tuple:
        """Return the current UI font tuple ``(family, size)``."""

        ui = self.config.user.ui
        scale = resolve_ui_scale(ui.scale)
        return (ui.font_family, scale.font_size)

    def _apply_menu_style(
        self,
        menu: tk.Menu
    ) -> None:
        """
        Apply the current UI font settings to a menu.

        Parameters
        ----------
        menu : tk.Menu
            Target menu widget.
        """

        menu.configure(font=self._get_font())

    # --------------------------------
    # PUBLIC
    # --------------------------------

    def post_under(
        self,
        anchor: Button
    ) -> None:
        """
        Show the settings menu below the specified widget.

        Parameters
        ----------
        anchor : Button
            Anchor widget used for menu positioning.
        """

        self._anchor = anchor

        # Synchronize menu state with current configuration.
        self.language_var.set(self.config.user.ui.language)
        self.scale_var.set(self.config.user.ui.scale)
        self.theme_var.set(self.config.user.ui.theme)
        self.ttk_theme_var.set(self.config.user.ui.ttk_theme)

        x = anchor.winfo_rootx()
        y = anchor.winfo_rooty() + anchor.winfo_height()

        self._menu.post(x, y)
