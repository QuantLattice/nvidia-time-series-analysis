"""
Filled area layer implementation.

This module defines the concrete layer used to render filled regions
between two numerical series on a Matplotlib axes object.
"""


from typing import (
    Sequence,
    Optional
)
from matplotlib.axes import Axes

from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.layers.base.numerical import (
    NumericalLayer
)
from work.library.plotting.contracts.layer_style import (
    FillBetweenStyle
)


class FillBetweenLayer(NumericalLayer):
    """
    Renderable layer for filled area plots.

    A fill-between layer renders the region between two numerical
    curves and is commonly used for confidence intervals, envelopes,
    and bounded areas.

    Parameters
    ----------
    x : Sequence[float]
        X-axis coordinates shared by both boundaries.
    y1 : Sequence[float]
        Lower boundary values.
    y2 : Sequence[float]
        Upper boundary values.
    where : Optional[Sequence[bool]], default=None
        Boolean mask controlling where the filled region is drawn.
    style : Optional[FillBetweenStyle], default=None
        Visual styling configuration for the filled area.
    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        x: Sequence[float],
        y1: Sequence[float],
        y2: Sequence[float],
        where: Optional[Sequence[bool]] = None,
        style: Optional[FillBetweenStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a fill-between layer.

        Parameters
        ----------
        x : Sequence[float]
            X-axis coordinates shared by both boundaries.
        y1 : Sequence[float]
            Lower boundary values.
        y2 : Sequence[float]
            Upper boundary values.
        where : Optional[Sequence[bool]], default=None
            Boolean mask controlling where the filled region is drawn.
        style : Optional[FillBetweenStyle], default=None
            Visual styling configuration for the filled area.
        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(
            placement=placement
        )

        self._style = style or FillBetweenStyle()

        self._x = x
        self._y1 = y1
        self._y2 = y2
        self._where = where

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def x(self) -> Sequence[float]:
        """
        X-axis coordinates of the filled region.

        Returns
        -------
        Sequence[float]
            Stored x-values used during rendering.
        """

        return self._x

    @property
    def y1(self) -> Sequence[float]:
        """
        Lower boundary of the filled region.

        Returns
        -------
        Sequence[float]
            Stored lower boundary values used during rendering.
        """

        return self._y1

    @property
    def y2(self) -> Sequence[float]:
        """
        Upper boundary of the filled region.

        Returns
        -------
        Sequence[float]
            Stored upper boundary values used during rendering.
        """

        return self._y2

    @property
    def style(self) -> FillBetweenStyle:
        """
        Visual style of the fill-between layer.

        Returns
        -------
        FillBetweenStyle
            Styling configuration used for rendering.
        """

        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, axes: Axes) -> None:
        """
        Render the filled region on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        axes.fill_between(  # type: ignore
            x=self._x,
            y1=self._y1,
            y2=self._y2,
            where=self._where,
            color=self.style.color,
            alpha=self.style.alpha,
            label=self.style.label,
            zorder=self.style.zorder,
            hatch=self.style.hatch,
        )
