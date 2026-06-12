"""
Context panel component.

This module implements the side panel that changes its content
depending on the currently active application section.
"""


import tkinter as tk
from tkinter import ttk, Tk
from datetime import date
from typing import Callable, List, Optional

from work.scripts.core import AppState
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.services.translator import Translator
from work.scripts.gui.utils.date_entry import DatePickerEntry


class ContextPanel(ttk.Frame):
    """
    Side panel that renders controls for the active section.

    Parameters
    ----------
    parent : Tk
        Root application window.

    ui_factory : UIFactory
        Factory used to create themed UI controls.

    app_state : AppState
        Shared runtime application state.

    on_import_csv : Callable[[], None]
        Callback for importing a CSV file.

    on_export_csv : Callable[[], None]
        Callback for exporting a CSV file.

    on_run_analysis : Callable[[date, date, str], None]
        Callback invoked when the user clicks "Plot".
        Receives (start_date, end_date, chart_type).

    on_generate_features : Callable[[str, date, date], Optional[List[str]]]
        Callback invoked when the user clicks "Generate".
        Receives (generator_type, start_date, end_date).
        Returns list of numeric column names or None on error.

    on_plot_features : Callable[[List[str]], None]
        Callback invoked when the user clicks "Plot" in features section.
        Receives the list of selected column names.

    on_delete_selected : Callable[[], None]
        Callback invoked when the user clicks "Delete selected".

    on_delete_all : Callable[[], None]
        Callback invoked when the user clicks "Delete all".

    translator : Translator
        Localization service.
    """

    def __init__(
        self,
        parent: Tk,
        ui_factory: UIFactory,
        app_state: AppState,
        on_import_csv: Callable[[], None],
        on_export_csv: Callable[[], None],
        on_run_analysis: Callable[[date, date, str], None],
        on_generate_features: Callable[[str, date, date], Optional[List[str]]],
        on_plot_features: Callable[[List[str]], None],
        on_delete_selected: Callable[[], None],
        on_delete_all: Callable[[], None],
        translator: Translator
    ) -> None:
        super().__init__(parent)

        self.ui_factory = ui_factory
        self.app_state = app_state
        self.on_import_csv = on_import_csv
        self.on_export_csv = on_export_csv
        self.on_run_analysis = on_run_analysis
        self.on_generate_features = on_generate_features
        self.on_plot_features = on_plot_features
        self.on_delete_selected = on_delete_selected
        self.on_delete_all = on_delete_all
        self.translator = translator

        self._start_picker: Optional[DatePickerEntry] = None
        self._end_picker: Optional[DatePickerEntry] = None
        self._chart_type_var: Optional[ttk.Combobox] = None

        self._feat_start_picker: Optional[DatePickerEntry] = None
        self._feat_end_picker: Optional[DatePickerEntry] = None
        self._feat_generator_var: Optional[ttk.Combobox] = None
        self._feat_column_frame: Optional[ttk.Frame] = None
        self._features_listbox: Optional[tk.Listbox] = None
        self._feat_df_columns: List[str] = []
        self._stats_area: Optional[ttk.Frame] = None

    def render(
        self,
        section: str,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> None:
        """
        Render controls for the requested section.

        Parameters
        ----------
        section : str
            Active application section identifier.
        min_date : date, optional
            Earliest available date in the database (pre-fills start picker).
        max_date : date, optional
            Latest available date in the database (pre-fills end picker).
        """

        self._stats_area = None
        for widget in self.winfo_children():
            widget.destroy()

        if section == "data":
            self._build_data()
        elif section == "analysis":
            self._build_analysis(min_date=min_date, max_date=max_date)
        elif section == "features":
            self._build_features(min_date=min_date, max_date=max_date)

    def _build_data(self) -> None:
        ttk.Label(
            master=self,
            text="Data management"
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.ui_factory.text_button(
            parent=self,
            text="Delete selected",
            command=self.on_delete_selected,
        ).grid(row=1, column=0, sticky="ew", pady=(0, 4))

        self.ui_factory.text_button(
            parent=self,
            text="Delete all",
            command=self.on_delete_all,
        ).grid(row=2, column=0, sticky="ew")

    def _build_analysis(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> None:
        """
        Build analysis section controls: date pickers, chart type, plot button.
        Year is selected inside the CalendarPopup via its built-in spinbox.
        """

        ttk.Label(
            master=self,
            text="Analysis parameters"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        form = ttk.Frame(master=self)
        form.grid(row=1, column=0, sticky="w")
        form.columnconfigure(1, weight=1)

        today = date.today()
        start_initial = min_date if min_date is not None else date(today.year, 1, 1)
        end_initial = max_date if max_date is not None else today

        # --- Start date ---
        ttk.Label(master=form, text="Start date").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._start_picker = DatePickerEntry(
            parent=form,
            initial_date=start_initial,
        )
        self._start_picker.grid(row=0, column=1, sticky="w", pady=3)

        # --- End date ---
        ttk.Label(master=form, text="End date").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._end_picker = DatePickerEntry(
            parent=form,
            initial_date=end_initial,
        )
        self._end_picker.grid(row=1, column=1, sticky="w", pady=3)

        ttk.Separator(form, orient="horizontal").grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(6, 4)
        )

        # --- Chart type ---
        ttk.Label(master=form, text="Chart type").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=3
        )
        chart_types = ["Candlestick", "Line", "Scatter", "Box", "Histogram"]
        self._chart_type_var = ttk.Combobox(
            master=form,
            values=chart_types,
            state="readonly",
            width=12,
        )
        self._chart_type_var.set(chart_types[0])
        self._chart_type_var.grid(row=3, column=1, sticky="w", pady=3)

        # --- Plot button ---
        self.ui_factory.text_button(
            parent=form,
            text="Plot",
            command=self._on_plot_click,
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _on_plot_click(self) -> None:
        """Validate inputs and invoke the analysis callback."""

        if self._start_picker is None or self._end_picker is None:
            return

        start = self._start_picker.get_date()
        end = self._end_picker.get_date()

        if start is None or end is None:
            return

        if start > end:
            start, end = end, start

        chart_type = (
            self._chart_type_var.get().lower()
            if self._chart_type_var is not None
            else "candlestick"
        )

        self.on_run_analysis(start, end, chart_type)

    def _build_features(
        self,
        min_date: Optional[date] = None,
        max_date: Optional[date] = None,
    ) -> None:
        """
        Build features section controls: generator selector, date range,
        generate button, and (after generation) column selector with plot button.
        """

        self._feat_column_frame = None
        self._features_listbox = None
        self._feat_df_columns = []

        ttk.Label(
            master=self,
            text="Feature generation"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        form = ttk.Frame(master=self)
        form.grid(row=1, column=0, sticky="w")
        form.columnconfigure(1, weight=1)
        self._feat_form = form

        today = date.today()
        start_initial = min_date if min_date is not None else date(today.year, 1, 1)
        end_initial = max_date if max_date is not None else today

        ttk.Label(master=form, text="Generator").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=3
        )
        generator_options = ["Moving Averages", "Returns", "Technical Indicators"]
        self._feat_generator_var = ttk.Combobox(
            master=form,
            values=generator_options,
            state="readonly",
            width=18,
        )
        self._feat_generator_var.set(generator_options[0])
        self._feat_generator_var.grid(row=0, column=1, sticky="w", pady=3)

        ttk.Label(master=form, text="Start date").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._feat_start_picker = DatePickerEntry(
            parent=form,
            initial_date=start_initial,
        )
        self._feat_start_picker.grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(master=form, text="End date").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._feat_end_picker = DatePickerEntry(
            parent=form,
            initial_date=end_initial,
        )
        self._feat_end_picker.grid(row=2, column=1, sticky="w", pady=3)

        self.ui_factory.text_button(
            parent=form,
            text="Generate",
            command=self._on_generate_click,
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _on_generate_click(self) -> None:
        if self._feat_start_picker is None or self._feat_end_picker is None:
            return

        start = self._feat_start_picker.get_date()
        end = self._feat_end_picker.get_date()

        if start is None or end is None:
            return

        if start > end:
            start, end = end, start

        generator_type = (
            self._feat_generator_var.get()
            if self._feat_generator_var is not None
            else "Moving Averages"
        )

        columns = self.on_generate_features(generator_type, start, end)
        if columns is None:
            return

        self._feat_df_columns = columns

        if self._feat_column_frame is not None:
            self._feat_column_frame.destroy()

        if self._stats_area is not None:
            self._stats_area.destroy()
            self._stats_area = None

        self._feat_column_frame = ttk.Frame(self)
        self._feat_column_frame.grid(row=2, column=0, sticky="nsew", pady=(8, 0))

        ttk.Separator(self._feat_column_frame, orient="horizontal").pack(
            fill="x", pady=(0, 6)
        )
        ttk.Label(master=self._feat_column_frame, text="Columns to plot").pack(
            anchor="w"
        )

        list_frame = ttk.Frame(self._feat_column_frame)
        list_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        bg = style.lookup("TFrame", "background") or "#ffffff"
        fg = style.lookup("TLabel", "foreground") or "#000000"
        sel_bg = style.lookup("TButton", "background") or "#d0d0d0"

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        self._features_listbox = tk.Listbox(
            list_frame,
            selectmode="multiple",
            yscrollcommand=scrollbar.set,
            height=8,
            exportselection=False,
            background=bg,
            foreground=fg,
            selectbackground=sel_bg,
            selectforeground=fg,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=style.lookup("TSeparator", "background") or bg,
            relief="flat",
        )
        scrollbar.config(command=self._features_listbox.yview)

        for col in columns:
            self._features_listbox.insert("end", col)

        self._features_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.ui_factory.text_button(
            parent=self._feat_column_frame,
            text="Plot",
            command=self._on_plot_features_click,
        ).pack(anchor="w", pady=(8, 0))

    def _on_plot_features_click(self) -> None:
        if self._features_listbox is None or not self._feat_df_columns:
            return

        selected_indices = self._features_listbox.curselection()
        selected_columns = [self._feat_df_columns[i] for i in selected_indices]

        if not selected_columns:
            return

        self.on_plot_features(selected_columns)

    # ── public stats API ─────────────────────────────────────────

    def show_stats(
        self,
        stats_text: str,
        on_download: Optional[Callable[[], None]] = None,
    ) -> None:
        """Render a stats block below the section controls (grid row 10)."""

        if self._stats_area is not None:
            self._stats_area.destroy()

        style = ttk.Style()
        bg = style.lookup("TFrame", "background") or "#ffffff"
        fg = style.lookup("TLabel", "foreground") or "#000000"
        sep_color = style.lookup("TSeparator", "background") or bg

        frame = ttk.Frame(self)
        frame.grid(row=10, column=0, sticky="nsew", pady=(10, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        self.rowconfigure(10, weight=1)
        self._stats_area = frame

        ttk.Separator(frame, orient="horizontal").grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6)
        )

        text = tk.Text(
            frame,
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
            highlightbackground=sep_color,
            state="normal",
        )
        text.insert("1.0", stats_text)
        text.config(state="disabled")
        text.grid(row=1, column=0, sticky="nsew")

        sb = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        sb.grid(row=1, column=1, sticky="ns")
        text.config(yscrollcommand=sb.set)

        if on_download is not None:
            ttk.Button(
                frame,
                text="Скачать отчёт",
                command=on_download,
            ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 0))

