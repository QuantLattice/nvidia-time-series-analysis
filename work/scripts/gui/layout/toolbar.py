"""
Application toolbar component.

This module implements the top toolbar used to switch between
the main application sections such as data, analysis, and reports.
"""


from tkinter import ttk, Tk
from typing import Callable

from work.library.config import Config
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.services import Translator


class ToolBar(ttk.Frame):
    """
    Top toolbar with section-switching icon buttons.

    Parameters
    ----------
    parent : Tk
        Root application window.

    config : Config
        Application configuration object.

    ui_factory : UIFactory
        Factory used to create themed UI controls.

    on_click : Callable[[str], None]
        Callback invoked when a toolbar button is clicked.
        The selected section key is passed as an argument.

    translator : Translator
        Localization service used for tooltip text.
    """

    def __init__(
        self,
        parent: Tk,
        config: Config,
        ui_factory: UIFactory,
        on_click: Callable[[str], None],
        translator: Translator
    ) -> None:
        """
        Initialize the toolbar.

        Parameters
        ----------
        parent : Tk
            Root application window.

        config : Config
            Application configuration object.

        ui_factory : UIFactory
            Factory used to create themed UI controls.

        on_click : Callable[[str], None]
            Callback invoked when a toolbar button is clicked.

        translator : Translator
            Localization service used for tooltip text.
        """

        super().__init__(master=parent)

        self.config = config
        self.on_click = on_click
        self.ui_factory = ui_factory
        self.translator = translator

        self._build()

    def _build(self) -> None:
        """
        Build toolbar buttons.
        """

        toolbar = self.translator.get_data().tool_bar
        assets = self.config.app.assets

        items = {
            "data": (toolbar.data_button_tooltip, assets.data_icon),
            "analysis": (
                toolbar.analysis_button_tooltip,
                assets.analysis_icon
            ),
            "features": (
                toolbar.features_button_tooltip,
                assets.analysis_icon
            ),
            "reports": (toolbar.reports_button_tooltip, assets.reports_icon),
        }

        for key, (label, path) in items.items():
            button = self.ui_factory.icon_button(
                parent=self,
                icon_path=path,
                command=lambda section=key: self.on_click(section),
                tooltip=label,
            )
            button.pack(side="left")
