"""
Public API for the plotting contracts subsystem.

This package defines the core abstractions and configuration
objects used across the plotting framework.

It serves as a stable interface boundary between:

- plot composition logic (layers and placement);
- rendering backend implementations;
- session-level orchestration;
- shared configuration structures.

The design follows a strict separation of concerns:

Configuration layer
    FigureConfig, ChartConfig, AxisVisibilityConfig, ChartStyle

Rendering layer
    PlotContext

Layer abstraction layer
    PlotLayer, LayerPlacement

Styling layer
    LayerStyle and specialized style variants

Type constraints layer
    Literal types for Matplotlib-compatible styling options

Notes
-----
These contracts are intentionally backend-agnostic and do not
depend on any specific rendering implementation.
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
)
from .types import (
    LineStyleLiteral,
    MarkerStyle,
    HatchStyle
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

    "LineStyleLiteral",
    "MarkerStyle",
    "HatchStyle"
]
