"""
Main content display area.

This module defines the central content container used to show
tables, reports, charts, or placeholder text depending on the
active application section.
"""


import tkinter as tk
from tkinter import ttk, Tk
from typing import Any, Callable, Dict, List, Optional

from matplotlib.figure import Figure


class ContentArea(ttk.Frame):
    """
    Central content container.

    Parameters
    ----------
    parent : Tk
        Root application window.
    """

    def __init__(
        self,
        parent: Tk
    ) -> None:
        """
        Initialize the content area.

        Parameters
        ----------
        parent : Tk
            Root application window.
        """

        super().__init__(master=parent, style='App.TFrame')
        self._page = 1
        self._page_size = 100
        self._total_pages = 1
        self._sort_col: str = 'trade_date'
        self._sort_desc: bool = False
        self._load_page_callback: Optional[Callable] = None
        self._columns = (
            'id',
            'trade_date',
            'source',
            'open_price',
            'high_price',
            'low_price',
            'close_price',
            'adj_close_price',
            'volume',
        )
        self._build()
        self.bind('<Configure>', self._on_resize)

    def _on_resize(self, event) -> None:
        if not hasattr(self, 'table') or not self.table.winfo_exists():
            return
        avail = event.width - 20
        if avail < 50:
            return
        weights = {
            'id': 1,
            'trade_date': 3,
            'source': 3,
            'open_price': 2,
            'high_price': 2,
            'low_price': 2,
            'close_price': 2,
            'adj_close_price': 2,
            'volume': 2,
        }
        total_w = sum(weights.get(c, 2) for c in self._columns)
        for col in self._columns:
            w = max(30, int(avail * weights.get(col, 2) / total_w))
            self.table.column(col, width=w, stretch=False)

    def _build(self) -> None:
        self.clear()

        self.table = ttk.Treeview(
            self,
            columns=self._columns,
            show='headings',
            selectmode='extended',
        )

        self._update_headings()

        for col in self._columns:
            self.table.column(col, width=100, anchor='center', stretch=False)

        scrollbar_y = ttk.Scrollbar(
            self,
            orient='vertical',
            command=self.table.yview,  # type: ignore
        )
        self.table.configure(yscrollcommand=scrollbar_y.set)

        self.table.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        pager = ttk.Frame(self)
        pager.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(8, 0))

        self.prev_button = ttk.Button(pager, text='Prev', command=self.prev_page)
        self.prev_button.pack(side='left')

        self.page_label = ttk.Label(pager, text='Page 1 / 1')
        self.page_label.pack(side='left', padx=10)

        self.next_button = ttk.Button(pager, text='Next', command=self.next_page)
        self.next_button.pack(side='left')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def set_placeholder(
        self,
        text: str
    ) -> None:
        """
        Display placeholder text in the content area.

        Parameters
        ----------
        text : str
            Text shown inside the content area.
        """

        self.clear()
        ttk.Label(self, text=text).pack(padx=10, pady=10)

    def _update_headings(self) -> None:
        for col in self._columns:
            label = col
            if col == self._sort_col:
                label = f'{col} {"▼" if self._sort_desc else "▲"}'
            self.table.heading(col, text=label, command=lambda c=col: self._sort_by(c))

    def _sort_by(self, col: str) -> None:
        if self._sort_col == col:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col = col
            self._sort_desc = False
        self._page = 1
        self._update_headings()
        self._reload()

    def set_loader(
        self,
        loader: Callable,
    ) -> None:
        self._load_page_callback = loader

    def show_quotes(self, page: int = 1, page_size: int = 100) -> None:
        self._build()

        self._page = page
        self._page_size = page_size

        self._reload()

    def refresh(self) -> None:
        self._reload()

    def _reload(self) -> None:
        if self._load_page_callback is None:
            return

        result = self._load_page_callback(
            self._page, self._page_size, self._sort_col, self._sort_desc
        )
        data = result['data']

        if data is None:
            self.clear()
            ttk.Label(self, text='No data').grid(row=0, column=0, sticky='w')
            return

        items = data['items']
        self._total_pages = data['total_pages']
        self._render_rows(items)
        self._update_pager()

    def _render_rows(self, items: List[Dict[str, Any]]) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        for item in items:
            self.table.insert(
                '',
                'end',
                values=(
                    item['id'],
                    item['trade_date'],
                    item['source'],
                    item['open_price'],
                    item['high_price'],
                    item['low_price'],
                    item['close_price'],
                    item['adj_close_price'],
                    item['volume'],
                ),
            )

    def _update_pager(self) -> None:
        self.page_label.configure(
            text=f'Page {self._page} / {self._total_pages}'
        )
        self.prev_button.configure(
            state='normal' if self._page > 1 else 'disabled'
        )
        self.next_button.configure(
            state='normal' if self._page < self._total_pages else 'disabled'
        )

    def next_page(self) -> None:
        if self._page < self._total_pages:
            self._page += 1
            self._reload()

    def prev_page(self) -> None:
        if self._page > 1:
            self._page -= 1
            self._reload()

    def get_selected_ids(self) -> List[int]:
        """Return the IDs of all currently selected table rows."""
        ids = []
        for item in self.table.selection():
            values = self.table.item(item, 'values')
            if values:
                try:
                    ids.append(int(values[0]))
                except (ValueError, IndexError):
                    pass
        return ids

    def show_chart(self, figure: Figure) -> None:
        from matplotlib.backends.backend_tkagg import (
            FigureCanvasTkAgg,
            NavigationToolbar2Tk,
        )

        self.clear()

        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()

        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(row=0, column=0, sticky="ew")

        self._toolbar = NavigationToolbar2Tk(canvas, toolbar_frame, pack_toolbar=True)
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
        """Toolbar compact on the left; stats fills the rest of the top strip."""

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

        # ── row 0: top strip — toolbar (left, compact) + stats (right, expands) ──
        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="nsew")
        # column 0 = toolbar (natural width); column 1 = stats (takes the rest)
        top_frame.columnconfigure(0, weight=0)
        top_frame.columnconfigure(1, weight=1)
        top_frame.rowconfigure(0, weight=1)

        toolbar_frame = ttk.Frame(top_frame)
        toolbar_frame.grid(row=0, column=0, sticky="nw")
        self._toolbar = NavigationToolbar2Tk(canvas, toolbar_frame, pack_toolbar=True)
        self._toolbar.update()

        # stats panel — no fixed width, fills all remaining horizontal space
        stats_frame = ttk.Frame(top_frame)
        stats_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
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

        sb = ttk.Scrollbar(stats_frame, orient="vertical", command=text_widget.yview)
        sb.grid(row=0, column=1, sticky="ns")
        text_widget.config(yscrollcommand=sb.set)

        if on_download is not None:
            ttk.Button(
                stats_frame,
                text="Скачать отчёт",
                command=on_download,
            ).grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=(2, 0))

        # ── row 1: chart canvas fills the rest ───────────────────
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def clear(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
