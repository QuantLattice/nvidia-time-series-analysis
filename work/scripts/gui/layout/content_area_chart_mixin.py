"""
Chart display mixin for ContentArea.

Provides show_chart and show_chart_with_report methods that embed
Matplotlib figures into a Tkinter frame with a navigation toolbar.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from matplotlib.figure import Figure


class ContentAreaChartMixin:
    """
    Mixin that adds chart display capabilities to ContentArea.

    Requires the host class to provide ``self.clear()`` and to be
    a ``ttk.Frame`` (so that ``self.columnconfigure`` / ``rowconfigure``
    are available).

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    def show_chart(self, figure: Figure) -> None:
        """
        Embed a Matplotlib figure with a navigation toolbar.

        Parameters
        ----------
        figure : Figure
            Matplotlib figure to display.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        from matplotlib.backends.backend_tkagg import (
            FigureCanvasTkAgg,
            NavigationToolbar2Tk,
        )

        self.clear()

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()

        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(row=0, column=0, sticky="ew")

        self._toolbar = NavigationToolbar2Tk(
            canvas, toolbar_frame, pack_toolbar=True
        )
        self._toolbar.update()

        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def show_chart_with_report(
        self,
        figure: Figure,
        stats_text: str,
        on_download: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Embed a Matplotlib figure alongside an inline stats panel.

        The navigation toolbar sits top-left; the stats text and
        optional download button fill the rest of the top strip.

        Parameters
        ----------
        figure : Figure
            Matplotlib figure to display.
        stats_text : str
            Pre-formatted statistics text to show next to the toolbar.
        on_download : Callable[[], None], optional
            Callback wired to the "Скачать отчёт" button.

        Авторы
        ------
        Черкащенко Данил Дмитриевич,
        Ловчиков Станислав Олегович,
        Андреева Мария Александровна
        """
        from matplotlib.backends.backend_tkagg import (
            FigureCanvasTkAgg,
            NavigationToolbar2Tk,
        )

        self.clear()

        style = ttk.Style()
        bg = style.lookup("TFrame", "background") or "#ffffff"
        fg = style.lookup("TLabel", "foreground") or "#000000"

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()

        # row 0: toolbar (left) + stats panel (right, expands)
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.columnconfigure(0, weight=0)
        top_frame.columnconfigure(1, weight=1)
        top_frame.rowconfigure(0, weight=1)

        toolbar_frame = ttk.Frame(top_frame)
        toolbar_frame.grid(row=0, column=0, sticky="nw")
        self._toolbar = NavigationToolbar2Tk(
            canvas, toolbar_frame, pack_toolbar=True
        )
        self._toolbar.update()

        stats_frame = ttk.Frame(top_frame)
        stats_frame.grid(
            row=0, column=1, sticky="nsew", padx=(8, 0)
        )
        stats_frame.rowconfigure(0, weight=1)
        stats_frame.columnconfigure(0, weight=1)

        text_widget = tk.Text(
            stats_frame,
            wrap="none",
            font=("Courier New", 9),
            relief="flat",
            padx=8,
            pady=4,
            background=bg,
            foreground=fg,
            insertbackground=fg,
            borderwidth=0,
            highlightthickness=0,
            state="normal",
        )
        text_widget.insert("1.0", stats_text)
        text_widget.config(state="disabled")
        text_widget.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(
            stats_frame, orient="vertical", command=text_widget.yview
        )
        sb.grid(row=0, column=1, sticky="ns")
        text_widget.config(yscrollcommand=sb.set)

        if on_download is not None:
            ttk.Button(
                stats_frame,
                text="Скачать отчёт",
                command=on_download,
            ).grid(
                row=1, column=0, columnspan=2,
                sticky="ew", padx=2, pady=(2, 0)
            )

        # row 1: chart canvas fills the rest
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
