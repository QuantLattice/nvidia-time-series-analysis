"""
Public API for the plotting framework.

This module defines the main entry point of the plotting system,
providing access to session management, layer composition, and
rendering orchestration utilities.

It serves as a high-level interface over the internal plotting
architecture, which is composed of:

Orchestration layer
    PlotSession and LayerStack, responsible for building and managing
    plot composition before rendering.

Layer system
    Composable visualization primitives that define rendering logic
    for numerical and categorical data.

Configuration layer
    ChartConfig, FigureConfig, and style objects controlling visual
    appearance and layout behavior.

Contract layer
    Abstract interfaces and shared types defining rendering semantics
    across all components.

Design goals
------------
- provide a stable and minimal public API surface;
- separate composition, configuration, and rendering concerns;
- ensure backend-independent plot construction;
- support composable multi-layer visualizations.

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
    HistogramStyle
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

    "BaseLayer",
    "CategoricalLayer",
    "NumericalLayer",
    "LineLayer",
    "FillBetweenLayer",
    "ScatterLayer",
    "BarLayer",
    "BoxLayer",
    "HistogramLayer"
]
