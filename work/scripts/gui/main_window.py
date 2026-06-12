"""
Main application window composition.

This module builds the top-level interface, including the menu bar,
toolbar, context panel, content area, and layout orchestration.
"""


import tkinter as tk
from tkinter import ttk
import os
import datetime
from datetime import date
from typing import Dict, List, Any, Optional

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
        self._features_df = None

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
            on_generate_features=self._on_generate_features,
            on_plot_features=self._on_plot_features,
            on_delete_selected=self._on_delete_selected,
            on_delete_all=self._on_delete_all,
            translator=self.translator
        )

        # ── main row: chart + stats side by side ────────────────
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
        self.layout.register(name=LayoutKey.CONTEXT, widget=self.context_panel)
        self.layout.register(name=LayoutKey.CONTENT, widget=self._main_frame)

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
        page_size: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> Dict[str, object]:
        return self.stock_quote_controller.get_quotes_page(
            page=page,
            page_size=page_size,
            sort_col=sort_col,
            sort_desc=sort_desc,
        )

    def _import_csv(self) -> None:
        path = self.data_dialog.ask_csv_to_import()
        if path is None:
            return

        result = self.csv_controller.import_csv(str(path))
        self.csv_result_handler.show_import_result(result, self.data_dialog)

    def _on_delete_selected(self) -> None:
        ids = self.content_area.get_selected_ids()
        if not ids:
            self.data_dialog.show_info(
                title="Delete selected",
                message="No rows selected. Use Shift/Cmd+click to select rows.",
            )
            return

        confirmed = self.data_dialog.ask_confirm(
            title="Delete selected",
            message=f"Delete {len(ids)} selected record(s)? This cannot be undone.",
        )
        if not confirmed:
            return

        errors = 0
        for quote_id in ids:
            result = self.stock_quote_controller.delete_quote_by_id(quote_id)
            if not result["success"]:
                errors += 1

        self.content_area.refresh()

        if errors:
            self.data_dialog.show_error(
                title="Delete selected",
                message=f"Deleted {len(ids) - errors} record(s). {errors} failed.",
            )

    def _on_delete_all(self) -> None:
        confirmed = self.data_dialog.ask_confirm(
            title="Delete all",
            message="Delete ALL records from the database? This cannot be undone.",
        )
        if not confirmed:
            return

        result = self.stock_quote_controller.delete_all_quotes()
        if result["success"]:
            deleted = result["data"]["deleted"]
            self.content_area.refresh()
            self.data_dialog.show_info(
                title="Delete all",
                message=f"Deleted {deleted} record(s).",
            )
        else:
            self.data_dialog.show_error(
                title="Delete all — Error",
                message=result["error"] or "Unknown error",
            )

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

    def _get_db_date_range(self):
        result = self.stock_quote_controller.get_date_range()
        if result["success"] and result["data"]:
            return result["data"]["min_date"], result["data"]["max_date"]
        return None, None

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
            self._report_panel.grid_remove()

            return

        ui_state.active_section = section

        min_date, max_date = self._get_db_date_range()
        self.context_panel.render(section=section, min_date=min_date, max_date=max_date)

        self.layout.show(name=LayoutKey.CONTEXT)

        self._render_content(section)

    def _render_content(
        self,
        section: str
    ) -> None:
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
        """Fetch data, build the requested chart with stats panel, and display it."""

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

        stats_text = self._build_stats_text(quotes, start_date, end_date)
        self._show_report_panel(stats_text)

    def _build_stats_text(
        self,
        quotes: List[Any],
        start_date: date,
        end_date: date,
    ) -> str:
        """Compute descriptive stats for close price and volume."""

        import statistics as st

        closes = [q["close_price"] for q in quotes]
        volumes = [q["volume"] for q in quotes]
        highs = [q["high_price"] for q in quotes]
        lows = [q["low_price"] for q in quotes]

        def fmt_vol(v: float) -> str:
            if v >= 1_000_000:
                return f"{v / 1_000_000:.2f}M"
            if v >= 1_000:
                return f"{v / 1_000:.1f}K"
            return str(int(v))

        lines = [
            f"Период:",
            f"  {start_date}",
            f"  {end_date}",
            f"Торговых дней: {len(quotes)}",
            "",
            "─── Цена закрытия ───",
            f"Мин:     ${min(closes):.2f}",
            f"Макс:    ${max(closes):.2f}",
            f"Среднее: ${sum(closes)/len(closes):.2f}",
            f"Медиана: ${st.median(closes):.2f}",
            f"σ:       ${st.stdev(closes):.2f}" if len(closes) > 1 else "",
            "",
            "─── High / Low ──────",
            f"Max High: ${max(highs):.2f}",
            f"Min Low:  ${min(lows):.2f}",
            f"Диапазон: ${max(highs) - min(lows):.2f}",
            "",
            "─── Объём торгов ────",
            f"Мин:     {fmt_vol(min(volumes))}",
            f"Макс:    {fmt_vol(max(volumes))}",
            f"Среднее: {fmt_vol(sum(volumes)/len(volumes))}",
        ]

        return "\n".join(lines)

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

    def _on_generate_features(
        self,
        generator_type: str,
        start_date: date,
        end_date: date,
    ) -> Optional[List[str]]:
        """Fetch quotes, run the selected feature generator, return numeric column names."""

        result = self.stock_quote_controller.get_quotes_by_date_range(
            start_date=start_date,
            end_date=end_date,
        )

        if not result["success"]:
            self.content_area.set_placeholder(f"Error: {result['error']}")
            return None

        quotes: List[Any] = result["data"]

        if not quotes:
            self.content_area.set_placeholder(
                "No data found for the selected date range."
            )
            return None

        import pandas as pd
        from work.scripts.analytics.features import (
            MovingAverageFeatureGenerator,
            ReturnsFeatureGenerator,
            TechnicalIndicatorsFeatureGenerator,
        )

        df = pd.DataFrame(quotes)
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        df = df.sort_values("trade_date").set_index("trade_date")

        try:
            if generator_type == "Moving Averages":
                gen = MovingAverageFeatureGenerator()
                df = gen.apply(df, price_column="close_price", volume_column="volume")
            elif generator_type == "Returns":
                gen = ReturnsFeatureGenerator()
                df = gen.apply(df, price_column="close_price")
            elif generator_type == "Technical Indicators":
                gen = TechnicalIndicatorsFeatureGenerator()
                df = gen.apply(df, price_column="close_price")
        except Exception as e:
            self.content_area.set_placeholder(f"Feature generation error: {e}")
            return None

        self._features_df = df

        exclude = {"id"}
        return [
            c for c in df.select_dtypes(include="number").columns
            if c not in exclude
        ]

    def _on_plot_features(self, selected_columns: List[str]) -> None:
        """Build a multi-line chart for the selected feature columns."""

        if self._features_df is None:
            return

        fig = self._build_feature_figure(self._features_df, selected_columns)
        self.content_area.show_chart(fig)

        stats_text = self._build_feature_stats_text(self._features_df, selected_columns)
        self._show_report_panel(stats_text)

    def _build_feature_stats_text(self, df, selected_columns: List[str]) -> str:
        """Compute descriptive stats for each selected feature column."""

        import statistics as st

        lines: List[str] = []
        for col in selected_columns:
            if col not in df.columns:
                continue
            values = [v for v in df[col].dropna().tolist()]
            if not values:
                continue
            lines.append(f"── {col} ──")
            lines.append(f"  Кол-во: {len(values)}")
            lines.append(f"  Мин:    {min(values):.4f}")
            lines.append(f"  Макс:   {max(values):.4f}")
            lines.append(f"  Среднее:{sum(values)/len(values):.4f}")
            lines.append(f"  Медиана:{st.median(values):.4f}")
            if len(values) > 1:
                lines.append(f"  σ:      {st.stdev(values):.4f}")
            lines.append("")

        return "\n".join(lines)

    def _build_feature_figure(self, df, selected_columns: List[str]):
        """Build a Matplotlib Figure with one line per selected column."""

        from matplotlib.figure import Figure
        from work.library.plotting.rendering import MatplotlibRenderer
        from work.library.plotting.contracts import PlotContext, ChartConfig
        from work.library.plotting.stack import LayerStack
        from work.library.plotting.layers import LineLayer
        from work.library.plotting.contracts import LineStyle

        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        context = PlotContext(figure=fig, primary_axes=ax)
        stack = LayerStack()

        dates = df.index.to_pydatetime()

        for col in selected_columns:
            if col not in df.columns:
                continue
            values = df[col].ffill().tolist()
            stack.add_layer(LineLayer(
                x=dates,
                y=values,
                style=LineStyle(label=col),
            ))

        chart_config = ChartConfig(
            title=f"Features: {', '.join(selected_columns)}",
            xlabel="Date",
            primary_ylabel="Value",
        )

        renderer = MatplotlibRenderer()
        renderer.render(stack=stack, context=context, chart_config=chart_config)
        fig.tight_layout()

        return fig

    # ── report panel ──────────────────────────────────────────

    def _show_report_panel(self, stats_text: str) -> None:
        """Populate and reveal the right-side report panel."""

        style = ttk.Style()
        bg = style.lookup("TFrame", "background") or "#ffffff"
        fg = style.lookup("TLabel", "foreground") or "#000000"
        sep = style.lookup("TSeparator", "background") or bg

        # clear old content
        for w in self._report_panel.winfo_children():
            w.destroy()

        ttk.Label(
            self._report_panel,
            text="Отчёт",
            font=("", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=6, pady=(6, 2))

        self._report_text = tk.Text(
            self._report_panel,
            font=("Courier New", 9),
            wrap="word",
            relief="flat",
            padx=6,
            pady=4,
            background=bg,
            foreground=fg,
            insertbackground=fg,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=sep,
            state="normal",
        )
        self._report_text.insert("1.0", stats_text)
        self._report_text.config(state="disabled")
        self._report_text.grid(row=1, column=0, sticky="nsew", padx=(6, 0))

        sb = ttk.Scrollbar(
            self._report_panel, orient="vertical",
            command=self._report_text.yview,
        )
        sb.grid(row=1, column=1, sticky="ns", padx=(0, 2))
        self._report_text.config(yscrollcommand=sb.set)

        ttk.Button(
            self._report_panel,
            text="Скачать отчёт",
            command=self._export_txt,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", padx=6, pady=(4, 6))

        self._report_panel.grid()   # show

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
            min_date, max_date = self._get_db_date_range()
            self.context_panel.render(
                section=ui_state.active_section,
                min_date=min_date,
                max_date=max_date,
            )
            self.layout.show(name=LayoutKey.CONTEXT)
        else:
            self.layout.hide(name=LayoutKey.CONTEXT)
