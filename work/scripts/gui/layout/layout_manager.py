"""
Grid-based layout management system for the main GUI window.

This module defines a declarative layout system that organizes
application widgets into structured rows using Tkinter's grid geometry
manager.

The system supports:
- declarative layout definition;
- dynamic show/hide of UI sections;
- optional separators between layout regions;
- weighted row resizing.
"""


from dataclasses import dataclass
from tkinter import Tk, Widget, ttk
from enum import StrEnum
from typing import Dict, List, Optional


class LayoutKey(StrEnum):
    """
    Identifiers for main layout regions.

    Attributes
    ----------
    MENU : str
        Top application menu bar region.

    TOOLBAR : str
        Secondary toolbar region.

    CONTEXT : str
        Context or navigation panel region.

    CONTENT : str
        Main content display region.
    """

    MENU = "menu"
    TOOLBAR = "toolbar"
    CONTEXT = "context"
    CONTENT = "content"


@dataclass(slots=True)
class LayoutRow:
    """
    Declarative configuration of a layout row.

    Each row defines how a GUI region should be placed in the grid
    layout, including visibility, spacing, and resizing behavior.

    Attributes
    ----------
    name : LayoutKey
        Identifier of the widget region.

    weight : int, default=0
        Row weight for vertical resizing behavior.

    sticky : str, default="ew"
        Tkinter grid sticky option.

    separator : bool, default=True
        Whether to place a visual separator after this row.

    visible : bool, default=True
        Initial visibility state of the row.
    """

    name: LayoutKey
    weight: int = 0
    sticky: str = "ew"
    separator: bool = True
    visible: bool = True


@dataclass(slots=True)
class LayoutItem:
    """
    Runtime representation of a placed layout element.

    Attributes
    ----------
    widget : Widget
        Tkinter widget assigned to this layout slot.

    row : int
        Grid row index of the widget.

    sticky : str
        Grid sticky configuration.

    separator : Optional[Widget]
        Optional separator widget following the row.

    separator_row : Optional[int]
        Grid row index of the separator.
    """

    widget: Widget
    row: int
    sticky: str
    separator: Optional[Widget] = None
    separator_row: Optional[int] = None


class LayoutManager:
    """
    Central manager for application GUI layout.

    The LayoutManager is responsible for:
    - registering GUI sections (widgets);
    - building a structured grid layout;
    - managing visibility of layout regions;
    - inserting separators between logical UI blocks.

    Parameters
    ----------
    root : Tk
        Root application window.

    Notes
    -----
    The layout is defined using LayoutRow descriptors and is applied
    sequentially to a single-column grid system.
    """

    def __init__(
        self,
        root: Tk
    ) -> None:
        """
        Initialize layout manager.

        Parameters
        ----------
        root : Tk
            Root application window used as layout container.

        Notes
        -----
        The manager stores:
        - registered widgets mapped by LayoutKey;
        - runtime layout items with grid metadata.
        """

        self.root = root
        self.widgets: Dict[LayoutKey, Widget] = {}
        self.items: Dict[LayoutKey, LayoutItem] = {}

    def register(
        self,
        name: LayoutKey,
        widget: Widget
    ) -> None:
        """
        Register a widget under a layout key.

        Parameters
        ----------
        name : LayoutKey
            Layout region identifier.

        widget : Widget
            Tkinter widget to be managed.
        """

        self.widgets[name] = widget

    def build(
        self,
        rows: List[LayoutRow]
    ) -> None:
        """
        Construct the GUI layout based on provided layout rows.

        Parameters
        ----------
        rows : list[LayoutRow]
            Ordered list of layout definitions.

        Notes
        -----
        Each row may optionally include a separator widget. Rows are placed
        sequentially in a single-column grid layout.
        """

        current_row = 0

        for row in rows:
            widget = self.widgets[row.name]
            widget.grid(row=current_row, column=0, sticky=row.sticky)

            if row.weight:
                self.root.grid_rowconfigure(
                    index=current_row,
                    weight=row.weight
                )

            separator_widget = None
            separator_row = None

            if row.separator:
                separator_row = current_row + 1
                separator_widget = ttk.Separator(
                    master=self.root,
                    orient="horizontal"
                )
                separator_widget.grid(row=separator_row, column=0, sticky="ew")

            if not row.visible:
                widget.grid_remove()
                if separator_widget is not None:
                    separator_widget.grid_remove()

            self.items[row.name] = LayoutItem(
                widget=widget,
                row=current_row,
                sticky=row.sticky,
                separator=separator_widget,
                separator_row=separator_row,
            )

            current_row += 1 + (1 if row.separator else 0)

        self.root.grid_columnconfigure(index=0, weight=1)

    # -----------------------
    # visibility control
    # -----------------------

    def show(
        self,
        name: LayoutKey
    ) -> None:
        """
        Show a previously hidden layout section.

        Parameters
        ----------
        name : LayoutKey
            Layout region to display.
        """

        item = self.items[name]

        item.widget.grid(row=item.row, column=0, sticky=item.sticky)

        if item.separator is not None and item.separator_row is not None:
            item.separator.grid(row=item.separator_row, column=0, sticky="ew")

    def hide(
        self,
        name: LayoutKey
    ) -> None:
        """
        Hide a layout section without destroying its widget.

        Parameters
        ----------
        name : LayoutKey
            Layout region to hide.
        """

        item = self.items[name]
        item.widget.grid_remove()

        if item.separator is not None:
            item.separator.grid_remove()
