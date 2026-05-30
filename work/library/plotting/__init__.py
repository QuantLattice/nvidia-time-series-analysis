"""
Core plotting session and layer stack utilities.

This package provides the orchestration layer for the plotting
subsystem.

It exposes:
- LayerStack for managing plot layer collections;
- PlotSession for building and rendering charts.

The package is responsible for:
- collecting plot layers;
- storing chart-level metadata;
- coordinating rendering through a configured backend.
"""


from .stack import (
    LayerStack
)
from .session import (
    PlotSession
)


__all__ = [
    "LayerStack",
    "PlotSession"
]
