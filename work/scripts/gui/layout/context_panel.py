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

    on_export_txt : Callable[[], None]
        Callback invoked when the user clicks "Export TXT".

    on_generate_features : Callable[[str, date, date], Optional[List[str]]]
        Callback invoked when the user clicks "Generate".
        Receives (generator_type, start_date, end_date).
        Returns list of numeric column names or None on error.

    on_plot_features : Callable[[List[str]], None]
        Callback invoked when the user clicks "Plot" in features section.
        Receives the list of selected column names.

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
        on_export_txt: Callable[[], None],
        on_generate_features: Callable[[str, date, date], Optional[List[str]]],
        on_plot_features: Callable[[List[str]], None],
        translator: Translator
    ) -> None:
        super().__init__(parent)

        self.ui_factory = ui_factory
        self.app_state = app_state
        self.on_import_csv = on_import_csv
        self.on_export_csv = on_export_csv
        self.on_run_analysis = on_run_analysis
        self.on_export_txt = on_export_txt
        self.on_generate_features = on_generate_features
        self.on_plot_features = on_plot_features
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

    def render(
        self,
        section: str
    ) -> None:
        """
        Render controls for the requested section.

        Parameters
        ----------
        section : str
            Active application section identifier.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if section == "data":
            self._build_data()
        elif section == "analysis":
            self._build_analysis()
        elif section == "features":
            self._build_features()
        elif section == "reports":
            self._build_reports()

    def _build_data(self) -> None:
        """
        Build data section controls.
        """

        actions = ttk.Frame(self)
        actions.pack(anchor="w")

        data = self.translator.get_data().context_panel

        self.ui_factory.text_button(
            parent=actions,
            text=data.import_csv_text,
            command=self.on_import_csv,
        ).pack(side="left", padx=5, pady=5)

        self.ui_factory.text_button(
            parent=actions,
            text=data.export_csv_text,
            command=self.on_export_csv,
        ).pack(side="left", padx=5, pady=5)

    def _build_analysis(self) -> None:
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

        # --- Start date ---
        ttk.Label(master=form, text="Start date").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._start_picker = DatePickerEntry(
            parent=form,
            initial_date=date(today.year, 1, 1),
        )
        self._start_picker.grid(row=0, column=1, sticky="w", pady=3)

        # --- End date ---
        ttk.Label(master=form, text="End date").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._end_picker = DatePickerEntry(
            parent=form,
            initial_date=today,
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

    def _build_features(self) -> None:
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
            initial_date=date(today.year, 1, 1),
        )
        self._feat_start_picker.grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(master=form, text="End date").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=3
        )
        self._feat_end_picker = DatePickerEntry(
            parent=form,
            initial_date=today,
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

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        self._features_listbox = tk.Listbox(
            list_frame,
            selectmode="multiple",
            yscrollcommand=scrollbar.set,
            height=8,
            exportselection=False,
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

    def _build_reports(self) -> None:
        """
        Build reports section controls: CSV export and TXT analytics report.
        """

        data = self.translator.get_data().context_panel

        ttk.Label(master=self, text="Reports").pack(anchor="w")

        self.ui_factory.text_button(
            parent=self,
            text=data.export_csv_text,
            command=self.on_export_csv,
        ).pack(side="left", padx=5, pady=5)

        self.ui_factory.text_button(
            parent=self,
            text="Export TXT",
            command=self.on_export_txt,
        ).pack(side="left", padx=5, pady=5)
