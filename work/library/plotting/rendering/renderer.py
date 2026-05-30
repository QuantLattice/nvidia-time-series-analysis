"""
Abstract rendering interface for the plotting subsystem.

This module defines the renderer contract used by plotting sessions
to transform a stack of plot layers into a concrete figure object.

Concrete implementations are expected to:
- accept a layered plot stack;
- apply figure-level configuration;
- render all plot layers;
- return a fully constructed Matplotlib figure.
"""


from abc import ABC, abstractmethod
from matplotlib.figure import Figure

from work.library.plotting.contracts import (
    FigureConfig,
    ChartConfig,
)
from work.library.plotting import (
    LayerStack
)


class Renderer(ABC):
    """
    Abstract base class for plotting renderers.

    A renderer is responsible for converting a stack of plot layers into
    a final figure using a specific rendering backend.

    Subclasses must implement the rendering behavior for the selected
    backend.

    Parameters
    ----------
    None
        The class itself does not store rendering state.
    """

    @abstractmethod
    def render(
        self,
        stack: LayerStack,
        figure_config: FigureConfig,
        chart_config: ChartConfig,
    ) -> Figure:
        """
        Render a plot stack into a Matplotlib figure.

        Parameters
        ----------
        stack : LayerStack
            Stack of plot layers to render.

        figure_config : FigureConfig
            Figure-level rendering configuration.

        chart_config : ChartConfig
            Chart-level visual configuration.

        Returns
        -------
        Figure
            Rendered Matplotlib figure.

        Notes
        -----
        Subclasses must implement this method.
        """

        ...
