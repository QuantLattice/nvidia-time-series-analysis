"""
Scatter plot layer implementation.

This module defines the concrete layer used to render point-based
visualizations on a Matplotlib axes object.
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
    ScatterStyle
)
from work.library.plotting.layers.base.numerical import (
    NumericalLayer
)


class ScatterLayer(NumericalLayer):
    """
    Renderable layer for scatter plots.

    A scatter layer represents discrete point-based numerical data
    rendered as individual markers.

    Parameters
    ----------
    x : Sequence[Any]
        X-axis coordinates of the points.
    y : Sequence[float]
        Y-axis coordinates of the points.
    style : Optional[ScatterStyle], default=None
        Visual styling configuration for the scatter layer.
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
        style: Optional[ScatterStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a scatter layer.

        Parameters
        ----------
        x : Sequence[Any]
            X-axis coordinates of the points.
        y : Sequence[float]
            Y-axis coordinates of the points.
        style : Optional[ScatterStyle], default=None
            Visual styling configuration for the scatter layer.
        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(
            placement=placement
        )

        self._style = style or ScatterStyle()

        self._x = x
        self._y = y

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def x(self) -> Sequence[Any]:
        """
        X-axis coordinates of the scatter points.

        Returns
        -------
        Sequence[Any]
            Stored x-values used during rendering.
        """

        return self._x

    @property
    def y(self) -> Sequence[float]:
        """
        Y-axis coordinates of the scatter points.

        Returns
        -------
        Sequence[float]
            Stored y-values used during rendering.
        """

        return self._y

    @property
    def style(self) -> ScatterStyle:
        """
        Visual style of the scatter layer.

        Returns
        -------
        ScatterStyle
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
        Render the scatter layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        res = axes.scatter(  # type: ignore
            x=self.x,
            y=self.y,
            color=self.style.color,
            alpha=self.style.alpha,
            label=self.style.label,
            zorder=self.style.zorder,
            linewidths=self.style.linewidth,
            marker=self.style.marker,  # type: ignore
            s=self.style.markersize,
            hatch=self.style.hatch,
            edgecolor=self.style.edgecolor,
        )

        if self.style.linestyle is not None:
            res.set_linestyle(ls=self.style.linestyle)  # type: ignore
