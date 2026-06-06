"""
Core abstractions for composable plot layers.

This module defines the base contract for all renderable plot layers
used in the layered plotting architecture.

The system is built around a two-level composition model:

- PRIMARY layers: main visual content of the chart
- OVERLAY layers: auxiliary visual elements rendered on top of primary content

Each layer implements a rendering contract targeting a Matplotlib Axes
instance, allowing the plotting system to remain backend-agnostic while
still supporting Matplotlib as the default renderer.

Notes
-----
This abstraction enables modular chart construction where visual elements
are composed rather than hard-coded into monolithic plotting functions.
"""


from enum import StrEnum
from abc import ABC, abstractmethod
from matplotlib.axes import Axes


class LayerPlacement(StrEnum):
    """
    Defines the rendering layer category in a compositional chart.

    Layer placement determines how a plot layer is integrated into the
    rendering pipeline.

    Attributes
    ----------
    PRIMARY : str
        Main visualization layer containing core chart data.

    OVERLAY : str
        Auxiliary layer rendered above primary content, typically used
        for annotations, reference lines, or secondary data series.
    """

    PRIMARY = "primary"
    OVERLAY = "overlay"


class PlotLayer(ABC):
    """
    Abstract contract for all renderable plot layers.

    A plot layer represents a single composable visualization unit that
    can be combined with other layers within a plotting session.

    Each layer defines:
    - its placement in the rendering pipeline;
    - a unique identifier;
    - a rendering method targeting a Matplotlib Axes instance.

    This design enables declarative composition of charts from independent
    visual components.

    Notes
    -----
    Implementations must be stateless with respect to rendering context
    and should rely solely on provided data and configuration.
    """

    # ------------------------------------------------------------------
    # Abstract API
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Unique identifier of the plot layer.

        Returns
        -------
        str
            Stable identifier used for tracking, debugging, or caching.
        """

        ...

    @property
    @abstractmethod
    def placement(self) -> LayerPlacement:
        """
        Define the layer placement within the rendering pipeline.

        Returns
        -------
        LayerPlacement
            Placement category (PRIMARY or OVERLAY).
        """

        ...

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    @abstractmethod
    def render(
        self,
        axes: Axes
    ) -> None:
        """
        Render the layer onto a Matplotlib Axes instance.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        Implementations must not modify global plotting state.
        """

        ...
