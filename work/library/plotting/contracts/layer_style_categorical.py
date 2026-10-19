"""
Categorical and distribution layer style dataclasses.

This module defines visual styling for area, bar, box, and
histogram plot layer types.

- FillBetweenStyle: styling for filled area plots
- BarStyle: styling for categorical bar plots
- BoxStyle: styling for statistical box plots
- HistogramStyle: styling for histogram plots

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Optional

from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle,
)
from .layer_style_base import LayerStyle


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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    edgecolor: Optional[str] = None

    hatch: Optional[HatchStyle] = None

    alpha: Optional[float] = None
