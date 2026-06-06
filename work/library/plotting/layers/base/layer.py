"""
Base implementation of the plot layer abstraction.

This module defines the concrete base class for all rendering layers
used in the plotting subsystem.

A plot layer represents a single renderable visualization unit that
encapsulates both metadata and rendering behavior.

Each layer:

- has a unique identifier;
- belongs to a rendering placement group (PRIMARY or OVERLAY);
- defines a rendering method operating on Matplotlib axes.

This base implementation provides common identity and placement
handling while delegating rendering logic to subclasses.
"""


from abc import ABC, abstractmethod
from matplotlib.axes import Axes
from uuid import uuid4

from work.library.plotting.contracts.layer import (
    LayerPlacement,
    PlotLayer
)


class BaseLayer(PlotLayer, ABC):
    """
    Base implementation of a renderable plot layer.

    This class provides shared functionality for all plot layers,
    including unique identity generation and placement management.

    It serves as the foundational building block for all numerical
    and categorical visualization layers in the system.

    Notes
    -----
    - Each instance is assigned a globally unique identifier.
    - Layers are stateless with respect to rendering lifecycle.
    - Rendering is delegated to backend-specific implementations.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize base plot layer.

        Parameters
        ----------
        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Defines the rendering group of the layer within the
            composition pipeline (primary or overlay).
        """

        self._id = str(uuid4())
        self._placement = placement

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def id(self) -> str:
        """
        Unique identifier of the plot layer.

        Returns
        -------
        str
            Globally unique identifier assigned at layer creation time.

        Notes
        -----
        This identifier is used for tracking, debugging, and internal
        composition management.
        """

        return self._id

    @property
    def placement(self) -> LayerPlacement:
        """
        Rendering placement category of the layer.

        Returns
        -------
        LayerPlacement
            Defines whether the layer is rendered as PRIMARY content
            or OVERLAY content.

        Notes
        -----
        Placement determines which axes the layer is rendered onto
        within the plotting pipeline.
        """

        return self._placement

    # ------------------------------------------------------------------
    # Abstract API
    # ------------------------------------------------------------------

    @abstractmethod
    def render(
        self,
        axes: Axes
    ) -> None:
        """
        Render the layer on a Matplotlib axes instance.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for rendering.

        Notes
        -----
        - Rendering is performed as a side effect on the provided axes.
        - Implementations must not modify global Matplotlib state.
        - This method defines the core rendering contract for all
        concrete plot layers.
        """

        ...
