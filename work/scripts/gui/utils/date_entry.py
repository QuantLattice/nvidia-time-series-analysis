"""
Date picker entry widget.

Compound widget: an Entry showing the date in ISO format paired with
a button that opens a CalendarPopup for visual date selection.
"""

import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
from typing import Callable, Optional


class DatePickerEntry(ttk.Frame):
    """
    Entry + calendar button for choosing a date.

    Parameters
    ----------
    parent : tk.Widget
        Parent widget.
    initial_date : Optional[date]
        Date shown on creation. Defaults to today.
    on_change : Optional[Callable[[date], None]]
        Called with the new date whenever the user picks one.
    """

    def __init__(
        self,
        parent: tk.Widget,
        initial_date: Optional[date] = None,
        on_change: Optional[Callable[[date], None]] = None,
        **frame_kwargs,
    ) -> None:
        super().__init__(parent, **frame_kwargs)

        self._date = initial_date or date.today()
        self._on_change = on_change
        self._var = tk.StringVar(value=self._date.isoformat())

        self._entry = ttk.Entry(self, textvariable=self._var, width=11)
        self._entry.pack(side="left")

        self._btn = ttk.Button(
            self, text="...", width=3, command=self._open_popup
        )
        self._btn.pack(side="left", padx=(2, 0))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_date(self) -> Optional[date]:
        """Return the currently displayed date, or None if the text is invalid."""
        try:
            return datetime.strptime(self._var.get().strip(), "%Y-%m-%d").date()
        except ValueError:
            return None

    def set_date(self, d: date) -> None:
        """Set the date value programmatically without firing on_change."""
        self._date = d
        self._var.set(d.isoformat())

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _open_popup(self) -> None:
        from work.scripts.gui.views.calendar_popup import CalendarPopup

        CalendarPopup(
            parent=self,
            initial_date=self.get_date() or self._date,
            on_select=self._on_selected,
        )

    def _on_selected(self, d: date) -> None:
        self._date = d
        self._var.set(d.isoformat())
        if self._on_change is not None:
            self._on_change(d)
