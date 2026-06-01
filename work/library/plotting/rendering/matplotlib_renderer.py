"""
Matplotlib rendering backend for the plotting subsystem.

This module implements the renderer contract using Matplotlib as the
underlying visualization engine.

The renderer operates on an existing ``PlotContext`` and is responsible
for drawing plot layers and applying chart-level configuration.

Features
--------
- primary and overlay layer rendering;
- chart title and axis label configuration;
- grid management;
- legend aggregation across multiple axes.

Notes
-----
Figure creation and lifecycle management are handled by the plotting
session. This renderer only performs drawing operations on an existing
plot context.
"""


from typing import Iterable
from matplotlib.axes import Axes

from work.library.plotting.contracts import (
    ChartConfig,
    PlotContext,
    PlotLayer
)
from work.library.plotting.rendering import (
    Renderer
)
from work.library.plotting.stack import LayerStack


class MatplotlibRenderer(Renderer):
    """
    Matplotlib implementation of the rendering contract.

    The renderer draws plot layers into an existing plotting context
    using Matplotlib axes.

    The rendering workflow includes:

    - primary layer rendering;
    - overlay layer rendering;
    - chart configuration application;
    - legend aggregation;
    - final chart composition.

    Notes
    -----
    The renderer assumes that figure creation and axis initialization
    have already been performed by the active plotting session.
    """

    # ==========================================
    # RENDERING PIPELINE
    # ==========================================

    def render(
        self,
        stack: LayerStack,
        context: PlotContext,
        chart_config: ChartConfig,
    ) -> None:
        """
        Render a plot stack using Matplotlib.

        Parameters
        ----------
        stack : LayerStack
            Collection of plot layers to render.

        context : PlotContext
            Active plotting context containing the figure and target axes.

        chart_config : ChartConfig
            Chart-level configuration controlling labels, title,
            grid visibility, and legend behavior.

        Returns
        -------
        None
            Rendering is performed by side effect on the provided
            plotting context.

        Notes
        -----
        Primary layers are rendered on the primary axes, while overlay
        layers are rendered on the secondary overlay axes.
        """

        ax = context.primary_axes
        overlay_ax = context.overlay_axes

        # LAYER RENDERING
        self._render_layers(
            layers=stack.primary_layers(),
            axes=ax
        )
        self._render_layers(
                layers=stack.overlay_layers(),
                axes=overlay_ax
            )

        # CHART CONFIGURATION
        self._apply_chart_config(
            chart_config=chart_config,
            axes=ax
        )

        # LEGEND HANDLING
        self._apply_legend(
            axes=ax,
            overlay_axes=overlay_ax,
            chart_config=chart_config
        )

    # ==========================================
    # INTERNAL HELPERS
    # ==========================================

    def _render_layers(
        self,
        layers: Iterable[PlotLayer],
        axes: Axes
    ) -> None:
        """
        Render a sequence of plot layers on the provided axes.

        Parameters
        ----------
        layers : Iterable[PlotLayer]
            Collection of plot layers to render.

        axes : Axes
            Target Matplotlib axes.

        Returns
        -------
        None
            Rendering is performed by side effect.
        """

        for layer in layers:
            layer.render(axes=axes)

    def _apply_chart_config(
        self,
        axes: Axes,
        chart_config: ChartConfig
    ) -> None:
        """
        Apply chart-level visual configuration to axes.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes.

        chart_config : ChartConfig
            Chart metadata and display options to apply to the
            primary axes.

        Returns
        -------
        None
            Configuration is applied by side effect.
        """

        if chart_config.show_grid:
            axes.grid(visible=True)  # type: ignore

        if chart_config.title:
            axes.set_title(label=chart_config.title)  # type: ignore

        if chart_config.xlabel:
            axes.set_xlabel(xlabel=chart_config.xlabel)  # type: ignore

        if chart_config.ylabel:
            axes.set_ylabel(ylabel=chart_config.ylabel)  # type: ignore

    def _apply_legend(
        self,
        axes: Axes,
        overlay_axes: Axes,
        chart_config: ChartConfig
    ) -> None:
        """
        Apply legend configuration to the rendered chart.

        Parameters
        ----------
        axes : Axes
            Primary Matplotlib axes.

        overlay_axes : Axes
            Secondary overlay axes used for twin-axis rendering.

        chart_config : ChartConfig
            Chart configuration controlling legend visibility.

        Notes
        -----
        Legend entries from both primary and overlay axes are merged
        into a single legend attached to the primary axes.
        """

        if not chart_config.show_legend:
            return

        handles, labels = axes.get_legend_handles_labels()
        all_handles = list(handles)
        all_labels = list(labels)

        overlay_handles, overlay_labels = (
            overlay_axes.get_legend_handles_labels()
        )

        all_handles.extend(overlay_handles)
        all_labels.extend(overlay_labels)

        if all_handles:
            axes.legend(  # type: ignore
                handles=all_handles,
                labels=all_labels
            )
