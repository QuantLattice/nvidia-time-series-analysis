"""
Plotting contracts and shared data structures.

This package defines immutable configuration objects and abstract
interfaces used throughout the plotting subsystem.

It provides the core contracts required for:
- figure configuration;
- chart metadata;
- plot layer definitions;
- rendering and composition pipelines.

The contracts in this package are intentionally lightweight and
framework-agnostic so they can be reused by different rendering
backends and chart composition layers.
"""


from .config import (
    FigureConfig,
    ChartConfig
)
from .layer import (
    LayerPlacement,
    PlotLayer
)


__all__ = [
    "FigureConfig",
    "ChartConfig",
    "LayerPlacement",
    "PlotLayer",
]
