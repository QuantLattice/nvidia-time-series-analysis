"""
Plot rendering context for the layered visualization system.

This module defines the `PlotContext` object used as a shared runtime
container during plot rendering.

The context encapsulates Matplotlib primitives (figure and axes)
and is passed through the rendering pipeline from the plotting session
to renderers and plot layers.

It provides a unified interface for accessing the active figure,
primary axes, and optional overlay axes used for multi-axis visualizations.

Notes
-----
The context is owned by the plotting session and consumed by renderers.
It does not manage lifecycle events such as figure creation or teardown.
"""


from dataclasses import dataclass
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Optional


@dataclass(slots=True)
class PlotContext:
    """
    Runtime context for plot rendering operations.

    The plotting context groups Matplotlib objects required during
    rendering and provides a shared access point for renderers and
    plot layers.

    It represents the active state of a plot session and is passed
    through the rendering pipeline without modification.

    Attributes
    ----------
    figure : Figure
        Root Matplotlib figure containing all axes and artists.

    primary_axes : Axes
        Main axes used for rendering primary plot layers.

    overlay_axes : Optional[Axes]
        Optional secondary axes used for overlay visualizations,
        typically for independent y-axis scaling.

    Notes
    -----
    - The context is created by a plotting session.
    - Renderers must treat it as read-only.
    - Axes objects are assumed to be already initialized.
    """

    figure: Figure
    primary_axes: Axes
    overlay_axes: Optional[Axes] = None
