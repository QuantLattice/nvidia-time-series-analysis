"""
Theme color token definitions.

This module defines immutable color token structures
used by the GUI theme system for ttk styling and
application-wide visual consistency.
"""


from dataclasses import dataclass


@dataclass(slots=True)
class ThemeTokens:
    """
    Immutable GUI theme color palette.

    The token structure centralizes all colors used by
    the application interface, including backgrounds,
    typography, buttons, inputs, icons, and tooltip styles.

    Attributes
    ----------
    background : str
        Main application background color.

    surface : str
        Secondary surface color for panels and containers.

    border : str
        Border color used for frames and separators.

    text : str
        Primary text color.

    text_secondary : str
        Secondary or muted text color.

    accent : str
        Main accent color used for highlights and active elements.

    accent_hover : str
        Accent color used for hover states.

    input_background : str
        Background color for input controls.

    icon : str
        Default icon color.

    button : str
        Button background color.

    button_hover : str
        Button background color on hover.

    button_pressed : str
        Button background color when pressed.

    button_text : str
        Button text color.

    button_text_disabled : str
        Disabled button text color.

    tooltip_background : str
        Tooltip background color.

    tooltip_foreground : str
        Tooltip text color.

    tooltip_border : str
        Tooltip border color.
    """

    background: str
    surface: str
    border: str

    text: str
    text_secondary: str

    accent: str
    accent_hover: str

    input_background: str

    icon: str

    button: str
    button_hover: str
    button_pressed: str
    button_text: str
    button_text_disabled: str

    tooltip_background: str
    tooltip_foreground: str
    tooltip_border: str
