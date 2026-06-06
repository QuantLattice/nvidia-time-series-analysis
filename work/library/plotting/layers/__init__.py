"""
Core plot layer implementations.

This package defines the reusable layer implementations used by the
layered plotting system.

Layers serve as the primary composition units of the rendering engine,
encapsulating both visualization data and rendering behavior.

Architecture
------------
The layer system is organized into multiple domains:

Base layers
    Abstract foundation classes defining rendering contracts and
    placement semantics.

Numerical layers
    Continuous data visualizations such as line plots, scatter plots,
    and filled regions.

Categorical layers
    Discrete data visualizations such as bar charts, box plots,
    and histograms.

Matrix layers
    Matrix-oriented visualizations such as heatmaps.

Design goals
------------
- composable rendering primitives;
- separation of visualization domains;
- backend-independent rendering contracts;
- reusable styling abstractions;
- consistent rendering behavior across layer types.

Notes
-----
All layers implement the shared PlotLayer contract and are designed
to operate with Matplotlib-based rendering backends.
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
from .matrix import (
    HeatmapLayer
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
    "HistogramLayer",

    "HeatmapLayer"
]
