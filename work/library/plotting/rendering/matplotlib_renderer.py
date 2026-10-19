"""
Matplotlib-based implementation of the rendering backend.

This module provides a concrete implementation of the `Renderer`
contract using Matplotlib as the visualization engine.

The renderer operates on an existing `PlotContext`, which contains
pre-initialized Matplotlib figure and axes objects. It is responsible
for rendering a stack of plot layers and applying chart-level
configuration such as labels, styles, grid, and legends.

Notes
-----
This renderer does not manage figure or axes lifecycle. It assumes
that the plotting session is responsible for context creation and
initialization.
"""


from typing import (
    Iterable,
    Optional,
)
from matplotlib.axes import Axes

from work.library.plotting.contracts import (
    ChartConfig,
    PlotContext,
    PlotLayer
)
from work.library.plotting.rendering import (
    Renderer
)
from work.library.plotting.rendering.axes_configurator import (
    AxesConfigurator
)
from work.library.plotting.stack import (
    LayerStack
)


class MatplotlibRenderer(Renderer, AxesConfigurator):
    """
    Renderer implementation based on Matplotlib axes.

    This class translates a `LayerStack` and `ChartConfig` into
    visual output on Matplotlib axes contained in a `PlotContext`.

    The renderer is responsible for:

    - rendering primary and overlay plot layers;
    - applying chart-level styling and configuration;
    - managing axis labels, ticks, and grid visibility;
    - aggregating legend entries across multiple axes.

    Axis-configuration and legend methods are provided by the
    `AxesConfigurator` mixin.

    Notes
    -----
    This class does not create or manage Matplotlib figures or axes.
    It operates strictly on an existing `PlotContext`.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(
        self,
        stack: LayerStack,
        context: PlotContext,
        chart_config: ChartConfig,
    ) -> None:
        """
        Render a `LayerStack` into a Matplotlib plotting context.

        Parameters
        ----------
        stack : LayerStack
            Container of primary and overlay plot layers.

        context : PlotContext
            Active plotting context containing Matplotlib figure
            and axes.

        chart_config : ChartConfig
            Configuration describing chart appearance, labels,
            visibility rules, and legend behavior.

        Notes
        -----
        - Primary layers are rendered on the main axes.
        - Overlay layers (if present) are rendered on secondary axes.
        - Rendering is performed via side effects on Matplotlib
          objects.
        """

        ax = context.primary_axes
        overlay_ax = context.overlay_axes

        # LAYER RENDERING
        self._render_layers(
            layers=stack.primary_layers(),
            axes=ax
        )

        overlay_layers = stack.overlay_layers()
        if overlay_ax is not None:
            self._render_layers(
                    layers=overlay_layers,
                    axes=overlay_ax
                )

        # CHART CONFIGURATION
        self._apply_chart_config(
            context=context,
            chart_config=chart_config,
            axes=ax,
            overlay_axes=overlay_ax,
        )

        # LEGEND HANDLING
        self._apply_legend(
            axes=ax,
            overlay_axes=overlay_ax,
            chart_config=chart_config
        )

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render_layers(
        self,
        layers: Iterable[PlotLayer],
        axes: Axes
    ) -> None:
        """
        Render multiple plot layers on a single Matplotlib axes.

        Parameters
        ----------
        layers : Iterable[PlotLayer]
            Sequence of plot layers implementing the rendering
            contract.

        axes : Axes
            Target Matplotlib axes.
        """

        for layer in layers:
            layer.render(axes=axes)

    # ------------------------------------------------------------------
    # Chart configuration
    # ------------------------------------------------------------------

    def _apply_chart_config(
        self,
        context: PlotContext,
        chart_config: ChartConfig,
        axes: Axes,
        overlay_axes: Optional[Axes],
    ) -> None:
        """
        Apply chart-level configuration to Matplotlib axes.

        This includes styling, labels, tick visibility, and grid
        settings.

        Parameters
        ----------
        context : PlotContext
            Active rendering context.

        chart_config : ChartConfig
            Chart configuration object.

        axes : Axes
            Primary Matplotlib axes.

        overlay_axes : Optional[Axes]
            Optional secondary axes used for overlay rendering.
        """

        self._apply_style(
            context=context,
            chart_config=chart_config
        )

        self._apply_labels(
            chart_config=chart_config,
            axes=axes,
            overlay_axes=overlay_axes
        )

        self._apply_ticks(
            axes=axes,
            overlay_axes=overlay_axes,
            chart_config=chart_config
        )
