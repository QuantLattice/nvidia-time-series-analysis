"""
Application bootstrap and lifecycle management.

This module creates the Tkinter root window, loads configuration,
initializes shared runtime state, themes, services, and the main
application window.
"""


import tkinter as tk

from work.config.constants import TRANSLATOR_BASE_PATH
from work.library.config import ConfigManager
from work.scripts.core import AppState
from work.scripts.gui.theme import AppTheme
from work.scripts.gui.services import (
    UIBinder,
    Translator,
    UISettings,
)
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.main_window import MainWindow

from work.scripts.db import Database
from work.scripts.services import (
    StockQuoteService,
    CSVService
)
from work.scripts.controllers import (
    CSVController,
    StockQuoteController,
    ReportController,
)


class App():
    """
    Top-level GUI application controller.

    Parameters
    ----------
    config_manager : ConfigManager
        Configuration manager used to load and persist application settings.
    """

    def __init__(
        self,
        config_manager: ConfigManager
    ) -> None:
        """
        Initialize the application and all shared GUI subsystems.

        Parameters
        ----------
        config_manager : ConfigManager
            Configuration manager used to load and
            persist application settings.
        """

        self.config_manager = config_manager
        self.config = self.config_manager.load()

        self.root = tk.Tk()
        self.root.protocol(
            name="WM_DELETE_WINDOW",
            func=self._on_close
        )

        self.app_state = AppState()

        self.app_theme = AppTheme(
            root=self.root,
            config=self.config
        )

        self.ui_binder = UIBinder(
            app_state=self.app_state
        )

        self.ui_factory = UIFactory(
            config=self.config,
            ui_binder=self.ui_binder
        )

        self.translator = Translator(
            base_path=TRANSLATOR_BASE_PATH,
            language=self.config.user.ui.language
        )

        self.ui_settings = UISettings(
            config_manager=self.config_manager,
            app_theme=self.app_theme,
            ui_factory=self.ui_factory,
            translator=self.translator
        )

        self.db = Database()
        self.stock_quote_service = StockQuoteService(db=self.db)
        self.stock_quote_controller = StockQuoteController(
            service=self.stock_quote_service
        )
        self.csv_service = CSVService(stock_service=self.stock_quote_service)
        self.csv_controller = CSVController(service=self.csv_service)
        self.report_controller = ReportController(service=self.stock_quote_service)

        self.main_window = MainWindow(
            root=self.root,
            config=self.config,
            app_state=self.app_state,
            ui_factory=self.ui_factory,
            ui_settings=self.ui_settings,
            translator=self.translator,
            csv_controller=self.csv_controller,
            stock_quote_controller=self.stock_quote_controller,
            report_controller=self.report_controller,
        )

    def _on_close(self):
        """
        Handle application shutdown.

        Saves the current window state and geometry before closing
        the main window.
        """

        self.root.update_idletasks()

        state = self.root.state()

        ui = self.config.user.ui

        ui.maximized = (state == "zoomed")

        if state == "normal":
            geometry = self.root.geometry()
            size_part, pos_part = (
                geometry.split("+")[0],
                geometry.split("+")[1:]
            )

            width, height = map(int, size_part.split("x"))
            x, y = map(int, pos_part)

            ui.window_width = width
            ui.window_height = height
            ui.window_x = x
            ui.window_y = y

        self.config_manager.save()
        self.root.destroy()

    def run(self) -> None:
        """
        Start the Tkinter event loop.
        """

        self.root.mainloop()
