"""
Public API for the plotting framework.

This module defines the main entry point of the plotting system,
providing access to session management, layer composition, and
rendering orchestration utilities.

It exposes a high-level interface over the internal layered
rendering architecture.

Architecture
------------
The plotting system is composed of four core subsystems:

Orchestration layer
    PlotSession and LayerStack, responsible for constructing and
    managing plot compositions prior to rendering.

Layer system
    Composable visualization primitives defining rendering behavior
    for multiple data domains, including numerical, categorical,
    matrix-based, and financial visualizations.

Configuration system
    ChartConfig, FigureConfig, and style objects controlling visual
    appearance, layout, and rendering options.

Contract system
    Abstract interfaces and shared types defining rendering semantics,
    placement rules, and styling contracts.

Design goals
------------
- provide a stable and minimal public API surface;
- separate composition, configuration, and rendering concerns;
- support backend-independent plot construction;
- enable composable multi-layer visualizations across data domains.

Notes
-----
This package is intended as the primary import target for users
building plots using the layered rendering system.
"""


from .stack import (
    LayerStack
)
from .session import (
    PlotSession
)
from .contracts import (
    LayerPlacement,
    FigureConfig,
    ChartConfig,
    LineStyle,
    ScatterStyle,
    FillBetweenStyle,
    BarStyle,
    BoxStyle,
    HistogramStyle,
    HeatmapStyle,
    CandlestickStyle
)
from .layers import (
    BaseLayer,
    CategoricalLayer,
    NumericalLayer,
    LineLayer,
    FillBetweenLayer,
    ScatterLayer,
    BarLayer,
    BoxLayer,
    HistogramLayer,
    HeatmapLayer,
    CandlestickLayer
)


__all__ = [
    "LayerStack",

    "PlotSession",

    "LayerPlacement",
    "FigureConfig",
    "ChartConfig",
    "LineStyle",
    "ScatterStyle",
    "FillBetweenStyle",
    "BarStyle",
    "BoxStyle",
    "HistogramStyle",
    "HeatmapStyle",
    "CandlestickStyle",

    "BaseLayer",
    "CategoricalLayer",
    "NumericalLayer",
    "LineLayer",
    "FillBetweenLayer",
    "ScatterLayer",
    "BarLayer",
    "BoxLayer",
    "HistogramLayer",
    "HeatmapLayer",
    "CandlestickLayer"
]
