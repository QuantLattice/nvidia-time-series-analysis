"""
Main application window composition.

This module builds the top-level interface, including the menu bar,
toolbar, context panel, content area, and layout orchestration.
"""


import tkinter as tk
import os
import datetime
from datetime import date
from typing import Dict, List, Any

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
    StockQuoteController,
    ReportController,
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
        stock_quote_controller: StockQuoteController,
        report_controller: ReportController,
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

        report_controller : ReportController
            Controller for generating and exporting TXT reports.
        """

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
            on_run_analysis=self._on_run_analysis,
            on_export_txt=self._export_txt,
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

    def _export_txt(self) -> None:
        path = self.data_dialog.ask_txt_to_export()
        if path is None:
            return

        result = self.report_controller.export_txt(str(path))
        if result["success"]:
            self.data_dialog.show_info(
                title="Export TXT",
                message=f"Report saved:\n{path}",
            )
        else:
            self.data_dialog.show_error(
                title="Export TXT — Error",
                message=result["error"] or "Unknown error",
            )

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
                "Select date range and chart type, then click Plot."
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

    def _on_run_analysis(
        self,
        start_date: date,
        end_date: date,
        chart_type: str,
    ) -> None:
        """Fetch data, build the requested chart, and display it."""

        result = self.stock_quote_controller.get_quotes_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )

        if not result["success"]:
            self.content_area.set_placeholder(f"Error: {result['error']}")
            return

        quotes: List[Any] = result["data"]

        if not quotes:
            self.content_area.set_placeholder(
                "No data found for the selected date range."
            )
            return

        fig = self._build_figure(quotes, chart_type, start_date, end_date)
        self.content_area.show_chart(fig)

    def _build_figure(
        self,
        quotes: List[Any],
        chart_type: str,
        start_date: date,
        end_date: date,
    ):
        """Build a Matplotlib Figure from the given quotes and chart type."""

        from matplotlib.figure import Figure
        from work.library.plotting.rendering import MatplotlibRenderer
        from work.library.plotting.contracts import PlotContext, ChartConfig
        from work.library.plotting.stack import LayerStack
        from work.library.plotting.layers import (
            CandlestickLayer,
            LineLayer,
            ScatterLayer,
            BoxLayer,
            HistogramLayer,
        )
        from work.library.plotting.contracts import (
            LineStyle,
            ScatterStyle,
            BoxStyle,
            HistogramStyle,
        )

        # Convert trade_date strings/dates to datetime for matplotlib
        dates = [
            datetime.datetime.combine(
                datetime.date.fromisoformat(q["trade_date"])
                if isinstance(q["trade_date"], str)
                else q["trade_date"],
                datetime.time(),
            )
            for q in quotes
        ]
        closes = [q["close_price"] for q in quotes]

        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        context = PlotContext(figure=fig, primary_axes=ax)
        stack = LayerStack()

        if chart_type == "candlestick":
            opens = [q["open_price"] for q in quotes]
            highs = [q["high_price"] for q in quotes]
            lows = [q["low_price"] for q in quotes]
            n = len(dates)
            if n > 1:
                span = (dates[-1] - dates[0]).days or n
                width = (span / n) * 0.8
            else:
                width = 0.6
            layer = CandlestickLayer(
                x=dates, open=opens, high=highs, low=lows, close=closes,
                width=width,
            )
        elif chart_type == "line":
            layer = LineLayer(
                x=dates, y=closes,
                style=LineStyle(label="Close price"),
            )
        elif chart_type == "scatter":
            layer = ScatterLayer(
                x=dates, y=closes,
                style=ScatterStyle(label="Close price"),
            )
        elif chart_type == "box":
            layer = BoxLayer(
                values=closes,
                style=BoxStyle(label="Close price"),
            )
        else:
            layer = HistogramLayer(
                values=closes,
                style=HistogramStyle(label="Close price"),
            )

        stack.add_layer(layer)

        title_map = {
            "candlestick": "Candlestick chart",
            "line": "Close price — line",
            "scatter": "Close price — scatter",
            "box": "Price distribution — box",
            "histogram": "Price distribution — histogram",
        }
        xlabel_map = {
            "candlestick": "Date",
            "line": "Date",
            "scatter": "Date",
            "box": "Close price (USD)",
            "histogram": "Close price (USD)",
        }
        ylabel_map = {
            "candlestick": "Price (USD)",
            "line": "Price (USD)",
            "scatter": "Price (USD)",
            "box": "Price (USD)",
            "histogram": "Frequency",
        }

        chart_config = ChartConfig(
            title=f"{title_map.get(chart_type, chart_type)}  |  {start_date} — {end_date}",
            xlabel=xlabel_map.get(chart_type, "Date"),
            primary_ylabel=ylabel_map.get(chart_type, "Price (USD)"),
        )

        renderer = MatplotlibRenderer()
        renderer.render(stack=stack, context=context, chart_config=chart_config)
        fig.tight_layout()

        return fig

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
