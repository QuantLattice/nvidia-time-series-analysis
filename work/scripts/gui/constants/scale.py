"""
UI scale presets for the graphical interface.

This module defines named scale tokens and their corresponding
font, icon, and spacing values.
"""


from dataclasses import dataclass


class ScaleTokensNames:
    """
    Available UI scale preset names.

    Attributes
    ----------
    SMALL : str
        Small UI scale preset.

    MEDIUM : str
        Default UI scale preset.

    BIG : str
        Large UI scale preset.

    VERY_BIG : str
        Extra large UI scale preset.
    """

    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"
    VERY_BIG = "very big"


@dataclass(slots=True)
class ScaleTokens:
    """
    UI scale configuration values.

    Attributes
    ----------
    font_size : int
        Base font size.

    icon_size : int
        Icon size in pixels.

    padding_x : int
        Horizontal padding.

    padding_y : int
        Vertical padding.
    """

    font_size: int
    icon_size: int
    padding_x: int
    padding_y: int


SCALE_PRESETS = {
    ScaleTokensNames.SMALL: ScaleTokens(
        font_size=8,
        icon_size=16,
        padding_x=4,
        padding_y=2,
    ),
    ScaleTokensNames.MEDIUM: ScaleTokens(
        font_size=10,
        icon_size=24,
        padding_x=6,
        padding_y=3,
    ),
    ScaleTokensNames.BIG: ScaleTokens(
        font_size=12,
        icon_size=32,
        padding_x=8,
        padding_y=4,
    ),
    ScaleTokensNames.VERY_BIG: ScaleTokens(
        font_size=14,
        icon_size=40,
        padding_x=10,
        padding_y=5,
    )
}


def resolve_ui_scale(scale_name: str) -> ScaleTokens:
    """
    Resolve UI scale preset by name.

    Parameters
    ----------
    scale_name : str
        Name of the requested UI scale preset.

    Returns
    -------
    ScaleTokens
        Matching scale preset. If the name is unknown, the medium
        preset is returned.
    """

    return SCALE_PRESETS.get(
        scale_name,
        SCALE_PRESETS[ScaleTokensNames.MEDIUM]
    )
