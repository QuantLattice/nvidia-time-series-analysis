"""
Categorical plot layer abstraction.

This module defines the base class for categorical visualization
layers such as bar charts, box plots, and other discrete data
representations.

Categorical layers operate on discrete domains where data is
grouped into categories rather than continuous numerical ranges.
"""


from abc import ABC, abstractmethod

from work.library.plotting.contracts.layer_style import (
    LayerStyle
)
from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from .layer import (
    BaseLayer
)


class CategoricalLayer(BaseLayer, ABC):
    """
    Abstract base class for categorical plot layers.

    Categorical layers represent visualizations of discrete data
    grouped by categories (e.g., bar charts, box plots).

    Notes
    -----
    These layers are typically rendered using categorical axes
    rather than continuous numerical scales.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize categorical layer.

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
        Visual style configuration for the categorical layer.

        Returns
        -------
        LayerStyle
            Styling configuration applied during rendering.
        """

        ...
