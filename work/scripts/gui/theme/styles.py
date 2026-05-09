"""
Named ttk style identifiers used by the GUI layer.

This module centralizes custom ttk style names to avoid
hardcoded string literals across the interface codebase.
"""


from enum import StrEnum


class StyleName(StrEnum):
    """
    Custom ttk widget style identifiers.

    Attributes
    ----------
    FLAT_BUTTON : str
        Borderless flat button style.

    PANEL_LABEL : str
        Label style used in side panels and context sections.
    """

    FLAT_BUTTON = "Flat.TButton"

    PANEL_LABEL = "Panel.TLabel"
