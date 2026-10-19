"""
Main application window composition.

Builds the top-level interface: menu bar, toolbar, context panel,
content area, and layout orchestration.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import tkinter as tk
from tkinter import ttk
import os
from typing import Dict, Optional

from work.scripts.core import AppState
from work.library.config import Config
from work.scripts.gui.services import (
    UISettings, Translator, DataDialogService, CSVResultHandler,
)
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.constants import MAIN_WINDOW_SIZE
from work.scripts.gui.layout import (
    LayoutManager, LayoutKey, LayoutRow,
    ToolBar, ContextPanel, MenuBar, ContentArea,
)
from work.scripts.controllers import (
    CSVController, StockQuoteController, ReportController,
)
from work.scripts.gui.main_window_handlers import MainWindowHandlersMixin
from work.scripts.gui.report_panel import build_report_panel


class MainWindow(MainWindowHandlersMixin):
    """
    Main application window controller.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
        stock_quote_controller: StockQuoteController,
        report_controller: ReportController,
    ) -> None:
        """Initialize and build the main application window."""
        self.root = root
        self.config = config
        self.app_state = app_state
        self.ui_factory = ui_factory
        self.ui_settings = ui_settings
        self.translator = translator
        self.csv_controller = csv_controller
        self.stock_quote_controller = stock_quote_controller
        self.report_controller = report_controller
        self.data_dialog = DataDialogService(
            root=root, translator=self.translator
        )
        self.csv_result_handler = CSVResultHandler()
        self._features_df = None
        self._configure_root()
        self._build_layout()
        self.ui_settings.subscribe(callback=self.rebuild)

    def _configure_root(self) -> None:
        """Configure the main Tkinter root window."""
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
        """Load and set the application window icon."""
        paths = self.config.app.paths
        assets = self.config.app.assets
        logo_path = os.path.join(paths.graphics_dir, assets.logo)
        self._logo_image = tk.PhotoImage(file=logo_path)
        self.root.iconphoto(True, self._logo_image)

    def _build_layout(self) -> None:
        """Create all top-level GUI components and assemble the layout."""
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
            translator=self.translator,
        )
        self.context_panel = ContextPanel(
            parent=self.root,
            ui_factory=self.ui_factory,
            app_state=self.app_state,
            on_import_csv=self._import_csv,
            on_export_csv=self._export_csv,
            on_run_analysis=self._on_run_analysis,
            on_generate_features=self._on_generate_features,
            on_plot_features=self._on_plot_features,
            on_delete_selected=self._on_delete_selected,
            on_delete_all=self._on_delete_all,
            translator=self.translator,
        )
        self._main_frame = ttk.Frame(self.root)
        self.content_area = ContentArea(parent=self._main_frame)
        self.content_area.set_loader(self._load_quotes_page)
        self.content_area.set_placeholder(text="MAIN CONTENT")
        self.content_area.grid(row=0, column=0, sticky="nsew")
        self._report_panel = ttk.Frame(self._main_frame, width=260)
        self._report_panel.grid(row=0, column=1, sticky="nsew")
        self._report_panel.grid_remove()          # hidden until first plot
        self._report_panel.grid_propagate(False)  # hold fixed width
        self._report_panel.rowconfigure(1, weight=1)
        self._report_panel.columnconfigure(0, weight=1)
        self._report_text: Optional[tk.Text] = None
        self._main_frame.columnconfigure(0, weight=1)
        self._main_frame.columnconfigure(1, weight=0)
        self._main_frame.rowconfigure(0, weight=1)
        self.layout = LayoutManager(root=self.root)
        self.layout.register(name=LayoutKey.MENU, widget=self.menu_bar)
        self.layout.register(name=LayoutKey.TOOLBAR, widget=self.toolbar)
        self.layout.register(
            name=LayoutKey.CONTEXT, widget=self.context_panel)
        self.layout.register(
            name=LayoutKey.CONTENT, widget=self._main_frame)
        self.layout.build(
            rows=[
                LayoutRow(name=LayoutKey.MENU),
                LayoutRow(name=LayoutKey.TOOLBAR),
                LayoutRow(name=LayoutKey.CONTEXT, visible=False),
                LayoutRow(
                    name=LayoutKey.CONTENT,
                    weight=1,
                    sticky="nsew",
                    separator=False,
                ),
            ]
        )

    def _load_quotes_page(
        self,
        page: int,
        page_size: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> Dict[str, object]:
        """Load a page of stock quotes from the controller."""
        return self.stock_quote_controller.get_quotes_page(
            page=page,
            page_size=page_size,
            sort_col=sort_col,
            sort_desc=sort_desc,
        )

    def _import_csv(self) -> None:
        """Open a file dialog and import the selected CSV into the DB."""
        path = self.data_dialog.ask_csv_to_import()
        if path is None:
            return
        result = self.csv_controller.import_csv(str(path))
        self.csv_result_handler.show_import_result(result, self.data_dialog)

    def _export_csv(self) -> None:
        """Open a save dialog and export all records to a CSV file."""
        path = self.data_dialog.ask_csv_to_export()
        if path is None:
            return
        result = self.csv_controller.export_csv(str(path))
        self.csv_result_handler.show_export_result(result, self.data_dialog)

    def _export_txt(self) -> None:
        """Open a save dialog and export the analytics report to TXT."""
        path = self.data_dialog.ask_txt_to_export()
        if path is None:
            return
        result = self.report_controller.export_txt(str(path))
        if result["success"]:
            self.data_dialog.show_info(
                title="Export TXT", message=f"Report saved:\n{path}",
            )
        else:
            self.data_dialog.show_error(
                title="Export TXT — Error",
                message=result["error"] or "Unknown error",
            )

    def _get_db_date_range(self):
        """Return (min_date, max_date) of trade dates in the database."""
        result = self.stock_quote_controller.get_date_range()
        if result["success"] and result["data"]:
            return result["data"]["min_date"], result["data"]["max_date"]
        return None, None

    def on_section_click(self, section: str) -> None:
        """Handle toolbar section button click; toggle context panel."""
        ui_state = self.app_state.ui_state
        if ui_state.active_section == section:
            ui_state.active_section = None
            self.layout.hide(name=LayoutKey.CONTEXT)
            self.content_area.clear()
            self.content_area.set_placeholder("MAIN CONTENT")
            self._report_panel.grid_remove()
            return
        ui_state.active_section = section
        min_date, max_date = self._get_db_date_range()
        self.context_panel.render(
            section=section, min_date=min_date, max_date=max_date
        )
        self.layout.show(name=LayoutKey.CONTEXT)
        self._render_content(section)

    def _render_content(self, section: str) -> None:
        """Render the main content area for the given section."""
        self._report_panel.grid_remove()
        if section == "data":
            self._render_data_content()
        elif section == "analysis":
            self.content_area.set_placeholder(
                "Select date range and chart type, then click Plot."
            )
        elif section == "features":
            self.content_area.set_placeholder(
                "Select a generator and date range, then click Generate."
            )

    def _render_data_content(self) -> None:
        """Configure the content area to display the data table."""
        self.content_area.set_loader(
            self.stock_quote_controller.get_quotes_page
        )
        self.content_area.show_quotes(page=1, page_size=100)

    def _show_report_panel(self, stats_text: str) -> None:
        """Populate and reveal the right-side report panel."""
        build_report_panel(self._report_panel, stats_text, self._export_txt)
        self._report_panel.grid()

    def toggle_panels(self) -> None:
        """Toggle visibility of toolbar and context panel."""
        ui_state = self.app_state.ui_state
        ui_state.panels_visible = not ui_state.panels_visible
        if ui_state.panels_visible:
            self.layout.show(name=LayoutKey.TOOLBAR)
            if ui_state.active_section is not None:
                self.context_panel.render(
                    section=ui_state.active_section)
                self.layout.show(name=LayoutKey.CONTEXT)
            else:
                self.layout.hide(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)

    def rebuild(self):
        """Rebuild the main window after UI settings changes."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_layout()
        self._restore_ui_state()

    def _restore_ui_state(self) -> None:
        """Restore layout visibility after a rebuild."""
        ui_state = self.app_state.ui_state
        if not ui_state.panels_visible:
            self.layout.hide(name=LayoutKey.TOOLBAR)
            self.layout.hide(name=LayoutKey.CONTEXT)
            return
        self.layout.show(name=LayoutKey.TOOLBAR)
        if ui_state.active_section is not None:
            min_date, max_date = self._get_db_date_range()
            self.context_panel.render(
                section=ui_state.active_section,
                min_date=min_date,
                max_date=max_date,
            )
            self.layout.show(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.CONTEXT)
