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

Chart-configuration getters and setters live in
``PlotSessionConfigMixin`` (see ``session_config_mixin.py``).

Notes
-----
This implementation uses lazy figure creation and a context-based
rendering flow. The active plot context is created only when needed
and reused until the figure is explicitly released.
"""


from typing import List, Optional, Self, Iterable
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from work.library.plotting import LayerStack
from work.library.plotting.contracts import (
    FigureConfig,
    ChartConfig,
    PlotLayer,
    PlotContext,
)
from work.library.plotting.rendering import Renderer, MatplotlibRenderer
from work.library.plotting.session_config_mixin import (
    PlotSessionConfigMixin,
)


class PlotSession(PlotSessionConfigMixin):
    """
    Stateful plotting session.

    Stores the layer stack, figure and chart configuration, the active
    renderer, and an optional live figure context. The API is fluent so
    layers and labels can be assembled before rendering.

    Chart-configuration getters and setters are inherited from
    ``PlotSessionConfigMixin``.

    Notes
    -----
    Rendering is delegated to the configured renderer. Figure creation
    is performed lazily on the first ``render()`` call.
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        renderer: Optional[Renderer] = None,
        figure_config: Optional[FigureConfig] = None,
        chart_config: Optional[ChartConfig] = None,
    ) -> None:
        """
        Initialize a plotting session.

        Parameters
        ----------
        renderer : Optional[Renderer], optional
            Rendering backend. Defaults to ``MatplotlibRenderer``.
        figure_config : Optional[FigureConfig], optional
            Figure-level configuration. Defaults to ``FigureConfig()``.
        chart_config : Optional[ChartConfig], optional
            Chart-level configuration. Defaults to ``ChartConfig()``.

        Notes
        -----
        The session starts dirty so the first ``render()`` call
        produces a fresh figure context.
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

    def add_layer(self, layer: PlotLayer) -> Self:
        """Append a single plot layer to the session."""
        self._stack.add_layer(layer=layer)
        return self._mark_dirty()

    def add_layers(self, layers: Iterable[PlotLayer]) -> Self:
        """Append multiple plot layers to the session."""
        self._stack.extend(layers=layers)
        return self._mark_dirty()

    def remove_layer(self, layer: PlotLayer) -> Self:
        """Remove a plot layer from the session."""
        self._stack.remove_layer(layer=layer)
        return self._mark_dirty()

    def remove_layer_by_id(self, layer_id: str) -> Self:
        """Remove a plot layer by its identifier."""
        self._stack.remove_by_id(layer_id=layer_id)
        return self._mark_dirty()

    def get_layer_by_id(
        self, layer_id: str
    ) -> Optional[PlotLayer]:
        """Return a plot layer by its identifier, or None."""
        return self._stack.get_by_id(layer_id=layer_id)

    def get_layers(self) -> List[PlotLayer]:
        """Return all layers in insertion order."""
        return self._stack.get_all()

    def contains_layer(self, layer_id: str) -> bool:
        """Return True if a layer with *layer_id* exists."""
        return self.get_layer_by_id(layer_id=layer_id) is not None

    def clear_layers(self) -> Self:
        """
        Remove all layers from the session.

        Notes
        -----
        Does not close the active figure or reset chart metadata.
        """
        self._stack.clear()
        return self._mark_dirty()

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def has_figure(self) -> bool:
        """Return True if an active figure context exists."""
        return self._context is not None

    def has_layers(self) -> bool:
        """Return True if at least one layer is stored."""
        return self.layer_count() > 0

    def has_overlay_layers(self) -> bool:
        """Return True if one or more overlay layers are present."""
        return self._stack.has_overlay_layers()

    def layer_count(self) -> int:
        """Return the number of stored plot layers."""
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
        When the session is not dirty and a live figure context exists,
        the cached figure is returned without re-rendering.
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

    def show(self, block: bool = True) -> Figure:
        """
        Render and display the figure, then release the context.

        Parameters
        ----------
        block : bool, default=True
            Whether to block until the figure window is closed.

        Returns
        -------
        Figure
            Displayed Matplotlib figure.
        """

        fig = self.render()
        plt.show(block=block)  # type: ignore
        self.clear_figure()
        return fig

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def clear_metadata(self) -> Self:
        """Reset chart metadata to default values."""
        self._chart_config.reset()
        return self._mark_dirty()

    def clear_figure(self) -> Self:
        """
        Close and release the active Matplotlib figure.

        Notes
        -----
        Does not clear the layer stack or reset chart metadata.
        Use ``reset()`` to clear the entire session state.
        """
        if self._context is not None:
            plt.close(fig=self._context.figure)
            self._context = None
        return self._mark_dirty()

    def reset(self) -> Self:
        """Clear layers, metadata, and the active figure context."""
        self.clear_layers()
        self.clear_metadata()
        self.clear_figure()
        return self._mark_dirty()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _mark_dirty(self) -> Self:
        """Mark the session as requiring re-rendering."""
        self._dirty = True
        return self

    def _ensure_context(self) -> PlotContext:
        """
        Return the active plot context, creating one if necessary.

        A secondary overlay axes is created only when overlay layers
        are present or when an overlay y-label is explicitly enabled.

        Returns
        -------
        PlotContext
            Active plot context.
        """

        if self._context is not None:
            fig = self._context.figure
            if plt.fignum_exists(num=fig.number):
                return self._context

        figure, primary_axes = plt.subplots(  # type: ignore
            figsize=self._figure_config.figsize,
            dpi=self._figure_config.dpi,
        )

        overlay_axes = None
        if self.has_overlay_layers() or (
            self.overlay_ylabel is not None
            and self.show_overlay_ylabel is True
        ):
            overlay_axes = primary_axes.twinx()

        self._context = PlotContext(
            figure=figure,
            primary_axes=primary_axes,
            overlay_axes=overlay_axes,
        )

        return self._context
