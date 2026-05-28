"""
UI binding layer between Tkinter widgets and application state.

This module provides a lightweight data-binding mechanism that synchronizes
Tkinter UI widgets with the global AppState. It is responsible for keeping
GUI input fields and in-memory state consistent during runtime.
"""


from tkinter import ttk, Event

from work.scripts.core import AppState


class UIBinder:
    """
    Lightweight UI-to-state binding service.

    This class acts as an adapter between Tkinter widgets and the
    application state container. It provides simple two-way binding
    for form-like UI components.

    Parameters
    ----------
    app_state : AppState
        Global application state instance.
    """

    def __init__(
        self,
        app_state: AppState
    ) -> None:
        """
        Initialize UI binder with shared application state.

        Parameters
        ----------
        app_state : AppState
            Runtime application state container.
        """

        self.app_state = app_state

    def bind_entry(
        self,
        entry: ttk.Entry,
        section: str,
        key: str
    ) -> None:
        """
        Bind a Tkinter Entry widget to application state.

        The widget value is synchronized with:
        app_state.ui_state.context_data[section][key]

        Parameters
        ----------
        entry : ttk.Entry
            Tkinter entry widget.

        section : str
            Logical section name in context data.

        key : str
            Key within the section dictionary.
        """

        state = self.app_state.ui_state

        value = state.context_data.get(section, {}).get(key, "")
        entry.insert(index=0, string=value)

        def on_change(event: Event):
            """
            Update application state on user input.
            """

            state.context_data.setdefault(section, {})[key] = entry.get()

        entry.bind(sequence="<KeyRelease>", func=on_change)
