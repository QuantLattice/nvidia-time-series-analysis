"""
Main content display area.

This module defines the central content container used to show
tables, reports, charts, or placeholder text depending on the
active application section.
"""


from tkinter import ttk, Tk
from typing import Any, Callable, Dict, List


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
        self._load_page_callback: Callable[
            [int, int], Dict[str, Any]
        ] | None = None
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

    def _build(self) -> None:
        self.clear()

        self.table = ttk.Treeview(
            self,
            columns=self._columns,
            show='headings',
        )

        for col in self._columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor='center')

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

        self.prev_button = ttk.Button(
            pager,
            text='Prev',
            command=self.prev_page,
        )
        self.prev_button.pack(side='left')

        self.page_label = ttk.Label(pager, text='Page 1 / 1')
        self.page_label.pack(side='left', padx=10)

        self.next_button = ttk.Button(
            pager,
            text='Next',
            command=self.next_page,
        )
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

    def set_loader(
        self,
        loader: Callable[[int, int], Dict[str, Any]]
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

        result = self._load_page_callback(self._page, self._page_size)
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

    def clear(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()
