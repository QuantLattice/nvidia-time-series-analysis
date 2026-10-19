"""
Categorical box layer implementation.

This module defines the concrete layer used to render box-and-whisker
visualizations on a Matplotlib axes object.
"""


from typing import Sequence, Optional
from matplotlib.axes import Axes

from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.contracts.layer_style import (
    BoxStyle
)
from work.library.plotting.layers.base.categorical import (
    CategoricalLayer
)


class BoxLayer(CategoricalLayer):
    """
    Renderable layer for box plots.

    A box layer represents a statistical distribution using quartiles,
    whiskers, and optional outliers.

    Parameters
    ----------
    values : Sequence[float]
        Input values used to compute the box plot.

    style : Optional[BoxStyle], default=None
        Visual styling configuration for the box layer.

    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.
    """

    # ------------------------------------------------------------------
    # Matplotlib defaults
    # ------------------------------------------------------------------

    _PATCH_ARTIST = True
    _SHOWCAPS = True
    _SHOWBOX = True
    _SHOWMEANS = False

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        values: Sequence[float],
        style: Optional[BoxStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a box layer.

        Parameters
        ----------
        values : Sequence[float]
            Input values used to compute the box plot.

        style : Optional[BoxStyle], default=None
            Visual styling configuration for the box layer.

        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.
        """

        super().__init__(
            placement=placement
        )

        self._style = style or BoxStyle()

        self._values = values

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def values(self) -> Sequence[float]:
        """
        Input values used by the box layer.

        Returns
        -------
        Sequence[float]
            Stored values used for rendering.
        """

        return self._values

    @property
    def style(self) -> BoxStyle:
        """
        Visual style of the box layer.

        Returns
        -------
        BoxStyle
            Styling configuration used for rendering.
        """

        return self._style

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, axes: Axes) -> None:
        """
        Render the box layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        axes.boxplot(
            x=self._values,
            capprops=dict(
                color=self.style.color,
                linestyle=self.style.linestyle,
                linewidth=self.style.linewidth,
            ),
            boxprops=dict(
                color=self.style.color,
                linestyle=self.style.linestyle,
                linewidth=self.style.linewidth,
                hatch=self.style.hatch
            ),
            whiskerprops=dict(
                color=self.style.color,
                linestyle=self.style.linestyle,
                linewidth=self.style.linewidth,
            ),
            flierprops=dict(
                color=self.style.color,
                linestyle=self.style.linestyle,
                linewidth=self.style.linewidth,
                marker=self.style.marker,
                markersize=self.style.markersize,
            ),
            medianprops=dict(
                color=self.style.color,
                linestyle=self.style.linestyle,
                linewidth=self.style.linewidth,
            ),
            label=self.style.label,
            zorder=self.style.zorder,
            showfliers=self.style.showfliers,
            patch_artist=self._PATCH_ARTIST,
            showcaps=self._SHOWCAPS,
            showbox=self._SHOWBOX,
            showmeans=self._SHOWMEANS
        )
