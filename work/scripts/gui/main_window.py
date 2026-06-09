"""
Main application window composition.

This module builds the top-level interface, including the menu bar,
toolbar, context panel, content area, and layout orchestration.
"""


import tkinter as tk
import os
from typing import Dict

from work.scripts.core import AppState
from work.library.config import Config
from work.scripts.gui.services import (
    UISettings,
    Translator,
    DataDialogService,
    CSVResultHandler
)
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.constants import (
    MAIN_WINDOW_SIZE
)
from work.scripts.gui.layout import (
    LayoutManager,
    LayoutKey,
    LayoutRow,
    ToolBar,
    ContextPanel,
    MenuBar,
    ContentArea
)

from work.scripts.controllers import (
    CSVController,
    StockQuoteController
)


class MainWindow:
    """
    Main application window controller.

    Parameters
    ----------
    root : tk.Tk
        Root Tkinter application window.

    config : Config
        Application configuration object.

    app_state : AppState
        Shared runtime application state.

    ui_factory : UIFactory
        Factory used to create themed UI components.

    ui_settings : UISettings
        Runtime UI configuration manager.

    translator : Translator
        Localization service used for UI text.
    """

    def __init__(
        self,
        root: tk.Tk,
        config: Config,
        app_state: AppState,
        ui_factory: UIFactory,
        ui_settings: UISettings,
        translator: Translator,
        csv_controller: CSVController,
        stock_quote_controller: StockQuoteController
    ) -> None:
        """
        Initialize and build the main application window.

        Parameters
        ----------
        root : tk.Tk
            Root Tkinter application window.

        config : Config
            Application configuration object.

        app_state : AppState
            Shared runtime application state.

        ui_factory : UIFactory
            Factory used to create themed UI components.

        ui_settings : UISettings
            Runtime UI configuration manager.

        translator : Translator
            Localization service used for UI text.
        """

        self.root = root
        self.config = config
        self.app_state = app_state
        self.ui_factory = ui_factory
        self.ui_settings = ui_settings
        self.translator = translator
        self.csv_controller = csv_controller
        self.stock_quote_controller = stock_quote_controller

        self.data_dialog = DataDialogService(
            root=root,
            translator=self.translator
        )
        self.csv_result_handler = CSVResultHandler()

        self._configure_root()
        self._build_layout()

        self.ui_settings.subscribe(callback=self.rebuild)

    # ---------------------------
    # ROOT
    # ---------------------------

    def _configure_root(self) -> None:
        """
        Configure the main Tkinter root window.
        """

        self.root.title(self.config.app.app.title)

        ui = self.config.user.ui

        self.root.geometry(
            newGeometry=(
                f"{ui.window_width}x{ui.window_height}"
                f"+{ui.window_x}+{ui.window_y}"
            )
        )

        if ui.maximized:
            self.root.after(ms=0, func=lambda: self.root.state("zoomed"))

        self.root.minsize(*MAIN_WINDOW_SIZE)

        self._set_icon()

    def _set_icon(self) -> None:
        """
        Load and set the application window icon.
        """

        paths = self.config.app.paths
        assets = self.config.app.assets

        logo_path = os.path.join(paths.graphics_dir, assets.logo)
        self._logo_image = tk.PhotoImage(file=logo_path)
        self.root.iconphoto(True, self._logo_image)

    # ---------------------------
    # LAYOUT
    # ---------------------------

    def _build_layout(self) -> None:
        """
        Create all top-level GUI components and assemble the layout.
        """

        self.menu_bar = MenuBar(
            parent=self.root,
            config=self.config,
            ui_factory=self.ui_factory,
            on_toggle_panels=self.toggle_panels,
            on_import_csv=self._import_csv,
            on_export_csv=self._export_csv,
            translator=self.translator,
            ui_settings=self.ui_settings,
        )

        self.toolbar = ToolBar(
            parent=self.root,
            config=self.config,
            ui_factory=self.ui_factory,
            on_click=self.on_section_click,
            translator=self.translator
        )

        self.context_panel = ContextPanel(
            parent=self.root,
            ui_factory=self.ui_factory,
            app_state=self.app_state,
            on_import_csv=self._import_csv,
            on_export_csv=self._export_csv,
            translator=self.translator
        )

        self.content_area = ContentArea(parent=self.root)
        self.content_area.set_loader(self._load_quotes_page)
        self.content_area.set_placeholder(text="MAIN CONTENT")

        self.layout = LayoutManager(root=self.root)
        self.layout.register(name=LayoutKey.MENU, widget=self.menu_bar)
        self.layout.register(name=LayoutKey.TOOLBAR, widget=self.toolbar)
        self.layout.register(name=LayoutKey.CONTEXT, widget=self.context_panel)
        self.layout.register(name=LayoutKey.CONTENT, widget=self.content_area)

        self.layout.build(
            rows=[
                LayoutRow(name=LayoutKey.MENU),
                LayoutRow(name=LayoutKey.TOOLBAR),
                LayoutRow(
                    name=LayoutKey.CONTEXT,
                    visible=False
                ),
                LayoutRow(
                    name=LayoutKey.CONTENT,
                    weight=1,
                    sticky="nsew",
                    separator=False
                ),
            ]
        )

    # ---------------------------
    # LOGIC
    # ---------------------------

    def _load_quotes_page(
        self,
        page: int,
        page_size: int
    ) -> Dict[str, object]:
        return self.stock_quote_controller.get_quotes_page(
            page=page,
            page_size=page_size,
        )

    def _import_csv(self) -> None:
        path = self.data_dialog.ask_csv_to_import()
        if path is None:
            return

        result = self.csv_controller.import_csv(str(path))
        self.csv_result_handler.show_import_result(result, self.data_dialog)

    def _export_csv(self) -> None:
        path = self.data_dialog.ask_csv_to_export()
        if path is None:
            return

        result = self.csv_controller.export_csv(str(path))
        self.csv_result_handler.show_export_result(result, self.data_dialog)

    def on_section_click(
        self,
        section: str
    ) -> None:
        ui_state = self.app_state.ui_state

        if ui_state.active_section == section:
            ui_state.active_section = None

            self.layout.hide(name=LayoutKey.CONTEXT)

            self.content_area.clear()
            self.content_area.set_placeholder("MAIN CONTENT")

            return

        ui_state.active_section = section

        self.context_panel.render(section=section)

        self.layout.show(name=LayoutKey.CONTEXT)

        self._render_content(section)

    def _render_content(
        self,
        section: str
    ) -> None:

        if section == "data":
            self._render_data_content()

        elif section == "analysis":
            self.content_area.set_placeholder(
                "Analysis tools"
            )

        elif section == "reports":
            self.content_area.set_placeholder(
                "Reports"
            )

    def _render_data_content(self) -> None:
        self.content_area.set_loader(
            self.stock_quote_controller.get_quotes_page
        )

        self.content_area.show_quotes(
            page=1,
            page_size=100,
        )

    def toggle_panels(self) -> None:
        """
        Toggle visibility of toolbar and context panel.
        """

        ui_state = self.app_state.ui_state

        ui_state.panels_visible = not ui_state.panels_visible

        if ui_state.panels_visible:
            self.layout.show(name=LayoutKey.TOOLBAR)

            if ui_state.active_section is not None:
                self.context_panel.render(section=ui_state.active_section)
                self.layout.show(name=LayoutKey.CONTEXT)
            else:
                self.layout.hide(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)

    def rebuild(self):
        """
        Rebuild the main window after UI settings changes.

        The current widget tree is destroyed and recreated, then the
        runtime UI state is restored.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

        self._build_layout()
        self._restore_ui_state()

    def _restore_ui_state(self) -> None:
        """
        Restore layout visibility after a rebuild.
        """

        ui_state = self.app_state.ui_state

        if not ui_state.panels_visible:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)
            return

        self.layout.show(name=LayoutKey.TOOLBAR)

        if ui_state.active_section is not None:
            self.context_panel.render(section=ui_state.active_section)
            self.layout.show(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.CONTEXT)
