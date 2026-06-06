"""
Plotting session orchestration.

This module defines the session object used to collect plot layers,
manage chart metadata, and trigger rendering through a configured
renderer backend.

The session provides a fluent interface for:
- adding and removing layers;
- setting chart labels and visibility flags;
- querying session state;
- resetting the plotting state;
- rendering the final figure.

Notes
-----
This implementation uses lazy figure creation and a context-based
rendering flow. The active plot context is created only when needed
and reused until the figure is explicitly released.
"""


from typing import (
    List,
    Optional,
    Self,
    Iterable
)
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

    The session acts as the main orchestration object for chart creation.
    It stores:

    - the current layer stack;
    - figure-level configuration;
    - chart-level metadata;
    - the active rendering backend;
    - the active Matplotlib figure context;
    - a dirty-state flag indicating whether re-rendering is required.

    The API is intentionally fluent so that layers and labels can be
    assembled in a chainable style before rendering.

    Notes
    -----
    The session does not draw figures directly. Rendering is delegated
    to the configured renderer instance. Figure creation is performed
    lazily and only when the session is rendered for the first time.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

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
            Rendering backend used to convert the layer stack into a figure.
            If omitted, the default Matplotlib renderer is used.

        figure_config : Optional[FigureConfig], optional
            Figure-level configuration. If omitted, default values are used.

        chart_config : Optional[ChartConfig], optional
            Chart-level visual configuration. If omitted, default values are
            used.

        Notes
        -----
        The session starts in a dirty state so the first call to ``render()``
        creates and draws a fresh figure context.
        """

        self._renderer = renderer or MatplotlibRenderer()
        self._figure_config = figure_config or FigureConfig()
        self._chart_config = chart_config or ChartConfig()

        self._stack = LayerStack()
        self._context: Optional[PlotContext] = None
        self._dirty: bool = True

    # ------------------------------------------------------------------
    # Layer management
    # ------------------------------------------------------------------

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

        return self._mark_dirty()

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

        return self._mark_dirty()

    def remove_layer(
        self,
        layer: PlotLayer
    ) -> Self:
        """
        Remove a plot layer from the session.

        Parameters
        ----------
        layer : PlotLayer
            Plot layer to remove.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._stack.remove_layer(layer=layer)

        return self._mark_dirty()

    def remove_layer_by_id(
        self,
        layer_id: str
    ) -> Self:
        """
        Remove a plot layer by its identifier.

        Parameters
        ----------
        layer_id : str
            Identifier of the layer to remove.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._stack.remove_by_id(layer_id=layer_id)

        return self._mark_dirty()

    def get_layer_by_id(
        self,
        layer_id: str
    ) -> Optional[PlotLayer]:
        """
        Return a plot layer by its identifier.

        Parameters
        ----------
        layer_id : str
            Layer identifier.

        Returns
        -------
        Optional[PlotLayer]
            Matching plot layer, or None if not found.
        """

        return self._stack.get_by_id(layer_id=layer_id)

    def get_layers(
        self
    ) -> List[PlotLayer]:
        """
        Return all layers stored in the session.

        Returns
        -------
        List[PlotLayer]
            Copy of all plot layers in insertion order.
        """

        return self._stack.get_all()

    def contains_layer(
        self,
        layer_id: str
    ) -> bool:
        """
        Check whether a layer with the given identifier exists.

        Parameters
        ----------
        layer_id : str
            Layer identifier.

        Returns
        -------
        bool
            True if the layer is present, otherwise False.
        """

        return self.get_layer_by_id(layer_id=layer_id) is not None

    def clear_layers(self) -> Self:
        """
        Remove all layers from the session.

        Returns
        -------
        Self
            The current session instance for fluent chaining.

        Notes
        -----
        This method clears only the layer stack. It does not close the
        current figure or reset chart metadata.
        """

        self._stack.clear()

        return self._mark_dirty()

    # ------------------------------------------------------------------
    # Chart configuration
    # ------------------------------------------------------------------

    def set_title(
        self,
        value: str
    ) -> Self:
        """
        Set the chart title.

        Parameters
        ----------
        value : str
            Chart title text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.title = value

        return self._mark_dirty()

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

        return self._mark_dirty()

    def set_primary_ylabel(
        self,
        value: str
    ) -> Self:
        """
        Set the primary y-axis label.

        Parameters
        ----------
        value : str
            Primary y-axis label text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.primary_ylabel = value

        return self._mark_dirty()

    def set_overlay_ylabel(
        self,
        value: str
    ) -> Self:
        """
        Set the overlay y-axis label.

        Parameters
        ----------
        value : str
            Overlay y-axis label text.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.overlay_ylabel = value

        return self._mark_dirty()

    def set_show_xlabel(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of the x-axis label.

        Parameters
        ----------
        value : bool
            Whether the x-axis label should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_xlabel = value

        return self._mark_dirty()

    def set_show_primary_ylabel(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of the primary y-axis label.

        Parameters
        ----------
        value : bool
            Whether the primary y-axis label should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_primary_ylabel = value

        return self._mark_dirty()

    def set_show_overlay_ylabel(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of the overlay y-axis label.

        Parameters
        ----------
        value : bool
            Whether the overlay y-axis label should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_overlay_ylabel = value

        return self._mark_dirty()

    def set_show_title(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of the chart title.

        Parameters
        ----------
        value : bool
            Whether the chart title should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_title = value

        return self._mark_dirty()

    def set_show_xticks(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of x-axis tick labels.

        Parameters
        ----------
        value : bool
            Whether x-axis tick labels should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_xticks = value

        return self._mark_dirty()

    def set_show_primary_yticks(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of primary y-axis tick labels.

        Parameters
        ----------
        value : bool
            Whether primary y-axis tick labels should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_primary_yticks = value

        return self._mark_dirty()

    def set_show_overlay_yticks(
        self,
        value: bool
    ) -> Self:
        """
        Control visibility of overlay y-axis tick labels.

        Parameters
        ----------
        value : bool
            Whether overlay y-axis tick labels should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_overlay_yticks = value

        return self._mark_dirty()

    def set_show_grid(
        self,
        value: bool
    ) -> Self:
        """
        Control grid visibility.

        Parameters
        ----------
        value : bool
            Whether grid lines should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_grid = value

        return self._mark_dirty()

    def set_show_legend(
        self,
        value: bool
    ) -> Self:
        """
        Control legend visibility.

        Parameters
        ----------
        value : bool
            Whether the legend should be displayed.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.show_legend = value

        return self._mark_dirty()

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def has_figure(self) -> bool:
        """
        Check whether an active figure context exists.

        Returns
        -------
        bool
            True if the session has an active figure context, otherwise False.
        """

        return self._context is not None

    def has_layers(self) -> bool:
        """
        Check whether the session contains any layers.

        Returns
        -------
        bool
            True if at least one layer is stored, otherwise False.
        """

        return self.layer_count() > 0

    def has_overlay_layers(self) -> bool:
        """
        Check whether the session contains overlay layers.

        Returns
        -------
        bool
            True if one or more overlay layers are present, otherwise False.
        """

        return self._stack.has_overlay_layers()

    def layer_count(self) -> int:
        """
        Return the number of layers in the session.

        Returns
        -------
        int
            Number of stored plot layers.
        """

        return len(self._stack)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self) -> Figure:
        """
        Render the current plotting session.

        Returns
        -------
        Figure
            Rendered Matplotlib figure.

        Notes
        -----
        Rendering is skipped when the session is not dirty and an active
        figure context already exists. In that case, the cached figure is
        returned directly.

        If the session state changes, the next call to ``render()`` redraws
        the figure through the configured renderer backend.
        """

        context = self._ensure_context()

        if not self._dirty:
            return context.figure

        self._renderer.render(
            stack=self._stack,
            context=context,
            chart_config=self._chart_config,
        )

        if self._figure_config.tight_layout:
            context.figure.tight_layout()

        self._dirty = False

        return context.figure

    def show(
        self,
        block: bool = True
    ) -> Figure:
        """
        Render the session and display the resulting figure.

        Parameters
        ----------
        block : bool, default=True
            Whether to block execution until the figure window is closed.

        Returns
        -------
        Figure
            Displayed Matplotlib figure.

        Notes
        -----
        This method displays the current figure and then releases the active
        figure context. The layer stack and chart metadata are preserved.
        """

        fig = self.render()
        plt.show(block=block)  # type: ignore

        self.clear_figure()

        return fig

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def clear_metadata(self) -> Self:
        """
        Reset chart metadata to default values.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._chart_config.reset()

        return self._mark_dirty()

    def clear_figure(self) -> Self:
        """
        Close and release the active Matplotlib figure.

        Returns
        -------
        Self
            The current session instance for fluent chaining.

        Notes
        -----
        This method closes only the active figure context. It does not clear
        the layer stack or reset chart metadata. Use ``reset()`` to clear the
        entire session state.
        """

        if self._context is not None:
            plt.close(fig=self._context.figure)

            self._context = None

        return self._mark_dirty()

    def reset(self) -> Self:
        """
        Reset the session to a clean plotting state.

        This method clears the layer stack, resets chart metadata, and
        releases the active figure context.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self.clear_layers()
        self.clear_metadata()
        self.clear_figure()

        return self._mark_dirty()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

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
    def primary_ylabel(self) -> Optional[str]:
        """
        Return the current primary y-axis label.

        Returns
        -------
        Optional[str]
            Current primary y-axis label, or None if not set.
        """

        return self._chart_config.primary_ylabel

    @property
    def overlay_ylabel(self) -> Optional[str]:
        """
        Return the current overlay y-axis label.

        Returns
        -------
        Optional[str]
            Current overlay y-axis label, or None if not set.
        """

        return self._chart_config.overlay_ylabel

    @property
    def show_title(self) -> bool:
        """
        Return whether the chart title is visible.

        Returns
        -------
        bool
            True if the chart title is displayed, otherwise False.
        """
        return self._chart_config.show_title

    @property
    def show_xlabel(self) -> bool:
        """
        Return whether the x-axis label is visible.

        Returns
        -------
        bool
            True if the x-axis label is displayed, otherwise False.
        """
        return self._chart_config.show_xlabel

    @property
    def show_primary_ylabel(self) -> bool:
        """
        Return whether the primary y-axis label is visible.

        Returns
        -------
        bool
            True if the primary y-axis label is displayed,
            otherwise False.
        """
        return self._chart_config.show_primary_ylabel

    @property
    def show_overlay_ylabel(self) -> bool:
        """
        Return whether the overlay y-axis label is visible.

        Returns
        -------
        bool
            True if the overlay y-axis label is displayed,
            otherwise False.
        """
        return self._chart_config.show_overlay_ylabel

    @property
    def show_xticks(self) -> bool:
        """
        Return whether x-axis tick labels are visible.

        Returns
        -------
        bool
            True if x-axis tick labels are displayed,
            otherwise False.
        """
        return self._chart_config.show_xticks

    @property
    def show_primary_yticks(self) -> bool:
        """
        Return whether primary y-axis tick labels are visible.

        Returns
        -------
        bool
            True if primary y-axis tick labels are displayed,
            otherwise False.
        """
        return self._chart_config.show_primary_yticks

    @property
    def show_overlay_yticks(self) -> bool:
        """
        Return whether overlay y-axis tick labels are visible.

        Returns
        -------
        bool
            True if overlay y-axis tick labels are displayed,
            otherwise False.
        """
        return self._chart_config.show_overlay_yticks

    @property
    def show_grid(self) -> bool:
        """
        Return whether chart grid lines are visible.

        Returns
        -------
        bool
            True if grid lines are displayed, otherwise False.
        """
        return self._chart_config.show_grid

    @property
    def show_legend(self) -> bool:
        """
        Return whether the chart legend is visible.

        Returns
        -------
        bool
            True if the legend is displayed, otherwise False.
        """
        return self._chart_config.show_legend

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _mark_dirty(self) -> Self:
        """
        Mark the session as requiring re-rendering.

        Returns
        -------
        Self
            The current session instance for fluent chaining.
        """

        self._dirty = True
        return self

    def _ensure_context(self) -> PlotContext:
        """
        Ensure that the session has an active plot context.

        If a valid context already exists and its figure is still alive,
        it is reused. Otherwise, a new Matplotlib figure and axes are
        created.

        Returns
        -------
        PlotContext
            Active plot context.

        Notes
        -----
        A secondary overlay axes is created only when overlay layers are
        present or when overlay labels are explicitly enabled.
        """

        if self._context is not None:
            fig = self._context.figure
            if plt.fignum_exists(num=fig.number):
                return self._context

        figure, primary_axes = plt.subplots(  # type: ignore
            figsize=self._figure_config.figsize,
            dpi=self._figure_config.dpi
        )

        overlay_axes = None
        if (
            self.has_overlay_layers() or
            (
                self.overlay_ylabel is not None
                and self.show_overlay_ylabel is True
            )
        ):
            overlay_axes = primary_axes.twinx()

        context = PlotContext(
            figure=figure,
            primary_axes=primary_axes,
            overlay_axes=overlay_axes
        )

        self._context = context

        return context
