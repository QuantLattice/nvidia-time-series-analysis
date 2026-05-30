"""
Built-in plotting layer implementations.

This package contains reusable layer abstractions used by the
plotting subsystem.

Layers encapsulate rendering logic for individual visualization
elements and serve as the primary building blocks for chart
composition.

The package provides base classes that simplify development of
custom plot layers while remaining independent from rendering
session management and backend implementations.
"""


from abc import ABC, abstractmethod
from matplotlib.axes import Axes

from work.library.plotting.contracts import (
    LayerPlacement,
    PlotLayer
)


class BaseLayer(PlotLayer, ABC):
    """
    Base plotting layer implementation.

    This module provides a convenience base class for plot layers.

    The class implements common placement handling while leaving
    rendering behavior to subclasses. Concrete layers should inherit
    from this class and implement the rendering logic required to
    draw themselves on a Matplotlib axes instance.
    """

    def __init__(
        self,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize the layer.

        Parameters
        ----------
        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Placement category assigned to the layer.
        """

        self._placement = placement

    @property
    def placement(self) -> LayerPlacement:
        """
        Layer placement category.

        Returns
        -------
        LayerPlacement
            Placement assigned to this layer.
        """

        return self._placement

    @abstractmethod
    def render(
        self,
        axes: Axes
    ) -> None:
        """
        Render the layer on a Matplotlib axes object.

        Parameters
        ----------
        axes : Axes
            Target axes used for rendering.

        Returns
        -------
        None
            Rendering is performed by side effect.

        Notes
        -----
        Subclasses must implement this method.
        """

        ...
