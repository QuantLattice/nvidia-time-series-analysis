"""
Theme registry for the graphical interface.

This module defines available theme names and maps them to
the corresponding color token collections.
"""


from enum import StrEnum
from typing import Dict

from work.scripts.gui.theme._themes import (
    DARK_COLORS,
    LIGHT_COLORS,
    ThemeTokens
)


class ThemeName(StrEnum):
    """
    Supported GUI theme names.

    Attributes
    ----------
    DARK : str
        Dark theme identifier.

    LIGHT : str
        Light theme identifier.
    """

    DARK = "dark"
    LIGHT = "light"


THEMES: Dict[ThemeName, ThemeTokens] = {
    ThemeName.DARK: DARK_COLORS,
    ThemeName.LIGHT: LIGHT_COLORS,
}
