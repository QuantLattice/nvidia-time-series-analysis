"""
Plot rendering context definitions.

This module defines the plotting context object shared between
plot sessions, renderers, and plot layers.

The context encapsulates the Matplotlib objects required during
rendering and provides a unified access point to the active figure
and axes.

Notes
-----
A plotting context is typically created by a plotting session and
passed through the rendering pipeline. It allows renderers and
layers to operate without managing figure creation directly.
"""


from dataclasses import dataclass

from matplotlib.axes import Axes
from matplotlib.figure import Figure


@dataclass(slots=True)
class PlotContext:
    """
    Rendering context for a plot session.

    This object groups together the Matplotlib components used
    during rendering.

    Attributes
    ----------
    figure : Figure
        Root Matplotlib figure that owns all axes.

    primary_axes : Axes
        Primary axes used for standard plot layers.

    overlay_axes : Axes
        Secondary axes used for overlay layers that require an
        independent y-axis scale.
    """

    figure: Figure
    primary_axes: Axes
    overlay_axes: Axes
