"""
Line plot layer implementation.

This module defines the concrete layer used to render continuous
line-based visualizations such as time series, trends, and functions.
"""


from typing import (
    Sequence,
    Optional,
    Any
)
from matplotlib.axes import Axes

from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.contracts.layer_style import (
    LineStyle
)
from work.library.plotting.layers.base.numerical import (
    NumericalLayer
)


class LineLayer(NumericalLayer):
    """
    Renderable layer for line plots.

    A line layer represents continuous numerical data drawn as a line
    on a Matplotlib axes object.

    Parameters
    ----------
    x : Sequence[Any]
        X-axis coordinates of the line.
    y : Sequence[float]
        Y-axis coordinates of the line.
    style : Optional[LineStyle], default=None
        Visual styling configuration for the line.
    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        x: Sequence[Any],
        y: Sequence[float],
        style: Optional[LineStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a line layer.

        Parameters
        ----------
        x : Sequence[Any]
            X-axis coordinates of the line.
        y : Sequence[float]
            Y-axis coordinates of the line.
        style : Optional[LineStyle], default=None
            Visual styling configuration for the line.
        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(placement=placement)

        self._style = style or LineStyle()

        self._x = x
        self._y = y

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def x(self) -> Sequence[Any]:
        """
        X-axis coordinates of the line.

        Returns
        -------
        Sequence[Any]
            Stored x-values used during rendering.
        """

        return self._x

    @property
    def y(self) -> Sequence[Any]:
        """
        Y-axis coordinates of the line.

        Returns
        -------
        Sequence[float]
            Stored y-values used during rendering.
        """

        return self._y

    @property
    def style(self) -> LineStyle:
        """
        Visual style of the line layer.

        Returns
        -------
        LineStyle
            Styling configuration used for rendering.
        """

        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(
        self,
        axes: Axes
    ) -> None:
        """
        Render the line layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        axes.plot(  # type: ignore
            self.x,
            self.y,
            color=self.style.color,
            alpha=self.style.alpha,
            label=self.style.label,
            zorder=self.style.zorder,
            linewidth=self.style.linewidth,
            linestyle=self.style.linestyle,
            marker=self.style.marker,
            markersize=self.style.markersize,
        )
