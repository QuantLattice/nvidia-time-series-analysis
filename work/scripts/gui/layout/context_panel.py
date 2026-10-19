"""Context panel component.

Side panel that changes its content depending on the active section.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import tkinter as tk
from tkinter import ttk, Tk
from datetime import date
from typing import Callable, List, Optional

from work.scripts.core import AppState
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.services.translator import Translator
from work.scripts.gui.utils.date_entry import DatePickerEntry
from work.scripts.gui.layout.context_panel_analysis import (
    build_analysis_form,
)
from work.scripts.gui.layout.context_panel_features import (
    build_features_form,
    build_column_selector,
)
from work.scripts.gui.layout.context_panel_stats import (
    build_stats_area,
)


class ContextPanel(ttk.Frame):
    """Side panel rendering controls for the active section.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    def __init__(
        self,
        parent: Tk,
        ui_factory: UIFactory,
        app_state: AppState,
        on_import_csv: Callable[[], None],
        on_export_csv: Callable[[], None],
        on_run_analysis: Callable[[date, date, str], None],
        on_generate_features: Callable[
            [str, date, date], Optional[List[str]]
        ],
        on_plot_features: Callable[[List[str]], None],
        on_delete_selected: Callable[[], None],
        on_delete_all: Callable[[], None],
        translator: Translator
    ) -> None:
        """Bind all callbacks and initialise instance variables.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
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
        """Render controls for section ('data'/'analysis'/'features').

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
        """Build data management section controls."""
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
        """Build analysis controls via build_analysis_form.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        (
            self._start_picker,
            self._end_picker,
            self._chart_type_var,
        ) = build_analysis_form(
            panel=self,
            ui_factory=self.ui_factory,
            min_date=min_date,
            max_date=max_date,
            on_plot_click=self._on_plot_click,
        )

    def _on_plot_click(self) -> None:
        """Validate inputs and invoke the analysis callback.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
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
        """Build features controls via build_features_form.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self._feat_column_frame = None
        self._features_listbox = None
        self._feat_df_columns = []

        (
            self._feat_start_picker,
            self._feat_end_picker,
            self._feat_generator_var,
        ) = build_features_form(
            panel=self,
            ui_factory=self.ui_factory,
            min_date=min_date,
            max_date=max_date,
            on_generate_click=self._on_generate_click,
        )

    def _on_generate_click(self) -> None:
        """Validate inputs, invoke generate callback, show column selector."""
        if (
            self._feat_start_picker is None
            or self._feat_end_picker is None
        ):
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
        self._feat_column_frame.grid(
            row=2, column=0, sticky="nsew", pady=(8, 0)
        )

        ttk.Separator(
            self._feat_column_frame, orient="horizontal"
        ).pack(fill="x", pady=(0, 6))
        ttk.Label(
            master=self._feat_column_frame, text="Columns to plot"
        ).pack(anchor="w")

        style = ttk.Style()
        self._features_listbox = build_column_selector(
            parent_frame=self._feat_column_frame,
            columns=columns,
            style=style,
            ui_factory=self.ui_factory,
            on_plot_click=self._on_plot_features_click,
        )

    def _on_plot_features_click(self) -> None:
        """Read selected columns from listbox and invoke plot callback."""
        if (
            self._features_listbox is None
            or not self._feat_df_columns
        ):
            return

        selected_indices = self._features_listbox.curselection()
        selected_columns = [
            self._feat_df_columns[i] for i in selected_indices
        ]

        if not selected_columns:
            return

        self.on_plot_features(selected_columns)

    # ── public stats API ─────────────────────────────────────────

    def show_stats(
        self,
        stats_text: str,
        on_download: Optional[Callable[[], None]] = None,
    ) -> None:
        """Render a stats block below section controls (row 10).

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        if self._stats_area is not None:
            self._stats_area.destroy()

        frame = ttk.Frame(self)
        frame.grid(row=10, column=0, sticky="nsew", pady=(10, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        self.rowconfigure(10, weight=1)
        self._stats_area = frame

        build_stats_area(
            parent=frame,
            stats_text=stats_text,
            on_download=on_download,
        )
