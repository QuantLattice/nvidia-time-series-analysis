"""
Plotting configuration contracts.

This module defines reusable dataclass-based configuration objects
used to control figure-level and chart-level rendering behavior.

The configuration layer separates visual settings from rendering
logic and is shared by plot layers, rendering backends, and session
management components.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass, field
from typing import Tuple, Optional

from .axis_config import AxisVisibilityConfig, ChartStyle


@dataclass(slots=True)
class FigureConfig:
    """
    Configuration for Matplotlib figure-level properties.

    This object defines global figure settings such as size,
    resolution, and layout behavior.

    Attributes
    ----------
    figsize : Optional[Tuple[float, float]]
        Figure size in inches (width, height).

    dpi : Optional[float]
        Resolution of the figure in dots per inch.

    tight_layout : bool
        Whether to automatically apply tight layout after rendering.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    figsize: Optional[Tuple[float, float]] = None
    dpi: Optional[float] = None
    tight_layout: bool = False


@dataclass(slots=True)
class ChartConfig:
    """
    Root configuration object for chart rendering.

    This class aggregates all chart-level configuration including:

    - metadata (title, axis labels)
    - visibility rules
    - style configuration

    It acts as the central configuration contract shared between
    plot sessions, renderers, and plot layers.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Chart metadata
    # ------------------------------------------------------------------

    title: Optional[str] = None
    xlabel: Optional[str] = None
    primary_ylabel: Optional[str] = None

    overlay_ylabel: Optional[str] = None

    # ------------------------------------------------------------------
    # Nested configuration
    # ------------------------------------------------------------------

    visibility: AxisVisibilityConfig = field(
        default_factory=AxisVisibilityConfig
    )

    style: ChartStyle = field(
        default_factory=ChartStyle
    )

    # ------------------------------------------------------------------
    # Visibility properties
    # ------------------------------------------------------------------

    @property
    def show_title(self) -> bool:
        """
        Whether the chart title is visible.
        """
        return self.visibility.show_title

    @show_title.setter
    def show_title(self, value: bool) -> None:
        self.visibility.show_title = value

    # ------------------------------------------------------------------
    # Axis visibility properties
    # ------------------------------------------------------------------

    @property
    def show_xlabel(self) -> bool:
        """
        Whether the x-axis label is visible.
        """
        return self.visibility.show_xlabel

    @show_xlabel.setter
    def show_xlabel(self, value: bool) -> None:
        self.visibility.show_xlabel = value

    @property
    def show_primary_ylabel(self) -> bool:
        """
        Whether the primary y-axis label is visible.
        """
        return self.visibility.show_primary_ylabel

    @show_primary_ylabel.setter
    def show_primary_ylabel(self, value: bool) -> None:
        self.visibility.show_primary_ylabel = value

    @property
    def show_overlay_ylabel(self) -> bool:
        """
        Whether the overlay y-axis label is visible.
        """
        return self.visibility.show_overlay_ylabel

    @show_overlay_ylabel.setter
    def show_overlay_ylabel(self, value: bool) -> None:
        self.visibility.show_overlay_ylabel = value

    @property
    def show_xticks(self) -> bool:
        """
        Whether x-axis tick labels are visible.
        """
        return self.visibility.show_xticks

    @show_xticks.setter
    def show_xticks(self, value: bool) -> None:
        self.visibility.show_xticks = value

    @property
    def show_primary_yticks(self) -> bool:
        """
        Whether primary y-axis tick labels are visible.
        """
        return self.visibility.show_primary_yticks

    @show_primary_yticks.setter
    def show_primary_yticks(self, value: bool) -> None:
        self.visibility.show_primary_yticks = value

    @property
    def show_overlay_yticks(self) -> bool:
        """
        Whether overlay y-axis tick labels are visible.
        """
        return self.visibility.show_overlay_yticks

    @show_overlay_yticks.setter
    def show_overlay_yticks(self, value: bool) -> None:
        self.visibility.show_overlay_yticks = value

    # ------------------------------------------------------------------
    # Chart element visibility properties
    # ------------------------------------------------------------------

    @property
    def show_grid(self) -> bool:
        """
        Whether grid lines are visible.
        """
        return self.visibility.show_grid

    @show_grid.setter
    def show_grid(self, value: bool) -> None:
        self.visibility.show_grid = value

    @property
    def show_legend(self) -> bool:
        """
        Whether legend is visible.
        """
        return self.visibility.show_legend

    @show_legend.setter
    def show_legend(self, value: bool) -> None:
        self.visibility.show_legend = value

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Reset chart configuration to default state.

        This clears metadata (title, labels) while restoring default
        visibility and style settings.

        Notes
        -----
        This operation mutates the configuration object in-place.
        """

        self.title = None
        self.xlabel = None
        self.primary_ylabel = None

        self.overlay_ylabel = None

        self.visibility.reset()
        self.style.reset()
