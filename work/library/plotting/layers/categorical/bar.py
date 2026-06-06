"""
Categorical bar layer implementation.

This module defines the concrete layer used to render categorical bar
visualizations on a Matplotlib axes object.
"""


from typing import (
    Sequence,
    Any,
    Optional
)
from matplotlib.axes import Axes

from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.contracts.layer_style import (
    BarStyle
)
from work.library.plotting.layers.base.categorical import (
    CategoricalLayer
)


class BarLayer(CategoricalLayer):
    """
    Renderable layer for bar charts.

    A bar layer represents categorical data as rectangular bars drawn
    on a Matplotlib axes instance.

    Parameters
    ----------
    categories : Sequence[Any]
        Category labels used along the x-axis.

    values : Sequence[float]
        Bar heights corresponding to the provided categories.

    width : float, default=0.8
        Width of each bar.

    style : Optional[BarStyle], default=None
        Visual styling configuration for the bar layer.

    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        categories: Sequence[Any],
        values: Sequence[float],
        width: float = 0.8,
        style: Optional[BarStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a bar layer.

        Parameters
        ----------
        categories : Sequence[Any]
            Category labels used along the x-axis.

        values : Sequence[float]
            Bar heights corresponding to the provided categories.

        width : float, default=0.8
            Width of each bar.

        style : Optional[BarStyle], default=None
            Visual styling configuration for the bar layer.

        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(
            placement=placement
        )

        self._style = style or BarStyle()

        self._categories = categories
        self._values = values
        self._width = width

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def categories(self) -> Sequence[Any]:
        """
        Category labels used by the bar layer.

        Returns
        -------
        Sequence[Any]
            Stored category labels.
        """

        return self._categories

    @property
    def values(self) -> Sequence[float]:
        """
        Bar heights used by the bar layer.

        Returns
        -------
        Sequence[float]
            Stored bar heights.
        """

        return self._values

    @property
    def style(self) -> BarStyle:
        """
        Visual style of the bar layer.

        Returns
        -------
        BarStyle
            Styling configuration used for rendering.
        """

        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, axes: Axes) -> None:
        """
        Render the bar layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        axes.bar(  # type: ignore
            x=self._categories,
            height=self._values,
            width=self._width,
            color=self.style.color,
            alpha=self.style.alpha,
            label=self.style.label,
            zorder=self.style.zorder,
            linewidth=self.style.edge_linewidth,
            edgecolor=self.style.edgecolor,
            hatch=self.style.hatch
        )
