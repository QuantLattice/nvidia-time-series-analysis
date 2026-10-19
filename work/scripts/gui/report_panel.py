"""
Report panel widget builder for the main application window.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable


def build_report_panel(
    parent_frame: ttk.Frame,
    stats_text: str,
    on_download: Callable[[], None],
) -> None:
    """
    Populate the right-side report panel with stats text and a download button.

    Clears existing children of *parent_frame*, then inserts a header label,
    a read-only scrollable Text widget, and an export button.

    Parameters
    ----------
    parent_frame : ttk.Frame
        The frame widget to populate (already placed in the layout).
    stats_text : str
        Pre-formatted statistics text to display in the panel.
    on_download : Callable[[], None]
        Callback invoked when the user clicks the download button.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """
    style = ttk.Style()
    bg = style.lookup("TFrame", "background") or "#ffffff"
    fg = style.lookup("TLabel", "foreground") or "#000000"
    sep = style.lookup("TSeparator", "background") or bg

    for w in parent_frame.winfo_children():
        w.destroy()

    ttk.Label(
        parent_frame,
        text="Отчёт",
        font=("", 10, "bold"),
    ).grid(
        row=0, column=0, columnspan=2,
        sticky="w", padx=6, pady=(6, 2),
    )

    report_text = tk.Text(
        parent_frame,
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
    report_text.insert("1.0", stats_text)
    report_text.config(state="disabled")
    report_text.grid(row=1, column=0, sticky="nsew", padx=(6, 0))

    sb = ttk.Scrollbar(
        parent_frame,
        orient="vertical",
        command=report_text.yview,
    )
    sb.grid(row=1, column=1, sticky="ns", padx=(0, 2))
    report_text.config(yscrollcommand=sb.set)

    ttk.Button(
        parent_frame,
        text="Скачать отчёт",
        command=on_download,
    ).grid(
        row=2, column=0, columnspan=2,
        sticky="ew", padx=6, pady=(4, 6),
    )
