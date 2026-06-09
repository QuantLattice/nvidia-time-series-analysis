"""
Context panel component.

This module implements the side panel that changes its content
depending on the currently active application section.
"""


from tkinter import ttk, Tk
from typing import Callable

from work.scripts.core import AppState
from work.scripts.gui.factories import UIFactory
from work.scripts.gui.services.translator import Translator


class ContextPanel(ttk.Frame):
    """
    Side panel that renders controls for the active section.

    Parameters
    ----------
    parent : Tk
        Root application window.

    ui_factory : UIFactory
        Factory used to create themed UI controls.

    app_state : AppState
        Shared runtime application state.
    """

    def __init__(
        self,
        parent: Tk,
        ui_factory: UIFactory,
        app_state: AppState,
        on_import_csv: Callable[[], None],
        on_export_csv: Callable[[], None],
        translator: Translator
    ) -> None:
        """
        Initialize the context panel.

        Parameters
        ----------
        parent : Tk
            Root application window.

        ui_factory : UIFactory
            Factory used to create themed UI controls.

        app_state : AppState
            Shared runtime application state.
        """

        super().__init__(parent)

        self.ui_factory = ui_factory
        self.app_state = app_state
        self.on_import_csv = on_import_csv
        self.on_export_csv = on_export_csv
        self.translator = translator

    def render(
        self,
        section: str
    ) -> None:
        """
        Render controls for the requested section.

        Parameters
        ----------
        section : str
            Active application section identifier.
        """

        for widget in self.winfo_children():
            widget.destroy()

        if section == "data":
            self._build_data()
        elif section == "analysis":
            self._build_analysis()
        elif section == "reports":
            self._build_reports()

    def _build_data(self) -> None:
        """
        Build data section controls.
        """

        actions = ttk.Frame(self)
        actions.pack(anchor="w")

        data = self.translator.get_data().context_panel

        self.ui_factory.text_button(
            parent=actions,
            text=data.import_csv_text,
            command=self.on_import_csv,
        ).pack(side="left", padx=5, pady=5)

        self.ui_factory.text_button(
            parent=actions,
            text=data.export_csv_text,
            command=self.on_export_csv,
        ).pack(side="left", padx=5, pady=5)

    def _build_analysis(self) -> None:
        """
        Build analysis section controls.
        """

        state = self.app_state.ui_state

        ttk.Label(
            master=self,
            text="Analysis parameters"
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        form = ttk.Frame(master=self)
        form.grid(row=1, column=0, sticky="w")

        form.columnconfigure(0, weight=0)
        form.columnconfigure(1, weight=1)

        # Start Date
        ttk.Label(
            master=form,
            text="Start Date"
        ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=2)

        start_entry = self.ui_factory.bound_entry(
            parent=form,
            section="analysis",
            key="start_date"
        )
        start_entry.grid(
            row=0,
            column=1,
            sticky="w",
            pady=2
        )

        # End Date
        ttk.Label(
            master=form,
            text="End Date"
        ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=2)

        end_entry = self.ui_factory.bound_entry(
            parent=form,
            section="analysis",
            key="end_date"
        )
        end_entry.grid(
            row=1,
            column=1,
            sticky="w",
            pady=2
        )

        self.ui_factory.text_button(
            parent=form,
            text="Run Analysis",
            command=lambda: print(state.context_data.get("analysis"))
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _build_reports(self) -> None:
        """
        Build reports section controls.
        """

        data = self.translator.get_data().context_panel

        ttk.Label(master=self, text="Reports").pack(anchor="w")

        self.ui_factory.text_button(
            parent=self,
            text=data.export_csv_text,
            command=self.on_export_csv
        ).pack(side="left", padx=5, pady=5)

        self.ui_factory.text_button(
            parent=self,
            text="Export PNG",
            command=lambda: print("Export PNG")
        ).pack(side="left", padx=5, pady=5)
