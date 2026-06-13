"""
Base and fundamental layer style dataclasses.

This module defines the foundational visual styling primitives
used across the plotting framework.

- LayerStyle: base styling attributes shared by all layers
- LineStyle: styling for continuous line-based plots
- ScatterStyle: styling for point-based plots

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Optional

from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle,
)


# ------------------------------------------------------------------
# Base styles
# ------------------------------------------------------------------

@dataclass(slots=True)
class LayerStyle:
    """
    Base visual style shared by all plot layer types.

    This class defines common styling attributes that are applicable
    to all visualization primitives.

    Attributes
    ----------
    color : Optional[str]
        Primary color of the layer.

    label : Optional[str]
        Legend label associated with the layer.

    zorder : Optional[int]
        Drawing order relative to other layers.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    color: Optional[str] = None
    label: Optional[str] = None
    zorder: Optional[int] = None


# ------------------------------------------------------------------
# Line-based styles
# ------------------------------------------------------------------

@dataclass(slots=True)
class LineStyle(LayerStyle):
    """
    Style configuration for line-based plot layers.

    Used for continuous data representations such as line plots,
    time series, and mathematical functions.

    Attributes
    ----------
    linestyle : Optional[LineStyleLiteral]
        Line pattern (e.g. solid, dashed, dotted).

    linewidth : Optional[float]
        Thickness of the line.

    marker : Optional[MarkerStyle]
        Marker style for data points.

    markersize : Optional[float]
        Size of markers.

    alpha : Optional[float]
        Transparency level of the line.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    linestyle: Optional[LineStyleLiteral] = None
    linewidth: Optional[float] = None

    marker: Optional[MarkerStyle] = None
    markersize: Optional[float] = None

    alpha: Optional[float] = None


@dataclass(slots=True)
class ScatterStyle(LayerStyle):
    """
    Style configuration for scatter plot layers.

    Used for point-based visualizations where each data point
    is rendered independently.

    Attributes
    ----------
    edgecolor : Optional[str]
        Color of point edges.

    linestyle : Optional[LineStyleLiteral]
        Edge line style.

    linewidth : Optional[float]
        Edge thickness.

    marker : Optional[MarkerStyle]
        Shape of scatter points.

    markersize : Optional[float]
        Size of scatter points.

    hatch : Optional[HatchStyle]
        Pattern fill for markers (if supported).

    alpha : Optional[float]
        Transparency level of points.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    edgecolor: Optional[str] = None

    linestyle: Optional[LineStyleLiteral] = None
    linewidth: Optional[float] = None

    marker: Optional[MarkerStyle] = None
    markersize: Optional[float] = None

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None
