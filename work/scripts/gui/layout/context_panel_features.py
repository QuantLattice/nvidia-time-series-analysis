"""Features form builders for the context panel.

This module provides module-level functions that construct the
feature-generation form widgets and the column-selector listbox
for the features section of the context panel.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date
from typing import List, Optional, Tuple

from work.scripts.gui.factories import UIFactory
from work.scripts.gui.utils.date_entry import DatePickerEntry


def build_features_form(
    panel: ttk.Frame,
    ui_factory: UIFactory,
    min_date: Optional[date],
    max_date: Optional[date],
    on_generate_click,
) -> Tuple[DatePickerEntry, DatePickerEntry, ttk.Combobox]:
    """Build and grid the feature-generation form widgets.

    Creates a labelled form with a generator selector, start/end date
    pickers, and a Generate button, all placed inside *panel*.

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
    on_generate_click : callable
        Command wired to the Generate button.

    Returns
    -------
    tuple[DatePickerEntry, DatePickerEntry, ttk.Combobox]
        ``(start_picker, end_picker, generator_var)``

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    ttk.Label(
        master=panel,
        text="Feature generation"
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    form = ttk.Frame(master=panel)
    form.grid(row=1, column=0, sticky="w")
    form.columnconfigure(1, weight=1)

    today = date.today()
    start_initial = (
        min_date if min_date is not None else date(today.year, 1, 1)
    )
    end_initial = max_date if max_date is not None else today

    ttk.Label(master=form, text="Generator").grid(
        row=0, column=0, sticky="w", padx=(0, 8), pady=3
    )
    generator_options = [
        "Moving Averages", "Returns", "Technical Indicators"
    ]
    generator_var = ttk.Combobox(
        master=form,
        values=generator_options,
        state="readonly",
        width=18,
    )
    generator_var.set(generator_options[0])
    generator_var.grid(row=0, column=1, sticky="w", pady=3)

    ttk.Label(master=form, text="Start date").grid(
        row=1, column=0, sticky="w", padx=(0, 8), pady=3
    )
    start_picker = DatePickerEntry(
        parent=form,
        initial_date=start_initial,
    )
    start_picker.grid(row=1, column=1, sticky="w", pady=3)

    ttk.Label(master=form, text="End date").grid(
        row=2, column=0, sticky="w", padx=(0, 8), pady=3
    )
    end_picker = DatePickerEntry(
        parent=form,
        initial_date=end_initial,
    )
    end_picker.grid(row=2, column=1, sticky="w", pady=3)

    ui_factory.text_button(
        parent=form,
        text="Generate",
        command=on_generate_click,
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))

    return start_picker, end_picker, generator_var


def build_column_selector(
    parent_frame: ttk.Frame,
    columns: List[str],
    style: ttk.Style,
    ui_factory: UIFactory,
    on_plot_click,
) -> tk.Listbox:
    """Build and pack the column-selector listbox inside *parent_frame*.

    Creates a scrollable multi-select listbox populated with *columns*,
    plus a Plot button beneath it.

    Parameters
    ----------
    parent_frame : ttk.Frame
        Container frame that already has a separator and label above
        this widget.
    columns : list[str]
        Column names to populate the listbox with.
    style : ttk.Style
        Active ttk style used to look up theme colours.
    ui_factory : UIFactory
        Factory used to create themed UI controls.
    on_plot_click : callable
        Command wired to the Plot button.

    Returns
    -------
    tk.Listbox
        The populated listbox widget.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    bg = style.lookup("TFrame", "background") or "#ffffff"
    fg = style.lookup("TLabel", "foreground") or "#000000"
    sel_bg = style.lookup("TButton", "background") or "#d0d0d0"
    hl_bg = (
        style.lookup("TSeparator", "background") or bg
    )

    list_frame = ttk.Frame(parent_frame)
    list_frame.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    listbox = tk.Listbox(
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
        highlightbackground=hl_bg,
        relief="flat",
    )
    scrollbar.config(command=listbox.yview)

    for col in columns:
        listbox.insert("end", col)

    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ui_factory.text_button(
        parent=parent_frame,
        text="Plot",
        command=on_plot_click,
    ).pack(anchor="w", pady=(8, 0))

    return listbox
