"""
GUI constants package.

This package contains shared constants used by the graphical interface,
including language labels, UI scale presets, and window sizes.
"""


from .i18n import LANGUAGES
from .scale import resolve_ui_scale, ScaleTokensNames
from .window import MAIN_WINDOW_SIZE, FONT_SELECTOR_POPUP_SIZE


__all__ = [
    "LANGUAGES",
    "resolve_ui_scale",
    "ScaleTokensNames",
    "MAIN_WINDOW_SIZE",
    "FONT_SELECTOR_POPUP_SIZE"
]
