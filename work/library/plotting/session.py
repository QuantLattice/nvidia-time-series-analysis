"""
Plotting session orchestration.

This module defines the session object used to collect plot layers,
store chart metadata, and trigger rendering through a configured
renderer backend.

The session provides a fluent interface for:
- adding layers;
- setting chart labels;
- resetting session state;
- rendering the final figure.
"""


from typing import Optional, Self, Iterable
from matplotlib.figure import Figure

from work.library.plotting import (
    LayerStack
)
from work.library.plotting.contracts import (
    FigureConfig,
    ChartConfig,
    PlotLayer
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
    - the active rendering backend.

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
            Rendering backend used to convert the layer stack into a figure.
            If omitted, the default Matplotlib renderer is used.

        figure_config : Optional[FigureConfig], optional
            Figure-level configuration. If omitted, default values are used.

        chart_config : Optional[ChartConfig], optional
            Chart-level visual configuration.
            If omitted, default values are used.
        """

        self._renderer = renderer or MatplotlibRenderer()
        self._figure_config = figure_config or FigureConfig()
        self._chart_config = chart_config or ChartConfig()

        self._stack = LayerStack()

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

    def title(
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

    def xlabel(
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

    def ylabel(
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

    def get_stack(self) -> LayerStack:
        """
        Return the current plot layer stack.

        Returns
        -------
        LayerStack
            Active session layer stack.
        """

        return self._stack

    def get_title(self) -> Optional[str]:
        """
        Return the current chart title.

        Returns
        -------
        Optional[str]
            Current title text, or None if not set.
        """

        return self._chart_config.title

    def get_xlabel(self) -> Optional[str]:
        """
        Return the current x-axis label.

        Returns
        -------
        Optional[str]
            Current x-axis label, or None if not set.
        """

        return self._chart_config.xlabel

    def get_ylabel(self) -> Optional[str]:
        """
        Return the current y-axis label.

        Returns
        -------
        Optional[str]
            Current y-axis label, or None if not set.
        """

        return self._chart_config.ylabel

    def reset(self) -> None:
        """
        Reset the session to an empty plotting state.

        This method clears all stored layers and resets chart metadata
        to default values.

        Returns
        -------
        None
            Session state is reset by side effect.
        """

        self._stack.clear()

        self._chart_config.reset()

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
        Rendering is delegated to the configured renderer backend using the
        current layer stack, figure configuration, and chart configuration.
        """

        return self._renderer.render(
            stack=self._stack,
            figure_config=self._figure_config,
            chart_config=self._chart_config
        )
