"""
Public API for the plotting contracts subsystem.

This package defines the core abstractions, configuration objects,
and type constraints used across the plotting framework.

It serves as a stable interface boundary between:

- plot composition logic (layers and placement);
- rendering backend implementations;
- session-level orchestration;
- shared configuration and styling structures.

Architecture
------------
The contracts system is organized into the following layers:

Configuration layer
    FigureConfig, ChartConfig, AxisVisibilityConfig, ChartStyle

Rendering context layer
    PlotContext

Layer abstraction layer
    PlotLayer, LayerPlacement

Styling layer
    LayerStyle and specialized style variants for different plot types

Type constraints layer
    Literal types defining Matplotlib-compatible styling options

Notes
-----
These contracts are intentionally independent of any rendering
implementation and can be reused across different backends.
"""


from .config import (
    FigureConfig,
    ChartConfig,
    AxisVisibilityConfig,
    ChartStyle
)
from .layer import (
    LayerPlacement,
    PlotLayer
)
from .plot_context import (
    PlotContext
)
from .layer_style import (
    LayerStyle,
    LineStyle,
    ScatterStyle,
    FillBetweenStyle,
    BarStyle,
    BoxStyle,
    HistogramStyle,
    HeatmapStyle
)
from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle,
    ColormapLiteral
)


__all__ = [
    "FigureConfig",
    "ChartConfig",
    "AxisVisibilityConfig",
    "ChartStyle",
    "LayerPlacement",
    "PlotLayer",
    "PlotContext",

    "LayerStyle",
    "LineStyle",
    "ScatterStyle",
    "FillBetweenStyle",
    "BarStyle",
    "BoxStyle",
    "HistogramStyle",
    "HeatmapStyle",

    "LineStyleLiteral",
    "MarkerStyle",
    "HatchStyle",
    "ColormapLiteral"
]
