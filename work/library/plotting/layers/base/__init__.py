"""
Base layer abstractions for the plotting system.

This package defines the fundamental hierarchy of plot layers used
in the rendering engine.

The abstraction separates visualization logic into two main domains:

- Numerical layers: continuous data representations (lines, curves,
  histograms, scatter plots)

- Categorical layers: discrete grouped data representations (bar charts,
  box plots, category-based visualizations)

These base classes enforce a consistent contract for styling and
rendering behavior across all plot types.
"""


from .layer import (
    BaseLayer
)
from .categorical import (
    CategoricalLayer
)
from .numerical import (
    NumericalLayer
)


__all__ = [
    "BaseLayer",
    "CategoricalLayer",
    "NumericalLayer"
]
