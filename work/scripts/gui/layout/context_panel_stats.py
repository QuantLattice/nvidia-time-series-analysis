"""Stats area builder for the context panel.

Provides a module-level function that constructs a scrollable text
block with an optional download button for displaying analysis stats.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


def build_stats_area(
    parent: ttk.Frame,
    stats_text: str,
    on_download: Optional[Callable[[], None]] = None,
) -> ttk.Frame:
    """Build and grid a read-only stats text block inside *parent*.

    Creates a separator, a scrollable ``tk.Text`` widget pre-filled
    with *stats_text*, and (optionally) a download button.

    Parameters
    ----------
    parent : ttk.Frame
        Container frame placed at grid row 10 of the context panel.
    stats_text : str
        Pre-formatted statistics text to display.
    on_download : Callable[[], None], optional
        Callback wired to the "Скачать отчёт" button.  The button is
        only rendered when this argument is not ``None``.

    Returns
    -------
    ttk.Frame
        The *parent* frame (for convenience / assignment).

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    style = ttk.Style()
    bg = style.lookup("TFrame", "background") or "#ffffff"
    fg = style.lookup("TLabel", "foreground") or "#000000"
    sep_color = style.lookup("TSeparator", "background") or bg

    ttk.Separator(parent, orient="horizontal").grid(
        row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6)
    )

    text = tk.Text(
        parent,
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

    sb = ttk.Scrollbar(
        parent, orient="vertical", command=text.yview
    )
    sb.grid(row=1, column=1, sticky="ns")
    text.config(yscrollcommand=sb.set)

    if on_download is not None:
        ttk.Button(
            parent,
            text="Скачать отчёт",
            command=on_download,
        ).grid(
            row=2, column=0, columnspan=2,
            sticky="ew", pady=(6, 0)
        )

    return parent
