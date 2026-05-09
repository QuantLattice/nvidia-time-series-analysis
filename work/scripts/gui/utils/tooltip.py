"""
Animated tooltip widget for Tkinter interfaces.

This module provides a reusable tooltip component with:
- fade-in and fade-out animations;
- theme token integration;
- automatic screen boundary positioning;
- support for arbitrary Tkinter widgets.

The tooltip system is designed for lightweight contextual
UI hints used throughout the application interface.
"""


import tkinter as tk
from typing import Optional, Tuple

from work.scripts.gui.theme import ThemeTokens


_FADE_IN_STEP = 0.1
_FADE_OUT_STEP = 0.1

_FADE_IN_DELAY_MS = 30
_FADE_OUT_DELAY_MS = 15

_TOOLTIP_PADDING_X = 6
_TOOLTIP_PADDING_Y = 6

_TOOLTIP_BORDER_PADDING_X = 1
_TOOLTIP_BORDER_PADDING_Y = 1


class ToolTip:
    """
    Animated tooltip widget bound to a Tkinter widget.

    The tooltip automatically appears when the user hovers
    over the target widget and disappears when the cursor
    leaves the widget area.

    Parameters
    ----------
    widget : tk.Widget
        Target widget associated with the tooltip.

    text : str
        Tooltip display text.

    colors : ThemeTokens
        Active GUI theme color tokens.

    font : Tuple[str, int]
        Tooltip font configuration.

    icon_size : int
        Reference icon size used for tooltip positioning.
    """

    def __init__(
        self,
        widget: tk.Widget,
        text: str,
        colors: ThemeTokens,
        font: Tuple[str, int],
        icon_size: int
    ) -> None:
        """
        Initialize tooltip bindings and visual settings.

        Parameters
        ----------
        widget : tk.Widget
            Target widget associated with the tooltip.

        text : str
            Tooltip display text.

        colors : ThemeTokens
            Active GUI theme color tokens.

        font : Tuple[str, int]
            Tooltip font configuration.

        icon_size : int
            Reference icon size used for tooltip positioning.
        """

        self.widget = widget
        self.text = text

        self.colors = colors
        self.font = font
        self.icon_size = icon_size

        self.tip_window: Optional[tk.Toplevel] = None
        self._fade_job: Optional[str] = None
        self._alpha: float = 0.0

        self.widget.bind(
            sequence="<Enter>",
            func=self._show
        )
        self.widget.bind(
            sequence="<Leave>",
            func=self._hide
        )

    # ---------------------------
    # VISIBILITY
    # ---------------------------

    def _show(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Display the tooltip window.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            Tkinter hover event.
        """

        if self.tip_window or not self.text:
            return

        self.tip_window = tooltip = tk.Toplevel(
            master=self.widget,
        )
        tooltip.wm_overrideredirect(boolean=True)
        tooltip.attributes("-alpha", 0.0)  # type: ignore

        border = tk.Frame(
            master=tooltip,
            background=self.colors.tooltip_border,
            padx=_TOOLTIP_BORDER_PADDING_X,
            pady=_TOOLTIP_BORDER_PADDING_Y,
        )
        border.pack()

        label = tk.Label(
            master=border,
            text=self.text,
            font=self.font,
            background=self.colors.tooltip_background,
            foreground=self.colors.tooltip_foreground,
            padx=_TOOLTIP_PADDING_X,
            pady=_TOOLTIP_PADDING_Y,

            relief="flat",
            borderwidth=0,
        )
        label.pack()

        tooltip.update_idletasks()

        x, y = self._calculate_position(tooltip=tooltip)

        tooltip.wm_geometry(newGeometry=f"+{x}+{y}")

        self._alpha = 0.0
        self._cancel_animation()
        self._fade_in()

    def _hide(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Hide the tooltip window.

        Parameters
        ----------
        event : Optional[tk.Event], optional
            Tkinter leave event.
        """

        if not self.tip_window:
            return

        self._cancel_animation()
        self._fade_out()

    # =========================
    # ANIMATION
    # =========================

    def _fade_in(self) -> None:
        """
        Animate tooltip fade-in transition.
        """

        if not self.tip_window:
            return

        self._alpha += _FADE_IN_STEP

        if self._alpha >= 1.0:
            self.tip_window.attributes("-alpha", 1.0)  # type: ignore
            self._fade_job = None
            return

        self.tip_window.attributes("-alpha", self._alpha)  # type: ignore

        self._fade_job = self.tip_window.after(
            ms=_FADE_IN_DELAY_MS,
            func=self._fade_in
        )

    def _fade_out(self) -> None:
        """
        Animate tooltip fade-out transition.
        """

        if not self.tip_window:
            return

        self._alpha -= _FADE_OUT_STEP

        if self._alpha <= 0:
            self.tip_window.destroy()
            self.tip_window = None
            self._fade_job = None
            return

        self.tip_window.attributes("-alpha", self._alpha)  # type: ignore

        self._fade_job = self.tip_window.after(
            ms=_FADE_OUT_DELAY_MS,
            func=self._fade_out
        )

    def _cancel_animation(self) -> None:
        """
        Cancel active tooltip animation job.
        """

        if not self._fade_job or not self.tip_window:
            return

        try:
            self.tip_window.after_cancel(id=self._fade_job)
        except tk.TclError as e:
            # Animation may already be destroyed during rapid hover events.
            print(e)

        self._fade_job = None

    # =========================
    # POSITIONING
    # =========================

    def _calculate_position(
        self,
        tooltip: tk.Toplevel,
    ) -> Tuple[int, int]:
        """
        Calculate tooltip screen position.

        Parameters
        ----------
        tooltip : tk.Toplevel
            Tooltip window instance.

        Returns
        -------
        Tuple[int, int]
            Tooltip screen coordinates.
        """

        screen_width = tooltip.winfo_screenwidth()
        screen_height = tooltip.winfo_screenheight()

        tooltip_width = tooltip.winfo_reqwidth()
        tooltip_height = tooltip.winfo_reqheight()

        widget_x = self.widget.winfo_rootx()
        widget_y = self.widget.winfo_rooty()

        widget_width = self.widget.winfo_width()

        offset = -self.font[1] * 2 + _TOOLTIP_BORDER_PADDING_X

        x = widget_x + widget_width + offset
        y = widget_y + self.icon_size + _TOOLTIP_PADDING_X * 2

        if x + tooltip_width > screen_width:
            x = widget_x - tooltip_width - offset

        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height - offset

        return x, y
