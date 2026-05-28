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


from dataclasses import dataclass
import tkinter as tk
from tkinter.ttk import Frame, Button, Style
from tkinter import messagebox
from typing import Callable, List

from work.library.config import Config
from work.scripts.gui.services.ui_settings import UISettings
from work.scripts.gui.services.translator import Translator
from work.scripts.gui.constants import ScaleTokensNames
from work.scripts.gui.constants import resolve_ui_scale, LANGUAGES
from work.scripts.gui.theme import ThemeName
from work.scripts.gui.views.font_selector_popup import FontSelectorPopup


@dataclass(frozen=True)
class RadioItem:
    """
    Radio button menu item configuration.

    Attributes
    ----------
    label : str
        Display label shown in the menu.

    value : str
        Internal value associated with the menu item.

    command : Callable[[], None]
        Callback executed when the item is selected.
    """

    label: str
    value: str
    command: Callable[[], None]


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
        """
        Initialize settings menu and bind it to application state.

        The constructor initializes internal state variables, creates
        Tkinter StringVar bindings for reactive menu updates, constructs
        the root menu widget, and builds all menu sections.

        Parameters
        ----------
        parent : Frame
            Parent Tkinter frame used as menu anchor.

        ui_settings : UISettings
            UI settings controller used to apply changes.

        translator : Translator
            Translation provider for localized labels.

        config : Config
            Application configuration instance used for initial values.
        """

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
        """
        Build the complete settings menu structure.
        """

        self._build_language_menu()
        self._build_scale_menu()
        self._build_theme_menu()
        self._build_ttk_theme_menu()
        self._build_font_menu()
        self._build_reset_button()

    def _build_language_menu(self) -> None:
        """
        Build the language selection submenu.
        """

        language_menu = tk.Menu(master=self._menu, tearoff=False)

        items = [
            RadioItem(
                label=label,
                value=code,
                command=lambda lang=code: self.ui_settings.set_language(lang)
            )
            for code, label in LANGUAGES.items()
        ]

        self._build_radio_group(
            menu=language_menu,
            variable=self.language_var,
            items=items
        )

        language_menu_data = \
            self.translator.get_data().settings_menu.language_menu

        self._menu.add_cascade(
            label=language_menu_data.label,
            menu=language_menu
        )

    def _build_scale_menu(self) -> None:
        """
        Build the interface scale selection submenu.
        """

        scale_menu = tk.Menu(master=self._menu, tearoff=False)

        scale_menu_data = self.translator.get_data().settings_menu.scale_menu

        items = [
            RadioItem(
                label=scale_menu_data.small_label,
                value=ScaleTokensNames.SMALL,
                command=lambda: self.ui_settings.set_scale(
                    ScaleTokensNames.SMALL
                )
            ),
            RadioItem(
                label=scale_menu_data.medium_label,
                value=ScaleTokensNames.MEDIUM,
                command=lambda: self.ui_settings.set_scale(
                    ScaleTokensNames.MEDIUM
                )
            ),
            RadioItem(
                label=scale_menu_data.big_label,
                value=ScaleTokensNames.BIG,
                command=lambda: self.ui_settings.set_scale(
                    ScaleTokensNames.BIG
                )
            ),
            RadioItem(
                label=scale_menu_data.very_big_label,
                value=ScaleTokensNames.VERY_BIG,
                command=lambda: self.ui_settings.set_scale(
                    ScaleTokensNames.VERY_BIG
                )
            ),
        ]

        self._build_radio_group(
            menu=scale_menu,
            variable=self.scale_var,
            items=items
        )

        self._menu.add_cascade(
            label=scale_menu_data.label,
            menu=scale_menu
        )

    def _build_theme_menu(self) -> None:
        """
        Build the application theme selection submenu.
        """

        theme_menu = tk.Menu(master=self._menu, tearoff=False)

        theme_menu_data = self.translator.get_data().settings_menu.theme_menu

        items = [
            RadioItem(
                label=theme_menu_data.light_label,
                value=ThemeName.LIGHT,
                command=lambda: self.ui_settings.set_theme(ThemeName.LIGHT)
            ),
            RadioItem(
                label=theme_menu_data.dark_label,
                value=ThemeName.DARK,
                command=lambda: self.ui_settings.set_theme(ThemeName.DARK)
            ),
        ]

        self._build_radio_group(
            menu=theme_menu,
            variable=self.theme_var,
            items=items
        )

        self._menu.add_cascade(
            label=theme_menu_data.label,
            menu=theme_menu
        )

    def _build_ttk_theme_menu(self) -> None:
        """
        Build the ttk theme selection submenu.
        """

        ttk_theme_menu = tk.Menu(master=self._menu, tearoff=False)

        ttk_theme_menu_data = \
            self.translator.get_data().settings_menu.ttk_theme_menu

        available_themes = Style().theme_names()

        items = [
            RadioItem(
                label=theme,
                value=theme,
                command=lambda t=theme: self.ui_settings.set_ttk_theme(t)
            )
            for theme in available_themes
        ]

        self._build_radio_group(
            menu=ttk_theme_menu,
            variable=self.ttk_theme_var,
            items=items
        )

        self._menu.add_cascade(
            label=ttk_theme_menu_data.label,
            menu=ttk_theme_menu
        )

    def _build_font_menu(self) -> None:
        """
        Build the font settings submenu.
        """

        font_menu = tk.Menu(master=self._menu, tearoff=False)

        self._apply_menu_style(menu=font_menu)

        font_menu_data = self.translator.get_data().settings_menu.font_menu

        font_menu.add_command(
            label=font_menu_data.command_label,
            command=self._open_font_selector
        )

        self._menu.add_cascade(label=font_menu_data.label, menu=font_menu)

    def _build_reset_button(self) -> None:
        """
        Build the settings reset command.
        """

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
        """
        Reset interface settings after user confirmation.
        """

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
        """
        Open the font selection popup window.
        """

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

    def _build_radio_group(
        self,
        menu: tk.Menu,
        variable: tk.StringVar,
        items: List[RadioItem]
    ) -> None:
        """
        Build a radio button group inside a menu.

        Parameters
        ----------
        menu : tk.Menu
            Target menu widget.

        variable : tk.StringVar
            Tkinter variable bound to the radio group.

        items : List[RadioItem]
            Radio button configuration items.
        """

        self._apply_menu_style(menu=menu)

        for item in items:
            menu.add_radiobutton(
                label=item.label,
                variable=variable,
                value=item.value,
                command=item.command,
            )

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

        ui = self.config.user.ui
        scale = resolve_ui_scale(ui.scale)

        menu.configure(
            font=(ui.font_family, scale.font_size),
        )

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
