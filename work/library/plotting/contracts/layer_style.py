"""
Definition of visual styling primitives for plot layers.

This module provides a hierarchy of dataclasses describing visual
appearance for different types of plot layers used in the rendering
system.

The style system is organized as follows:

- LayerStyle: base styling attributes shared by all layers
- LineStyle: styling for continuous line-based plots
- ScatterStyle: styling for point-based plots
- FillBetweenStyle: styling for filled area plots
- BarStyle: styling for categorical bar plots
- BoxStyle: styling for statistical box plots
- HistogramStyle: styling for histogram plots

All style classes are designed as lightweight configuration objects
and are consumed by the rendering backend (e.g. MatplotlibRenderer).
"""


from dataclasses import dataclass
from typing import Optional

from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle
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
    """

    edgecolor: Optional[str] = None

    linestyle: Optional[LineStyleLiteral] = None
    linewidth: Optional[float] = None

    marker: Optional[MarkerStyle] = None
    markersize: Optional[float] = None

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None


# ------------------------------------------------------------------
# Area styles
# ------------------------------------------------------------------

@dataclass(slots=True)
class FillBetweenStyle(LayerStyle):
    """
    Style configuration for filled area plots.

    Used for visualizing areas between curves or bounds.

    Attributes
    ----------
    hatch : Optional[HatchStyle]
        Fill pattern.

    alpha : Optional[float]
        Transparency level of filled region.
    """

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None


# ------------------------------------------------------------------
# Categorical styles
# ------------------------------------------------------------------

@dataclass(slots=True)
class BarStyle(LayerStyle):
    """
    Style configuration for bar chart layers.

    Used for categorical data visualization with rectangular bars.

    Attributes
    ----------
    edgecolor : Optional[str]
        Color of bar edges.

    linewidth : Optional[float]
        Thickness of bar edges.

    hatch : Optional[HatchStyle]
        Pattern fill for bars.

    alpha : Optional[float]
        Transparency level of bars.
    """

    edgecolor: Optional[str] = None

    linewidth: Optional[float] = None

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None


# ------------------------------------------------------------------
# Distribution styles
# ------------------------------------------------------------------

@dataclass(slots=True)
class BoxStyle(LayerStyle):
    """
    Style configuration for box plot layers.

    Used for statistical distribution visualization (quartiles,
    medians, outliers).

    Attributes
    ----------
    edgecolor : Optional[str]
        Color of box edges.

    linestyle : Optional[LineStyleLiteral]
        Style of box borders.

    linewidth : Optional[float]
        Thickness of box borders.

    marker : Optional[MarkerStyle]
        Style of outlier markers.

    markersize : Optional[float]
        Size of outlier markers.

    hatch : Optional[HatchStyle]
        Fill pattern of the box.

    showfliers : Optional[bool]
        Whether to display outliers.
    """

    edgecolor: Optional[str] = None

    linestyle: Optional[LineStyleLiteral] = None
    linewidth: Optional[float] = None

    marker: Optional[MarkerStyle] = None
    markersize: Optional[float] = None

    hatch: Optional[HatchStyle] = None

    showfliers: Optional[bool] = None


@dataclass(slots=True)
class HistogramStyle(LayerStyle):
    """
    Style configuration for histogram layers.

    Used for frequency distribution visualization.

    Attributes
    ----------
    edgecolor : Optional[str]
        Color of bin edges.

    hatch : Optional[HatchStyle]
        Pattern fill for histogram bars.

    alpha : Optional[float]
        Transparency level of histogram bars.
    """

    edgecolor: Optional[str] = None

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None
