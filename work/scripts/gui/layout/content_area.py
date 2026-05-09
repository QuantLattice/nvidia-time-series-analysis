"""
Main content display area.

This module defines the central content container used to show
tables, reports, charts, or placeholder text depending on the
active application section.
"""


from tkinter import ttk, Tk


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

        super().__init__(master=parent, style="App.TFrame")

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

    def clear(self) -> None:
        """
        Remove all widgets from the content area.
        """

        for widget in self.winfo_children():
            widget.destroy()
