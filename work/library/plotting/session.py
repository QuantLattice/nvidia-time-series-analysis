"""
Plotting session orchestration.

This module defines the session object used to collect plot layers,
manage chart metadata, and trigger rendering through a configured
renderer backend.

The session provides a fluent interface for:
- adding layers;
- setting chart labels;
- resetting session state;
- rendering the final figure.

Notes
-----
This implementation assumes a context-based rendering flow using
``PlotContext`` objects.
"""


from typing import Optional, Self, Iterable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from work.library.plotting import (
    LayerStack
)
from work.library.plotting.contracts import (
    FigureConfig,
    ChartConfig,
    PlotLayer,
    PlotContext
)
from work.library.plotting.rendering import (
    Renderer,
    MatplotlibRenderer
)


class PlotSession:
    """
    Stateful plotting session.

    The session acts as the main orchestration object for chart
    creation. It stores:

    - the current layer stack;
    - figure-level configuration;
    - chart-level metadata;
    - the active rendering backend;
    - the active Matplotlib figure context.

    The API is intentionally fluent so that layers and labels can be
    assembled in a chainable style before rendering.

    Notes
    -----
    The session does not draw figures directly. Rendering is delegated
    to the configured renderer instance.
    """

    # ==========================================
    # CONSTRUCTION
    # ==========================================

    def __init__(
        self,
        renderer: Optional[Renderer] = None,
        figure_config: Optional[FigureConfig] = None,
        chart_config: Optional[ChartConfig] = None
    ) -> None:
        """
        Initialize a plotting session.

        Parameters
        ----------
        renderer : Optional[Renderer], optional
            Rendering backend used to convert the layer stack into a
            figure. If omitted, the default Matplotlib renderer is used.

        figure_config : Optional[FigureConfig], optional
            Figure-level configuration. If omitted, default values are
            used.

        chart_config : Optional[ChartConfig], optional
            Chart-level visual configuration. If omitted, default values
            are used.
        """

        self._renderer = renderer or MatplotlibRenderer()
        self._figure_config = figure_config or FigureConfig()
        self._chart_config = chart_config or ChartConfig()

        self._stack = LayerStack()
        self._context: Optional[PlotContext] = None

    # ==========================================
    # LAYER MANAGEMENT
    # ==========================================

    def add_layer(
        self,
        layer: PlotLayer
    ) -> Self:
        """
        Add a single plot layer to the session.

        Parameters
        ----------
        layer : PlotLayer
            Plot layer to append to the current stack.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._stack.add_layer(layer=layer)
        return self

    def add_layers(
        self,
        layers: Iterable[PlotLayer]
    ) -> Self:
        """
        Add multiple plot layers to the session.

        Parameters
        ----------
        layers : Iterable[PlotLayer]
            Iterable of plot layers to append.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._stack.extend(layers=layers)
        return self

    # ==========================================
    # CHART METADATA
    # ==========================================

    def set_title(
        self,
        value: str
    ) -> Self:
        """
        Set the chart title.

        Parameters
        ----------
        value : str
            Title text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.title = value
        return self

    def set_xlabel(
        self,
        value: str
    ) -> Self:
        """
        Set the x-axis label.

        Parameters
        ----------
        value : str
            X-axis label text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.xlabel = value
        return self

    def set_ylabel(
        self,
        value: str
    ) -> Self:
        """
        Set the y-axis label.

        Parameters
        ----------
        value : str
            Y-axis label text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.ylabel = value
        return self

    @property
    def title(self) -> Optional[str]:
        """
        Return the current chart title.

        Returns
        -------
        Optional[str]
            Current title text, or None if not set.
        """

        return self._chart_config.title

    @property
    def xlabel(self) -> Optional[str]:
        """
        Return the current x-axis label.

        Returns
        -------
        Optional[str]
            Current x-axis label, or None if not set.
        """

        return self._chart_config.xlabel

    @property
    def ylabel(self) -> Optional[str]:
        """
        Return the current y-axis label.

        Returns
        -------
        Optional[str]
            Current y-axis label, or None if not set.
        """

        return self._chart_config.ylabel

    # ==========================================
    # STATE MANAGEMENT
    # ==========================================

    def clear_layers(self) -> Self:
        """
        Remove all layers from the session.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._stack.clear()

        return self

    def clear_metadata(self) -> Self:
        """
        Reset chart metadata to default values.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.reset()

        return self

    def clear_figure(self) -> Self:
        """
        Close and release the active Matplotlib figure.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        if self._context is not None:
            plt.close(fig=self._context.figure)

            self._context = None

        return self

    def reset(self) -> Self:
        """
        Reset the session to an empty plotting state.

        This method clears all stored layers, resets chart metadata,
        and releases the active figure context.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self.clear_layers()
        self.clear_metadata()
        self.clear_figure()

        return self

    # ==========================================
    # INTROSPECTION
    # ==========================================

    def has_figure(self) -> bool:
        """
        Check whether a figure context already exists.

        Returns
        -------
        bool
            True if the session has an active figure context, otherwise
            False.
        """

        return self._context is not None

    def has_layers(self) -> bool:
        """
        Check whether the session contains at least one layer.

        Returns
        -------
        bool
            True if one or more layers are present, otherwise False.
        """

        return self.layer_count() > 0

    def layer_count(self) -> int:
        """
        Return the number of layers currently stored in the session.

        Returns
        -------
        int
            Number of plot layers in the stack.
        """

        return len(self._stack)

    # ==========================================
    # RENDERING
    # ==========================================

    def render(self) -> Figure:
        """
        Render the current plotting session.

        Returns
        -------
        Figure
            Rendered Matplotlib figure.

        Notes
        -----
        Rendering is delegated to the configured renderer backend using
        the current layer stack, figure configuration, chart
        configuration, and active plot context.
        """

        context = self._ensure_context()
        self._clear_axes()

        self._renderer.render(
            stack=self._stack,
            context=context,
            chart_config=self._chart_config
        )

        if self._figure_config.tight_layout:
            context.figure.tight_layout()

        return context.figure

    # ==========================================
    # INTERNAL
    # ==========================================

    def _ensure_context(self) -> PlotContext:
        """
        Ensure that the session has an active plot context.

        If no context exists, a new Matplotlib figure with primary and
        overlay axes is created and stored.

        Returns
        -------
        PlotContext
            Active plot context.
        """

        if self._context is not None:
            return self._context

        figure, primary_axes = plt.subplots(  # type: ignore
            figsize=self._figure_config.figsize,
            dpi=self._figure_config.dpi
        )

        overlay_axes = primary_axes.twinx()

        context = PlotContext(
            figure=figure,
            primary_axes=primary_axes,
            overlay_axes=overlay_axes
        )

        self._context = context

        return context

    def _clear_axes(self) -> None:
        """
        Clear all axes in the active figure context.

        Returns
        -------
        None
            Axes are cleared by side effect.
        """

        if self._context is None:
            return

        self._context.primary_axes.clear()
        self._context.overlay_axes.clear()
