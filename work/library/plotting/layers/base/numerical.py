"""
Numerical plot layer abstraction.

This module defines the base class for numerical visualization layers
that operate on continuous data domains such as line plots, scatter
plots, histograms, and mathematical functions.
"""


from abc import ABC, abstractmethod

from work.library.plotting.contracts.layer import (
    LayerPlacement,
)
from .layer import (
    BaseLayer
)
from work.library.plotting.contracts.layer_style import (
    LayerStyle
)


class NumericalLayer(BaseLayer, ABC):
    """
    Abstract base class for numerical plot layers.

    Numerical layers represent continuous data visualizations where
    values are defined over numeric domains (e.g., functions, time
    series, distributions).

    Notes
    -----
    These layers typically assume continuous x-axis behavior and
    are rendered using interpolation or point sampling.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize numerical layer.

        Parameters
        ----------
        placement : LayerPlacement
            Defines whether the layer is rendered as primary or overlay.
        """

        super().__init__(
            placement=placement
        )

    # ------------------------------------------------------------------
    # Abstract API
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def style(self) -> LayerStyle:
        """
        Visual style configuration for the numerical layer.

        Returns
        -------
        LayerStyle
            Styling configuration used during rendering.
        """

        ...
