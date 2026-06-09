"""
Calendar date picker popup.

Header layout:  [<]  Month  [Year spinbox]  [>]
  < / >      — navigate months
  year spin  — type or spin to any year directly
"""

import tkinter as tk
from tkinter import ttk
import calendar as _cal
from datetime import date
from typing import Callable, Optional


class CalendarPopup(tk.Toplevel):
    """
    Modal popup for selecting a calendar date.

    The header shows the current month name on the left and an editable
    year Spinbox on the right, flanked by prev/next month arrow buttons.
    Year can be changed by spinning or typing directly — no external
    widget needed.

    Parameters
    ----------
    parent : tk.Widget
        Parent widget used for positioning and modal grab.
    initial_date : Optional[date]
        Date highlighted when the popup opens. Defaults to today.
    on_select : Optional[Callable[[date], None]]
        Called with the chosen date when the user clicks a day.
    """

    def __init__(
        self,
        parent: tk.Widget,
        initial_date: Optional[date] = None,
        on_select: Optional[Callable[[date], None]] = None,
    ) -> None:
        super().__init__(parent)

        today = date.today()
        self._selected = initial_date or today
        self._year = self._selected.year
        self._month = self._selected.month
        self._on_select = on_select

        self.title("Select date")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._build()
        self._center(parent)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", padx=6, pady=(6, 2))

        ttk.Button(
            header, text="<", width=2, command=self._prev_month
        ).pack(side="left")

        # Month label — fixed width so the popup doesn't resize while navigating
        self._month_label = ttk.Label(header, text="", width=10, anchor="e")
        self._month_label.pack(side="left", padx=(4, 0))

        # Year spinbox — editable inline, range 1900-2100
        self._year_spin = ttk.Spinbox(
            header,
            from_=1900,
            to=2100,
            width=5,
            command=self._on_year_spin,
        )
        self._year_spin.set(str(self._year))
        self._year_spin.bind("<Return>", lambda _: self._on_year_spin())
        self._year_spin.bind("<FocusOut>", lambda _: self._on_year_spin())
        self._year_spin.pack(side="left", padx=(4, 0))

        ttk.Button(
            header, text=">", width=2, command=self._next_month
        ).pack(side="right")

        self._grid_frame = ttk.Frame(self)
        self._grid_frame.pack(padx=6, pady=(4, 6))

        self._render_grid()

    def _render_grid(self) -> None:
        for widget in self._grid_frame.winfo_children():
            widget.destroy()

        self._month_label.configure(text=_cal.month_abbr[self._month])

        for col, name in enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]):
            ttk.Label(
                self._grid_frame, text=name, width=4, anchor="center"
            ).grid(row=0, column=col)

        for row_i, week in enumerate(
            _cal.monthcalendar(self._year, self._month), start=1
        ):
            for col_i, day in enumerate(week):
                if day == 0:
                    ttk.Label(self._grid_frame, text="", width=4).grid(
                        row=row_i, column=col_i
                    )
                    continue

                is_selected = (
                    day == self._selected.day
                    and self._month == self._selected.month
                    and self._year == self._selected.year
                )
                btn = ttk.Button(
                    self._grid_frame,
                    text=str(day),
                    width=4,
                    command=lambda d=day: self._pick(d),
                )
                if is_selected:
                    btn.state(["pressed"])
                btn.grid(row=row_i, column=col_i, padx=1, pady=1)

    def _center(self, parent: tk.Widget) -> None:
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        w = self.winfo_width()
        h = self.winfo_height()
        self.geometry(f"+{px - w // 2}+{py - h // 2}")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _prev_month(self) -> None:
        if self._month == 1:
            self._month = 12
            self._year -= 1
            self._year_spin.set(str(self._year))
        else:
            self._month -= 1
        self._render_grid()

    def _next_month(self) -> None:
        if self._month == 12:
            self._month = 1
            self._year += 1
            self._year_spin.set(str(self._year))
        else:
            self._month += 1
        self._render_grid()

    def _on_year_spin(self) -> None:
        """Update the grid when the user changes the year via the spinbox."""
        try:
            year = int(self._year_spin.get())
        except ValueError:
            return
        if 1900 <= year <= 2100 and year != self._year:
            self._year = year
            self._render_grid()

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

    def _pick(self, day: int) -> None:
        chosen = date(self._year, self._month, day)
        if self._on_select is not None:
            self._on_select(chosen)
        self.destroy()
