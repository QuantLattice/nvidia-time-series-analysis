"""
Special-purpose layer style dataclasses.

This module defines visual styling for heatmap and financial
candlestick plot layer types.

- HeatmapStyle: styling for matrix-based heatmap plots
- CandlestickStyle: styling for financial candlestick plots

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Optional

from .types import (
    LineStyleLiteral,
    HatchStyle,
    ColormapLiteral,
)


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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
