"""
Light GUI theme color palette.

This module defines the default light color scheme
used by the application interface.
"""


from work.scripts.gui.theme._themes import ThemeTokens


LIGHT_COLORS = ThemeTokens(
    background="#F8FAFC",
    surface="#F8FAFC",
    border="#D6DCE2",

    text="#111827",
    text_secondary="#6B7280",

    accent="#2563EB",
    accent_hover="#1D4ED8",

    input_background="#FFFFFF",

    icon="#111827",

    button="#E5E7EB",
    button_hover="#D9DEE6",
    button_pressed="#CBD5E1",
    button_text="#111827",
    button_text_disabled="#9CA3AF",

    tooltip_background="#CCCCCC",
    tooltip_foreground="#000000",
    tooltip_border="#BBBBBB",
)
