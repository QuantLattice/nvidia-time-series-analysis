"""
Plot layer contracts.

This module defines the abstract interface and placement metadata
used by layered plotting components.

The layer contract is designed to support composable chart rendering,
including primary plot content and overlay elements such as
reference lines, annotations, or secondary series.
"""


from enum import StrEnum
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


class LayerPlacement(StrEnum):
    """
    Placement strategy for plot layers.

    Members
    -------
    PRIMARY : str
        Main plotting layer responsible for the core visualization.

    OVERLAY : str
        Secondary layer rendered on top of the primary layer.
    """

    PRIMARY = "primary"
    OVERLAY = "overlay"


class PlotLayer(ABC):
    """
    Abstract base class for plot layers.

    A plot layer represents a single renderable visualization component
    that can be composed with other layers inside a plotting session.

    Subclasses must define:
    - placement information;
    - render behavior for a Matplotlib Axes instance.

    Notes
    -----
    This abstraction allows charts to be built as layered compositions
    rather than monolithic plotting functions.
    """

    @property
    @abstractmethod
    def placement(self) -> LayerPlacement:
        """
        Return the placement category for the layer.

        Returns
        -------
        LayerPlacement
            Placement of the layer within the plot composition pipeline.
        """

        ...

    @abstractmethod
    def render(self, axes: Axes) -> None:
        """
        Render the layer on a Matplotlib axes object.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Returns
        -------
        None
            The method performs rendering by side effect.
        """

        ...
