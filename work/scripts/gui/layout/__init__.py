"""
GUI layout system.

This package provides a grid-based layout manager and high-level UI
containers used to assemble the main application interface.

Components
----------
LayoutManager :
    Central controller for arranging application UI regions.

LayoutKey :
    Enum identifiers for layout sections.

LayoutRow :
    Declarative description of a single layout row.

ToolBar :
    Top toolbar component.

ContextPanel :
    Side context panel component.

MenuBar :
    Main application menu bar.

ContentArea :
    Central content display area.
"""


from .toolbar import ToolBar
from .context_panel import ContextPanel
from .menu_bar import MenuBar
from .content_area import ContentArea
from .layout_manager import LayoutManager, LayoutRow, LayoutKey


__all__ = [
    "LayoutManager",
    "LayoutKey",
    "LayoutRow",
    "ToolBar",
    "ContextPanel",
    "MenuBar",
    "ContentArea"
]
