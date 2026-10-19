"""
Base layer abstractions for the plotting system.

This package defines the foundational layer hierarchy used throughout
the rendering engine.

The provided abstractions establish common behavior shared by all plot
layers, including placement management and rendering contracts.

Layer categories
----------------
BaseLayer
    Root abstraction for all renderable plot layers.

NumericalLayer
    Base class for layers representing continuous numerical data.

CategoricalLayer
    Base class for layers representing discrete or grouped data.

Notes
-----
Not all layer implementations are required to belong to a specific
domain abstraction. Specialized layer types may inherit directly from
BaseLayer when neither numerical nor categorical semantics apply.
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
    "NumericalLayer",
]
