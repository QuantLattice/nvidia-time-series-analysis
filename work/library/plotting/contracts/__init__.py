"""
Plotting contracts and shared data structures.

This package defines configuration objects, rendering context
containers, and abstract interfaces used throughout the plotting
subsystem.

Provided contracts include:

- figure-level configuration;
- chart-level configuration;
- rendering context objects;
- plot layer abstractions;
- layer placement definitions.

The contracts are intentionally lightweight and independent from
specific plotting implementations, allowing different rendering
backends and layer types to share a common API.
"""


from .config import (
    FigureConfig,
    ChartConfig
)
from .layer import (
    LayerPlacement,
    PlotLayer
)
from .plot_context import (
    PlotContext
)


__all__ = [
    "FigureConfig",
    "ChartConfig",
    "LayerPlacement",
    "PlotLayer",
    "PlotContext"
]
