"""
Main content display area.

This module defines the central content container used to show
tables, reports, charts, or placeholder text depending on the
active application section.
"""


from tkinter import ttk, Tk
from typing import Any, Callable, Dict, List, Optional

from work.scripts.gui.layout.content_area_chart_mixin import (
    ContentAreaChartMixin,
)


class ContentArea(ttk.Frame, ContentAreaChartMixin):
    """
    Central content container.

    Parameters
    ----------
    parent : Tk
        Root application window.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    def __init__(self, parent: Tk) -> None:
        """Initialize the content area with table, pager, and bindings.

        Parameters
        ----------
        parent : Tk
            Root application window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
        """Redistribute column widths proportionally when resized."""
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
        """Build or rebuild the table, scrollbar, and pager widgets."""
        self.clear()

        self.table = ttk.Treeview(
            self,
            columns=self._columns,
            show='headings',
            selectmode='extended',
        )

        self._update_headings()

        for col in self._columns:
            self.table.column(
                col, width=100, anchor='center', stretch=False
            )

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
            pager, text='Prev', command=self.prev_page
        )
        self.prev_button.pack(side='left')

        self.page_label = ttk.Label(pager, text='Page 1 / 1')
        self.page_label.pack(side='left', padx=10)

        self.next_button = ttk.Button(
            pager, text='Next', command=self.next_page
        )
        self.next_button.pack(side='left')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def set_placeholder(self, text: str) -> None:
        """Display placeholder text in the content area.

        Parameters
        ----------
        text : str
            Text shown inside the content area.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.clear()
        ttk.Label(self, text=text).pack(padx=10, pady=10)

    def _update_headings(self) -> None:
        """Update column heading labels to show sort indicator."""
        for col in self._columns:
            label = col
            if col == self._sort_col:
                label = f'{col} {"▼" if self._sort_desc else "▲"}'
            self.table.heading(
                col, text=label,
                command=lambda c=col: self._sort_by(c)
            )

    def _sort_by(self, col: str) -> None:
        """Toggle sort order or switch sort column, then reload."""
        if self._sort_col == col:
            self._sort_desc = not self._sort_desc
        else:
            self._sort_col = col
            self._sort_desc = False
        self._page = 1
        self._update_headings()
        self._reload()

    def set_loader(self, loader: Callable) -> None:
        """Register the callable used to load paginated quote data.

        Parameters
        ----------
        loader : Callable
            Callable with signature
            (page, page_size, sort_col, sort_desc) -> dict.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self._load_page_callback = loader

    def show_quotes(self, page: int = 1, page_size: int = 100) -> None:
        """Rebuild the table and load the specified page of quotes.

        Parameters
        ----------
        page : int, optional
            Page number to display. Defaults to 1.
        page_size : int, optional
            Number of rows per page. Defaults to 100.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self._build()
        self._page = page
        self._page_size = page_size
        self._reload()

    def refresh(self) -> None:
        """Reload the current page from the data source."""
        self._reload()

    def _reload(self) -> None:
        """Invoke the loader callback and refresh the table."""
        if self._load_page_callback is None:
            return

        result = self._load_page_callback(
            self._page, self._page_size, self._sort_col, self._sort_desc
        )
        data = result['data']

        if data is None:
            self.clear()
            ttk.Label(self, text='No data').grid(
                row=0, column=0, sticky='w'
            )
            return

        items = data['items']
        self._total_pages = data['total_pages']
        self._render_rows(items)
        self._update_pager()

    def _render_rows(self, items: List[Dict[str, Any]]) -> None:
        """Clear and repopulate the table with quote dicts."""
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
        """Update pager label text and Prev/Next button states."""
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
        """Advance to the next page and reload if not on last page."""
        if self._page < self._total_pages:
            self._page += 1
            self._reload()

    def prev_page(self) -> None:
        """Go back to the previous page if not on the first page."""
        if self._page > 1:
            self._page -= 1
            self._reload()

    def get_selected_ids(self) -> List[int]:
        """Return the IDs of all currently selected table rows.

        Returns
        -------
        list[int]
            Primary keys of the selected rows.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        ids = []
        for item in self.table.selection():
            values = self.table.item(item, 'values')
            if values:
                try:
                    ids.append(int(values[0]))
                except (ValueError, IndexError):
                    pass
        return ids

    def clear(self) -> None:
        """Destroy all child widgets, clearing the content area."""
        for widget in self.winfo_children():
            widget.destroy()
