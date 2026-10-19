"""
Builder functions for SettingsMenu submenus.

This module provides standalone builder functions that construct
Tkinter submenu widgets for the application settings menu.  Each
function creates a populated ``tk.Menu`` and returns it so the
caller can attach it to a parent menu via ``add_cascade``.

The ``RadioItem`` dataclass and ``_build_radio_group`` helper used
by every builder are also defined here.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
import tkinter as tk
from tkinter.ttk import Style
from typing import Callable, List, Tuple

from work.scripts.gui.services.ui_settings import UISettings
from work.scripts.gui.services.translator import Translator
from work.scripts.gui.constants import ScaleTokensNames, LANGUAGES
from work.scripts.gui.theme import ThemeName


@dataclass(frozen=True)
class RadioItem:
    """
    Radio button menu item configuration.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    label: str
    value: str
    command: Callable[[], None]


def _build_radio_group(
    menu: tk.Menu,
    variable: tk.StringVar,
    items: List[RadioItem],
    font: Tuple,
) -> None:
    """
    Build a radio button group inside a menu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    menu.configure(font=font)

    for item in items:
        menu.add_radiobutton(
            label=item.label,
            variable=variable,
            value=item.value,
            command=item.command,
        )


def build_language_menu(
    parent_menu: tk.Menu,
    translator: Translator,
    ui_settings: UISettings,
    font: Tuple,
    variable: tk.StringVar,
) -> tk.Menu:
    """
    Build and return the language selection submenu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    language_menu = tk.Menu(master=parent_menu, tearoff=False)

    items = [
        RadioItem(
            label=label,
            value=code,
            command=lambda lang=code: ui_settings.set_language(lang)
        )
        for code, label in LANGUAGES.items()
    ]

    _build_radio_group(
        menu=language_menu,
        variable=variable,
        items=items,
        font=font,
    )

    return language_menu


def build_scale_menu(
    parent_menu: tk.Menu,
    translator: Translator,
    ui_settings: UISettings,
    font: Tuple,
    variable: tk.StringVar,
) -> tk.Menu:
    """
    Build and return the interface scale selection submenu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    scale_menu = tk.Menu(master=parent_menu, tearoff=False)
    scale_menu_data = translator.get_data().settings_menu.scale_menu

    items = [
        RadioItem(
            label=scale_menu_data.small_label,
            value=ScaleTokensNames.SMALL,
            command=lambda: ui_settings.set_scale(
                ScaleTokensNames.SMALL
            )
        ),
        RadioItem(
            label=scale_menu_data.medium_label,
            value=ScaleTokensNames.MEDIUM,
            command=lambda: ui_settings.set_scale(
                ScaleTokensNames.MEDIUM
            )
        ),
        RadioItem(
            label=scale_menu_data.big_label,
            value=ScaleTokensNames.BIG,
            command=lambda: ui_settings.set_scale(
                ScaleTokensNames.BIG
            )
        ),
        RadioItem(
            label=scale_menu_data.very_big_label,
            value=ScaleTokensNames.VERY_BIG,
            command=lambda: ui_settings.set_scale(
                ScaleTokensNames.VERY_BIG
            )
        ),
    ]

    _build_radio_group(
        menu=scale_menu,
        variable=variable,
        items=items,
        font=font,
    )

    return scale_menu


def build_theme_menu(
    parent_menu: tk.Menu,
    translator: Translator,
    ui_settings: UISettings,
    font: Tuple,
    variable: tk.StringVar,
) -> tk.Menu:
    """
    Build and return the application theme selection submenu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    theme_menu = tk.Menu(master=parent_menu, tearoff=False)
    theme_menu_data = translator.get_data().settings_menu.theme_menu

    items = [
        RadioItem(
            label=theme_menu_data.light_label,
            value=ThemeName.LIGHT,
            command=lambda: ui_settings.set_theme(ThemeName.LIGHT)
        ),
        RadioItem(
            label=theme_menu_data.dark_label,
            value=ThemeName.DARK,
            command=lambda: ui_settings.set_theme(ThemeName.DARK)
        ),
    ]

    _build_radio_group(
        menu=theme_menu,
        variable=variable,
        items=items,
        font=font,
    )

    return theme_menu


def build_ttk_theme_menu(
    parent_menu: tk.Menu,
    ui_settings: UISettings,
    font: Tuple,
    variable: tk.StringVar,
) -> tk.Menu:
    """
    Build and return the ttk theme selection submenu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    ttk_theme_menu = tk.Menu(master=parent_menu, tearoff=False)
    available_themes = Style().theme_names()

    items = [
        RadioItem(
            label=theme,
            value=theme,
            command=lambda t=theme: ui_settings.set_ttk_theme(t)
        )
        for theme in available_themes
    ]

    _build_radio_group(
        menu=ttk_theme_menu,
        variable=variable,
        items=items,
        font=font,
    )

    return ttk_theme_menu


def build_font_menu(
    parent_menu: tk.Menu,
    translator: Translator,
    ui_settings: UISettings,
    font: Tuple,
    open_selector_callback: Callable[[], None],
) -> tk.Menu:
    """
    Build and return the font settings submenu.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    font_menu = tk.Menu(master=parent_menu, tearoff=False)
    font_menu.configure(font=font)

    font_menu_data = translator.get_data().settings_menu.font_menu

    font_menu.add_command(
        label=font_menu_data.command_label,
        command=open_selector_callback
    )

    return font_menu
