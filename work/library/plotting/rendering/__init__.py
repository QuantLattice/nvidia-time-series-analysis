"""
Rendering backends for the plotting subsystem.

This package defines the rendering abstraction used to convert
plot layers into concrete Matplotlib figures.

It provides:
- a backend-agnostic renderer interface;
- a Matplotlib-based implementation for layered chart rendering.

The rendering layer is responsible for:
- composing figure objects;
- applying chart-level configuration;
- delegating layer drawing to plot layer objects;
- handling legends and layout adjustments.
"""


from .renderer import (
    Renderer
)
from .matplotlib_renderer import (
    MatplotlibRenderer
)


__all__ = [
    "Renderer",
    "MatplotlibRenderer"
]
