"""Typed dataclass models for GUI translation keys.

This module contains all dataclass definitions that map localized
JSON resources to structured Python objects for safe access by
the GUI layer.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import (
    Iterable,
    List,
    Tuple,
    Union,
)


@dataclass(slots=True)
class MenuBarKeys:
    file_button_text: str
    settings_button_tooltip: str
    display_button_tooltip: str
    import_button_label: str
    export_button_label: str


@dataclass(slots=True)
class ToolBarKeys:
    """
    Localized strings for the main toolbar.

    Attributes
    ----------
    data_button_tooltip : str
        Tooltip text for the Data toolbar button.
    analysis_button_tooltip : str
        Tooltip text for the Analysis toolbar button.
    features_button_tooltip : str
        Tooltip text for the Features toolbar button.
    """

    data_button_tooltip: str
    analysis_button_tooltip: str
    features_button_tooltip: str


@dataclass(slots=True)
class MenuBaseKeys:
    """
    Base localization model for menu sections.

    Attributes
    ----------
    label : str
        Visible label of the menu section.
    """

    label: str


@dataclass(slots=True)
class LanguageMenuKeys(MenuBaseKeys):
    """Localized strings for the language menu."""

    pass


@dataclass(slots=True)
class ScaleMenuKeys(MenuBaseKeys):
    """
    Localized strings for the UI scale menu.

    Attributes
    ----------
    small_label : str
        Label for the small scale preset.
    medium_label : str
        Label for the medium scale preset.
    big_label : str
        Label for the large scale preset.
    very_big_label : str
        Label for the extra-large scale preset.
    """

    small_label: str
    medium_label: str
    big_label: str
    very_big_label: str


@dataclass(slots=True)
class ThemeMenuKeys(MenuBaseKeys):
    """
    Localized strings for the application theme menu.

    Attributes
    ----------
    light_label : str
        Label for the light theme option.
    dark_label : str
        Label for the dark theme option.
    """

    light_label: str
    dark_label: str


@dataclass(slots=True)
class TkinterThemeMenuKeys(MenuBaseKeys):
    """Localized strings for the ttk theme menu."""

    pass


@dataclass(slots=True)
class FontMenuKeys(MenuBaseKeys):
    """
    Localized strings for the font menu.

    Attributes
    ----------
    command_label : str
        Label for the font selection command.
    """

    command_label: str


@dataclass(slots=True)
class ResetButtonKeys(MenuBaseKeys):
    """
    Localized strings for the reset action.

    Attributes
    ----------
    title : str
        Dialog title for the reset confirmation window.
    message : str
        Confirmation message shown to the user.
    """

    title: str
    message: str


@dataclass(slots=True)
class SettingsMenuKeys:
    """
    Localized strings for the settings menu.

    Attributes
    ----------
    language_menu : MenuBaseKeys
        Language submenu labels.
    scale_menu : ScaleMenuKeys
        UI scale submenu labels.
    theme_menu : ThemeMenuKeys
        Application theme submenu labels.
    ttk_theme_menu : TkinterThemeMenuKeys
        ttk theme submenu labels.
    font_menu : FontMenuKeys
        Font submenu labels.
    reset_button : ResetButtonKeys
        Reset action labels.
    """

    language_menu: MenuBaseKeys
    scale_menu: ScaleMenuKeys
    theme_menu: ThemeMenuKeys
    ttk_theme_menu: TkinterThemeMenuKeys
    font_menu: FontMenuKeys
    reset_button: ResetButtonKeys


@dataclass(slots=True)
class FontSelectorPopupKeys:
    """
    Localized strings for the font selector popup.

    Attributes
    ----------
    title : str
        Popup window title.
    example_text : str
        Preview text shown in the popup.
    apply_button_text : str
        Text for the apply button.
    """

    title: str
    example_text: str
    apply_button_text: str


@dataclass(slots=True)
class DataDialogResponse:
    title: str
    message: str


@dataclass(slots=True)
class DataDialog:
    title: str
    filetypes: Iterable[Tuple[str, Union[str, List[str], Tuple[str, ...]]]]
    success: DataDialogResponse
    error: DataDialogResponse


@dataclass(slots=True)
class CSVDataDialog:
    import_data: DataDialog
    rows_imported_message: str
    date_range_message: str

    export_data: DataDialog
    file_message: str
    rows_exported_message: str

    unknown_error_message: str


@dataclass(slots=True)
class ContextPanelKeys:
    import_csv_text: str
    export_csv_text: str


@dataclass(slots=True)
class TranslationKeys:
    """
    Complete set of localized GUI strings.

    Attributes
    ----------
    menu_bar : MenuBarKeys
        Main menu bar labels.
    tool_bar : ToolBarKeys
        Main toolbar tooltips.
    settings_menu : SettingsMenuKeys
        Settings menu labels.
    font_selector_popup : FontSelectorPopupKeys
        Font selector popup labels.
    """

    menu_bar: MenuBarKeys
    tool_bar: ToolBarKeys
    settings_menu: SettingsMenuKeys
    font_selector_popup: FontSelectorPopupKeys
    csv_data_dialog: CSVDataDialog
    context_panel: ContextPanelKeys
