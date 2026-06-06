"""
Core plot layer implementations.

This package defines the concrete layer implementations used in the
layered plotting system.

It represents the primary composition unit of the rendering engine,
where each layer encapsulates both data and rendering logic.

Architecture
------------
The layer system is organized into three hierarchical domains:

Base layers
    Abstract foundation classes defining rendering contracts and
    placement semantics.

Numerical layers
    Continuous data visualizations such as line plots, scatter plots,
    and filled regions.

Categorical layers
    Discrete data visualizations such as bar charts, box plots,
    and histograms.

Design goals
-------------
- composable rendering primitives;
- separation between numerical and categorical domains;
- backend-independent rendering contract;
- consistent styling interface across all layer types.

Notes
-----
All layers implement the shared PlotLayer contract and are designed
to be compatible with Matplotlib-based rendering backends.
"""


from .base import (
    BaseLayer,
    CategoricalLayer,
    NumericalLayer
)
from .numerical import (
    FillBetweenLayer,
    LineLayer,
    ScatterLayer
)
from .categorical import (
    BarLayer,
    BoxLayer,
    HistogramLayer
)


__all__ = [
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
