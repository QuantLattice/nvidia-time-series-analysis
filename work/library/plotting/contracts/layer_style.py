"""
Re-export facade for all layer style dataclasses.

This module exists for backwards compatibility so that existing code
using ``from .layer_style import <ClassName>`` continues to work
without modification.

All style classes are defined in the following submodules:

- layer_style_base: LayerStyle, LineStyle, ScatterStyle
- layer_style_categorical: FillBetweenStyle, BarStyle, BoxStyle,
  HistogramStyle
- layer_style_special: HeatmapStyle, CandlestickStyle

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from .layer_style_base import (
    LayerStyle,
    LineStyle,
    ScatterStyle,
)
from .layer_style_categorical import (
    FillBetweenStyle,
    BarStyle,
    BoxStyle,
    HistogramStyle,
)
from .layer_style_special import (
    HeatmapStyle,
    CandlestickStyle,
)

__all__ = [
    "LayerStyle",
    "LineStyle",
    "ScatterStyle",
    "FillBetweenStyle",
    "BarStyle",
    "BoxStyle",
    "HistogramStyle",
    "HeatmapStyle",
    "CandlestickStyle",
]
