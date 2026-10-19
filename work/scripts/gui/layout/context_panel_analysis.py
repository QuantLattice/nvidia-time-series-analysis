"""Analysis form builder for the context panel.

This module provides a module-level function that constructs the
date-range and chart-type form widgets for the analysis section of
the context panel.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import tkinter as tk  # noqa: F401  (kept for consistent tk namespace)
from tkinter import ttk
from datetime import date
from typing import Tuple, Optional

from work.scripts.gui.factories import UIFactory
from work.scripts.gui.utils.date_entry import DatePickerEntry


def build_analysis_form(
    panel: ttk.Frame,
    ui_factory: UIFactory,
    min_date: Optional[date],
    max_date: Optional[date],
    on_plot_click,
) -> Tuple[DatePickerEntry, DatePickerEntry, ttk.Combobox]:
    """Build and grid the analysis section form widgets.

    Creates a labelled form with start/end date pickers, a chart-type
    combobox, and a Plot button, all placed inside *panel*.

    Parameters
    ----------
    panel : ttk.Frame
        Parent frame that owns the widgets (the ContextPanel itself).
    ui_factory : UIFactory
        Factory used to create themed UI controls.
    min_date : date, optional
        Earliest available date; pre-fills the start picker.
    max_date : date, optional
        Latest available date; pre-fills the end picker.
    on_plot_click : callable
        Command wired to the Plot button.

    Returns
    -------
    tuple[DatePickerEntry, DatePickerEntry, ttk.Combobox]
        ``(start_picker, end_picker, chart_type_var)``

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    ttk.Label(
        master=panel,
        text="Analysis parameters"
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    form = ttk.Frame(master=panel)
    form.grid(row=1, column=0, sticky="w")
    form.columnconfigure(1, weight=1)

    today = date.today()
    start_initial = (
        min_date if min_date is not None else date(today.year, 1, 1)
    )
    end_initial = max_date if max_date is not None else today

    # --- Start date ---
    ttk.Label(master=form, text="Start date").grid(
        row=0, column=0, sticky="w", padx=(0, 8), pady=3
    )
    start_picker = DatePickerEntry(
        parent=form,
        initial_date=start_initial,
    )
    start_picker.grid(row=0, column=1, sticky="w", pady=3)

    # --- End date ---
    ttk.Label(master=form, text="End date").grid(
        row=1, column=0, sticky="w", padx=(0, 8), pady=3
    )
    end_picker = DatePickerEntry(
        parent=form,
        initial_date=end_initial,
    )
    end_picker.grid(row=1, column=1, sticky="w", pady=3)

    ttk.Separator(form, orient="horizontal").grid(
        row=2, column=0, columnspan=2, sticky="ew", pady=(6, 4)
    )

    # --- Chart type ---
    ttk.Label(master=form, text="Chart type").grid(
        row=3, column=0, sticky="w", padx=(0, 8), pady=3
    )
    chart_types = [
        "Candlestick", "Line", "Scatter", "Box", "Histogram"
    ]
    chart_type_var = ttk.Combobox(
        master=form,
        values=chart_types,
        state="readonly",
        width=12,
    )
    chart_type_var.set(chart_types[0])
    chart_type_var.grid(row=3, column=1, sticky="w", pady=3)

    # --- Plot button ---
    ui_factory.text_button(
        parent=form,
        text="Plot",
        command=on_plot_click,
    ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

    return start_picker, end_picker, chart_type_var
