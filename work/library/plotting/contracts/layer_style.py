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
- HeatmapStyle: styling for matrix-based heatmap plots
- CandlestickStyle: styling for financial candlestick plots

All style classes are designed as lightweight configuration objects
and are consumed by the rendering backend (e.g. MatplotlibRenderer).
"""


from dataclasses import dataclass
from typing import Optional

from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle,
    ColormapLiteral
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

    edge_linewidth : Optional[float]
        Thickness of bar edges.

    hatch : Optional[HatchStyle]
        Pattern fill for bars.

    alpha : Optional[float]
        Transparency level of bars.
    """

    edgecolor: Optional[str] = None

    edge_linewidth: Optional[float] = None

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


@dataclass(slots=True)
class HeatmapStyle:
    """
    Style configuration for heatmap layers.

    HeatmapStyle is intentionally independent from LayerStyle because
    matrix-based rendering uses an image-oriented pipeline rather than
    the primitive artist-based pipeline used by the other layer types.

    Attributes
    ----------
    cmap : Optional[ColormapLiteral]
        Colormap used to map values to colors.

    annotate : bool
        Whether to draw numeric annotations inside heatmap cells.

    annotation_format : str
        Format string used to display annotation values.

    annotation_color : Optional[str]
        Fixed annotation color. If not provided, the color is chosen
        automatically based on background brightness.

    show_colorbar : bool
        Whether to display a colorbar next to the heatmap.

    vmin : Optional[float]
        Lower bound for color normalization.

    vmax : Optional[float]
        Upper bound for color normalization.

    alpha : Optional[float]
        Global transparency of the heatmap image.
    """

    cmap: Optional[ColormapLiteral] = None

    annotate: bool = True
    annotation_format: str = ".2f"
    annotation_color: Optional[str] = None

    show_colorbar: bool = True

    vmin: Optional[float] = None
    vmax: Optional[float] = None

    alpha: Optional[float] = None


@dataclass(slots=True)
class CandlestickStyle:
    """
    Style configuration for financial candlestick layers.

    This style defines visual properties for open-high-low-close
    chart elements, including candle body colors, wick styling,
    outline appearance, and optional hatch patterns.

    Attributes
    ----------
    linestyle : Optional[LineStyleLiteral]
        Line style used for wicks and candle edges.

    edgecolor : Optional[str]
        Color of candle body edges.

    edge_linewidth : Optional[float]
        Width of the candle body edges.

    up_color : str
        Fill color used for bullish candles where close >= open.

    down_color : str
        Fill color used for bearish candles where close < open.

    wick_color : str
        Color of the candle wicks.

    wick_linewidth : float
        Line width used for the candle wicks.

    body_alpha : float
        Transparency level of the candle body.

    wick_alpha : Optional[float]
        Transparency level of the candle wicks.

    hatch : Optional[HatchStyle]
        Hatch pattern applied to the candle body.

    zorder : Optional[int]
        Drawing order relative to other layers.
    """

    linestyle: Optional[LineStyleLiteral] = None

    edgecolor: Optional[str] = None
    edge_linewidth: Optional[float] = None

    up_color: str = "green"
    down_color: str = "red"

    wick_color: str = "black"
    wick_linewidth: float = 1.0

    body_alpha: float = 0.8
    wick_alpha: Optional[float] = None

    hatch: Optional[HatchStyle] = None

    zorder: Optional[int] = None
