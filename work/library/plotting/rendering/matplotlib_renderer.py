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
    Literal,
    Optional,
    Callable
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
from work.library.plotting.stack import (
    LayerStack
)


class MatplotlibRenderer(Renderer):
    """
    Renderer implementation based on Matplotlib axes.

    This class translates a `LayerStack` and `ChartConfig` into
    visual output on Matplotlib axes contained in a `PlotContext`.

    The renderer is responsible for:

    - rendering primary and overlay plot layers;
    - applying chart-level styling and configuration;
    - managing axis labels, ticks, and grid visibility;
    - aggregating legend entries across multiple axes.

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
            Active plotting context containing Matplotlib figure and axes.

        chart_config : ChartConfig
            Configuration describing chart appearance, labels,
            visibility rules, and legend behavior.

        Notes
        -----
        - Primary layers are rendered on the main axes.
        - Overlay layers (if present) are rendered on secondary axes.
        - Rendering is performed via side effects on Matplotlib objects.
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
            Sequence of plot layers implementing the rendering contract.

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

        This includes styling, labels, tick visibility, and grid settings.

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

    def _apply_style(
        self,
        context: PlotContext,
        chart_config: ChartConfig
    ) -> None:
        """
        Apply figure and axes-level styling.

        Parameters
        ----------
        context : PlotContext
            Rendering context containing figure and axes.

        chart_config : ChartConfig
            Styling configuration including colors and grid options.
        """

        style = chart_config.style

        if style.figure_facecolor is not None:
            context.figure.set_facecolor(
                color=style.figure_facecolor
            )

        if style.axes_facecolor is not None:
            context.primary_axes.set_facecolor(
                color=style.axes_facecolor
            )

            if context.overlay_axes is not None:
                context.overlay_axes.set_facecolor(
                    color=style.axes_facecolor
                )

        if chart_config.show_grid is True:
            context.primary_axes.grid(  # type: ignore
                visible=chart_config.show_grid,
                color=style.grid_color,
                alpha=style.grid_alpha,
                linestyle=style.grid_linestyle,
            )

    def _apply_labels(
        self,
        chart_config: ChartConfig,
        axes: Axes,
        overlay_axes: Optional[Axes]
    ) -> None:
        """
        Apply title and axis labels according to chart visibility rules.

        Parameters
        ----------
        chart_config : ChartConfig
            Chart configuration containing label text and visibility flags.

        axes : Axes
            Primary Matplotlib axes.

        overlay_axes : Optional[Axes]
            Optional secondary axes used for overlay y-axis labeling.
        """

        self._apply_label(
            visible=chart_config.visibility.show_title,
            value=chart_config.title,
            setter=axes.set_title  # type: ignore
        )

        self._apply_label(
            visible=chart_config.visibility.show_xlabel,
            value=chart_config.xlabel,
            setter=axes.set_xlabel  # type: ignore
        )

        self._apply_label(
            visible=chart_config.visibility.show_primary_ylabel,
            value=chart_config.primary_ylabel,
            setter=axes.set_ylabel  # type: ignore
        )

        if overlay_axes is not None:
            self._apply_label(
                visible=chart_config.visibility.show_overlay_ylabel,
                value=chart_config.overlay_ylabel,
                setter=overlay_axes.set_ylabel  # type: ignore
            )

            overlay_axes.yaxis.set_label_position('right')

    def _apply_ticks(
        self,
        axes: Axes,
        overlay_axes: Optional[Axes],
        chart_config: ChartConfig
    ) -> None:
        """
        Apply tick visibility rules to primary and overlay axes.

        Parameters
        ----------
        axes : Axes
            Primary Matplotlib axes.

        overlay_axes : Optional[Axes]
            Optional secondary axes used for overlay rendering.

        chart_config : ChartConfig
            Chart configuration containing tick visibility flags.
        """

        visibility = chart_config.visibility

        self._apply_tick_visibility(
            axes=axes,
            visible=visibility.show_xticks,
            axis='x'
        )

        self._apply_tick_visibility(
            axes=axes,
            visible=visibility.show_primary_yticks,
            axis='y'
        )

        if overlay_axes is not None:
            overlay_axes.tick_params(  # type: ignore
                axis='y',
                right=False,
                left=False,
                labelright=visibility.show_overlay_yticks
            )

    def _apply_legend(
        self,
        axes: Axes,
        chart_config: ChartConfig,
        overlay_axes: Optional[Axes]
    ) -> None:
        """
        Aggregate and apply legend entries for all rendered axes.

        Legend entries from primary and overlay axes are merged into a
        single legend attached to the primary axes.

        Parameters
        ----------
        axes : Axes
            Primary Matplotlib axes.

        chart_config : ChartConfig
            Chart configuration controlling legend visibility.

        overlay_axes : Optional[Axes]
            Secondary axes used for overlay plots.
        """

        if not chart_config.show_legend:
            return

        handles, labels = axes.get_legend_handles_labels()
        all_handles = list(handles)
        all_labels = list(labels)

        if overlay_axes is not None:
            overlay_handles, overlay_labels = \
                overlay_axes.get_legend_handles_labels()
            all_handles.extend(overlay_handles)
            all_labels.extend(overlay_labels)

        if all_handles:
            axes.legend(  # type: ignore
                handles=all_handles,
                labels=all_labels
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _apply_label(
        self,
        visible: bool,
        value: Optional[str],
        setter: Callable[[str], None]
    ) -> None:
        """
        Set a label only when it is marked visible and has a value.

        Parameters
        ----------
        visible : bool
            Whether the label should be applied.

        value : Optional[str]
            Label text to apply.

        setter : Callable[[str], None]
            Callable used to assign the label text.

        Notes
        -----
        The label is skipped when visibility is disabled or when the
        label value is empty.
        """

        if visible and value:
            setter(value)

    def _apply_tick_visibility(
        self,
        axes: Axes,
        visible: bool,
        axis: Literal["x", "y"]
    ) -> None:
        """
        Configure tick label visibility for a single axis.

        Parameters
        ----------
        axes : Axes
            Target Matplotlib axes.

        visible : bool
            Whether tick labels should be visible.

        axis : {"x", "y"}
            Axis direction to configure.
        """

        if axis == "x":
            axes.tick_params(  # type: ignore
                axis="x",
                which="both",
                top=False,
                bottom=False,
                labelbottom=visible
            )

        elif axis == "y":
            axes.tick_params(  # type: ignore
                axis="y",
                right=False,
                left=False,
                labelleft=visible
            )
