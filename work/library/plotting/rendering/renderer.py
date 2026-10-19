"""
Abstract rendering interface for the plotting subsystem.

This module defines the renderer contract used by plotting sessions
to transform a stack of plot layers into a rendered plot context.

A renderer is responsible for:

- traversing plot layers;
- selecting the appropriate axes;
- applying chart-level configuration;
- coordinating the rendering pipeline.

The plotting session owns figure creation and lifecycle management.
Renderers operate on an existing ``PlotContext`` and do not create
or destroy figures themselves.
"""


from abc import ABC, abstractmethod

from work.library.plotting.contracts import (
    PlotContext,
    ChartConfig,
)
from work.library.plotting import (
    LayerStack
)


class Renderer(ABC):
    """
    Abstract base class for plotting renderers.

    A renderer is responsible for drawing a layer stack into an
    existing plotting context using a specific rendering backend.

    Concrete implementations typically coordinate:

    - layer rendering;
    - axis selection;
    - chart metadata application;
    - legend construction.

    Notes
    -----
    Renderers do not manage figure creation. Figure lifecycle is
    controlled by the active plotting session.
    """

    @abstractmethod
    def render(
        self,
        stack: LayerStack,
        context: PlotContext,
        chart_config: ChartConfig,
    ) -> None:
        """
        Render a layer stack into a plotting context.

        Parameters
        ----------
        stack : LayerStack
            Collection of plot layers to render.

        context : PlotContext
            Active plotting context containing the figure and axes
            used during rendering.

        chart_config : ChartConfig
            Chart-level visual configuration applied after all
            layers have been rendered.

        Returns
        -------
        None
            Rendering is performed by side effect on the provided
            plotting context.

        Notes
        -----
        Implementations should render all layers contained in the
        stack and apply chart-level configuration to the target
        axes.
        """

        ...
