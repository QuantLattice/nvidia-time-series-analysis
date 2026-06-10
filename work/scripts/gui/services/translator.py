"""
GUI translation loader.

This module loads localized JSON resources and converts them into
typed dataclass models for safe access by the GUI layer.
"""


from dataclasses import dataclass
from pathlib import Path
from typing import (
    Any,
    Dict,
    Union,
    Iterable,
    Tuple,
    List,
)

from work.library.utils import load


@dataclass(slots=True)
class MenuBarKeys:
    """
    Localized strings for the main menu bar.

    Attributes
    ----------
    file_button_text : str
        Text for the File menu button.
    help_button_text : str
        Text for the Help menu button.
    settings_button_tooltip : str
        Tooltip text for the Settings menu button.
    display_button_tooltip : str
        Tooltip text for the Display menu button.
    """

    file_button_text: str
    help_button_text: str
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
    reports_button_tooltip : str
        Tooltip text for the Reports toolbar button.
    """

    data_button_tooltip: str
    analysis_button_tooltip: str
    features_button_tooltip: str
    reports_button_tooltip: str


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


class Translator():
    """
    Load GUI translation resources from JSON files.

    Parameters
    ----------
    base_path : Union[str, Path]
        Directory containing translation JSON files.

    language : str
        Language code used to resolve the translation file.
    """

    def __init__(
        self,
        base_path: Union[str, Path],
        language: str
    ) -> None:
        """
        Initialize the translator and load the selected language.

        Parameters
        ----------
        base_path : Union[str, Path]
            Directory containing translation JSON files.

        language : str
            Language code used to resolve the translation file.
        """

        self.base_path = Path(base_path)
        self.language = language
        self.set_language(language=self.language)

    def load(self) -> TranslationKeys:
        path = self.base_path / f"{self.language}.json"

        json_data = load(path)

        return TranslationKeys(
            menu_bar=MenuBarKeys(**json_data["menu_bar"]),
            tool_bar=ToolBarKeys(**json_data["toolbar"]),
            settings_menu=SettingsMenuKeys(
                language_menu=LanguageMenuKeys(
                    **json_data["settings_menu"]["language_menu"]
                ),
                scale_menu=ScaleMenuKeys(
                    **json_data["settings_menu"]["scale_menu"]
                ),
                theme_menu=ThemeMenuKeys(
                    **json_data["settings_menu"]["theme_menu"]
                ),
                ttk_theme_menu=TkinterThemeMenuKeys(
                    **json_data["settings_menu"]["ttk_theme_menu"]
                ),
                font_menu=FontMenuKeys(
                    **json_data["settings_menu"]["font_menu"]
                ),
                reset_button=ResetButtonKeys(
                    **json_data["settings_menu"]["reset_button"]
                )
            ),
            font_selector_popup=FontSelectorPopupKeys(
                **json_data["font_selector_popup"]
            ),
            csv_data_dialog=self._create_csv_data_dialog(
                json_data=json_data
            ),
            context_panel=ContextPanelKeys(
                **json_data["context_panel"]
            )
        )

    def _create_csv_data_dialog(
        self,
        json_data: Dict[Any, Any]
    ) -> CSVDataDialog:
        csv_data = json_data["csv_data_dialog"]

        import_data = csv_data["import_data"]
        export_data = csv_data["export_data"]

        return CSVDataDialog(
            import_data=DataDialog(
                title=import_data["title"],
                filetypes=import_data["filetypes"],
                success=DataDialogResponse(
                    **import_data["success"]
                ),
                error=DataDialogResponse(
                    **import_data["error"]
                )
            ),
            rows_imported_message=csv_data["rows_imported_message"],
            date_range_message=csv_data["date_range_message"],
            export_data=DataDialog(
                title=export_data["title"],
                filetypes=export_data["filetypes"],
                success=DataDialogResponse(
                    **export_data["success"]
                ),
                error=DataDialogResponse(
                    **export_data["error"]
                )
            ),
            file_message=csv_data["file_message"],
            rows_exported_message=csv_data["rows_exported_message"],
            unknown_error_message=csv_data["unknown_error_message"]
        )

    def set_language(
        self,
        language: str
    ) -> None:
        """
        Change the active language and reload translations.

        Parameters
        ----------
        language : str
            New language code.
        """

        self.language = language
        self.data = self.load()

    def get_data(self) -> TranslationKeys:
        """
        Return the currently loaded translation data.

        Returns
        -------
        TranslationKeys
            Loaded translation model.
        """

        return self.data
