"""
Histogram layer implementation.

This module defines the concrete layer used to render histogram-based
distribution visualizations on a Matplotlib axes object.
"""


from typing import Sequence, Optional
from matplotlib.axes import Axes

from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.contracts.layer_style import (
    HistogramStyle
)
from work.library.plotting.layers.base.categorical import (
    CategoricalLayer
)


class HistogramLayer(CategoricalLayer):
    """
    Renderable layer for histograms.

    A histogram layer represents the distribution of numerical values
    as bins drawn on a Matplotlib axes instance.

    Parameters
    ----------
    values : Sequence[float]
        Input values to be grouped into histogram bins.

    bins : Optional[int], default=None
        Number of bins to use for the histogram.

    style : Optional[HistogramStyle], default=None
        Visual styling configuration for the histogram layer.

    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        values: Sequence[float],
        bins: Optional[int] = None,
        style: Optional[HistogramStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a histogram layer.

        Parameters
        ----------
        values : Sequence[float]
            Input values to be grouped into histogram bins.

        bins : Optional[int], default=None
            Number of bins to use for the histogram.

        style : Optional[HistogramStyle], default=None
            Visual styling configuration for the histogram layer.

        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(
            placement=placement
        )

        self._style = style or HistogramStyle()

        self._values = values
        self._bins = bins

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def values(self) -> Sequence[float]:
        """
        Input values used by the histogram layer.

        Returns
        -------
        Sequence[float]
            Stored values used for rendering.
        """

        return self._values

    @property
    def style(self) -> HistogramStyle:
        """
        Visual style of the histogram layer.

        Returns
        -------
        HistogramStyle
            Styling configuration used for rendering.
        """

        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, axes: Axes) -> None:
        """
        Render the histogram layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        axes.hist(  # type: ignore
            x=self._values,
            bins=self._bins,
            color=self.style.color,
            alpha=self.style.alpha,
            label=self.style.label,
            zorder=self.style.zorder,
            edgecolor=self.style.edgecolor,
            hatch=self.style.hatch,
        )
