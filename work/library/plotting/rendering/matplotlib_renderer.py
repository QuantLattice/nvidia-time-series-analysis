"""
Matplotlib rendering backend for the plotting subsystem.

This module implements the renderer contract using Matplotlib as the
underlying visualization engine.

The implementation supports:
- primary and overlay layer rendering;
- chart title and axis configuration;
- grid and legend control;
- figure layout management.

The backend is intended for reusable layered chart composition.
"""


from matplotlib.figure import Figure
from typing import List
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from work.library.plotting.contracts import (
    ChartConfig,
    FigureConfig,
    PlotLayer
)
from work.library.plotting.rendering import (
    Renderer
)
from work.library.plotting.stack import LayerStack


class MatplotlibRenderer(Renderer):
    """
    Matplotlib-based implementation of the plotting renderer contract.

    This renderer composes a layered chart on top of a Matplotlib figure
    and supports a dual-axis layout for primary and overlay layers.

    The rendering workflow includes:
    - figure creation;
    - primary layer rendering;
    - overlay layer rendering;
    - chart configuration application;
    - legend assembly;
    - optional tight layout adjustment.
    """

    def render(
        self,
        stack: LayerStack,
        figure_config: FigureConfig,
        chart_config: ChartConfig,
    ) -> Figure:
        """
        Render a plot stack using Matplotlib.

        Parameters
        ----------
        stack : LayerStack
            Plot layer stack containing primary and overlay layers.

        figure_config : FigureConfig
            Figure configuration controlling size, DPI, and layout behavior.

        chart_config : ChartConfig
            Chart configuration controlling title, labels, grid, and legend.

        Returns
        -------
        Figure
            Rendered Matplotlib figure.

        Notes
        -----
        Primary layers are rendered on the main axes, while overlay layers
        are rendered on a secondary twin y-axis.
        """

        # FIGURE SETUP
        subplots = plt.subplots(  # type: ignore
            figsize=figure_config.figsize,
            dpi=figure_config.dpi
        )
        fig, ax = subplots

        overlay_ax = ax.twinx()

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

        # LAYOUT FINALIZATION
        if figure_config.tight_layout:
            fig.tight_layout()

        return fig

    def _render_layers(
        self,
        layers: List[PlotLayer],
        axes: Axes
    ) -> None:
        """
        Render a sequence of plot layers on the provided axes.

        Parameters
        ----------
        layers : List[PlotLayer]
            Plot layers to render.

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
            Chart configuration containing title, labels, and display flags.

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

        Returns
        -------
        None
            Legend is applied by side effect when enabled and available.
        """

        if not chart_config.show_legend:
            return

        handles, labels = axes.get_legend_handles_labels()
        overlay_handles, overlay_labels = \
            overlay_axes.get_legend_handles_labels()

        all_handles = handles + overlay_handles
        all_labels = labels + overlay_labels

        if all_handles:
            axes.legend(  # type: ignore
                handles=all_handles,
                labels=all_labels
            )
