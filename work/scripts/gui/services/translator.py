"""
GUI translation loader.

This module loads localized JSON resources and converts them into
typed dataclass models for safe access by the GUI layer.
"""


from pathlib import Path
from typing import (
    Any,
    Dict,
    Union,
)

from work.library.utils import load
from work.scripts.gui.services.translation_keys import (
    ContextPanelKeys,
    CSVDataDialog,
    DataDialog,
    DataDialogResponse,
    FontSelectorPopupKeys,
    FontMenuKeys,
    LanguageMenuKeys,
    MenuBarKeys,
    ResetButtonKeys,
    ScaleMenuKeys,
    SettingsMenuKeys,
    ThemeMenuKeys,
    TkinterThemeMenuKeys,
    ToolBarKeys,
    TranslationKeys,
)


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
