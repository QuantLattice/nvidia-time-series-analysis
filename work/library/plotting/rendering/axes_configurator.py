"""
Mixin providing axis configuration and legend methods.

This module contains `AxesConfigurator`, a mixin class that
encapsulates axis styling, label application, tick visibility,
and legend aggregation logic extracted from the Matplotlib
renderer.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from typing import (
    Callable,
    Literal,
    Optional,
)
from matplotlib.axes import Axes

from work.library.plotting.contracts import (
    ChartConfig,
    PlotContext,
)


class AxesConfigurator:
    """
    Mixin that provides axis-configuration and legend methods.

    This class is intended to be used as a mixin for renderer
    implementations.  It supplies methods for applying styles,
    labels, tick visibility, and legends to Matplotlib axes
    derived from a `PlotContext` and a `ChartConfig`.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Style
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Labels
    # ------------------------------------------------------------------

    def _apply_labels(
        self,
        chart_config: ChartConfig,
        axes: Axes,
        overlay_axes: Optional[Axes]
    ) -> None:
        """
        Apply title and axis labels according to visibility rules.

        Parameters
        ----------
        chart_config : ChartConfig
            Chart configuration containing label text and visibility
            flags.

        axes : Axes
            Primary Matplotlib axes.

        overlay_axes : Optional[Axes]
            Optional secondary axes for overlay y-axis labeling.
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

    # ------------------------------------------------------------------
    # Ticks
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Legend
    # ------------------------------------------------------------------

    def _apply_legend(
        self,
        axes: Axes,
        chart_config: ChartConfig,
        overlay_axes: Optional[Axes]
    ) -> None:
        """
        Aggregate and apply legend entries for all rendered axes.

        Legend entries from primary and overlay axes are merged into
        a single legend attached to the primary axes.

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
