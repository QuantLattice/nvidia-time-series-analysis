"""
Matrix-based heatmap layer implementation.

This module defines the concrete layer used to render 2D matrix data
as a heatmap on a Matplotlib axes object.

The layer supports optional row and column labels, value annotations,
and colorbar display through a dedicated heatmap style object.
"""


from typing import (
    Optional,
    Any,
    Iterable
)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import ArrayLike
from matplotlib.colors import Normalize


from work.library.plotting.contracts.layer import (
    LayerPlacement
)
from work.library.plotting.contracts.layer_style import (
    HeatmapStyle
)
from work.library.plotting.layers.base.layer import (
    BaseLayer
)


class HeatmapLayer(BaseLayer):
    """
    Renderable layer for heatmap visualizations.

    A heatmap layer represents a 2D numerical matrix visualized as a
    color-mapped image on a Matplotlib axes instance.

    Parameters
    ----------
    matrix : ArrayLike
        Two-dimensional numeric matrix to render as a heatmap.

    row_labels : Optional[Iterable[Any]], default=None
        Optional labels for matrix rows.

    column_labels : Optional[Iterable[Any]], default=None
        Optional labels for matrix columns.

    style : Optional[HeatmapStyle], default=None
        Visual styling configuration for the heatmap layer.

    placement : LayerPlacement, default=LayerPlacement.PRIMARY
        Rendering placement of the layer.

    Notes
    -----
    The input matrix is converted to a NumPy array of floating-point
    values. The layer expects a two-dimensional matrix.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        matrix: ArrayLike,
        row_labels: Optional[Iterable[Any]] = None,
        column_labels: Optional[Iterable[Any]] = None,
        style: Optional[HeatmapStyle] = None,
        placement: LayerPlacement = LayerPlacement.PRIMARY
    ) -> None:
        """
        Initialize a heatmap layer.

        Parameters
        ----------
        matrix : ArrayLike
            Two-dimensional numeric matrix to render as a heatmap.

        row_labels : Optional[Iterable[Any]], default=None
            Optional labels for matrix rows.

        column_labels : Optional[Iterable[Any]], default=None
            Optional labels for matrix columns.

        style : Optional[HeatmapStyle], default=None
            Visual styling configuration for the heatmap layer.

        placement : LayerPlacement, default=LayerPlacement.PRIMARY
            Rendering placement of the layer.

        Raises
        ------
        ValueError
            If the input matrix is not two-dimensional.
        """

        super().__init__(
            placement=placement
        )

        self._matrix = np.asarray(a=matrix, dtype=float)

        if self._matrix.ndim != 2:
            raise ValueError("HeatmapLayer.matrix must be a 2D matrix.")

        self._row_labels = None
        if row_labels is not None:
            self._row_labels = [str(value) for value in row_labels]

        self._column_labels = None
        if column_labels is not None:
            self._column_labels = [str(value) for value in column_labels]

        self._style = style or HeatmapStyle()

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def matrix(self) -> np.ndarray:
        """
        Heatmap data matrix.

        Returns
        -------
        np.ndarray
            Stored two-dimensional floating-point matrix.
        """
        return self._matrix

    @property
    def style(self) -> HeatmapStyle:
        """
        Visual style of the heatmap layer.

        Returns
        -------
        HeatmapStyle
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
        Render the heatmap layer on a Matplotlib axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing.

        Notes
        -----
        Rendering is performed as a side effect on the provided axes.
        """

        image = axes.imshow(  # type: ignore
            X=self.matrix,
            cmap=self.style.cmap,
            vmin=self.style.vmin,
            vmax=self.style.vmax,
            aspect="auto",
            alpha=self.style.alpha,
        )

        if self._column_labels is not None:
            axes.set_xticks(  # type: ignore
                ticks=range(len(self._column_labels)),
                labels=self._column_labels
            )

        if self._row_labels is not None:
            axes.set_yticks(  # type: ignore
                ticks=range(len(self._row_labels)),
                labels=self._row_labels
            )

        if self.style.annotate:
            self._draw_annotations(
                axes=axes
            )

        if self.style.show_colorbar:
            axes.figure.colorbar(  # type: ignore
                mappable=image,
                ax=axes
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _draw_annotations(
        self,
        axes: Axes
    ) -> None:
        """
        Draw numeric annotations inside each heatmap cell.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes used for drawing annotations.
        """

        rows, cols = self.matrix.shape

        for row in range(rows):
            for col in range(cols):
                if self.style.annotation_color is not None:
                    color = self.style.annotation_color
                else:
                    color = self._get_auto_annotation_color(
                        value=self.matrix[row, col]
                    )

                axes.text(  # type: ignore
                    x=col,
                    y=row,
                    color=color,
                    s=format(
                        self.matrix[row, col],
                        self.style.annotation_format
                    ),
                    ha="center",
                    va="center"
                )

    def _get_auto_annotation_color(
        self,
        value: float
    ) -> str:
        """
        Compute annotation color based on background brightness.

        Parameters
        ----------
        value : float
            Heatmap cell value used to determine annotation contrast.

        Returns
        -------
        str
            "black" for light backgrounds and "white" for dark backgrounds.
        """

        norm = Normalize(
            vmin=(
                self.style.vmin
                if self.style.vmin is not None
                else float(self.matrix.min())
            ),
            vmax=(
                self.style.vmax
                if self.style.vmax is not None
                else float(self.matrix.max())
            )
        )

        rgba = plt.get_cmap(
            self.style.cmap
        )(
            norm(value)
        )

        r, g, b, _ = rgba

        brightness = (
            0.299 * r +
            0.587 * g +
            0.114 * b
        )

        return "black" if brightness > 0.5 else "white"
