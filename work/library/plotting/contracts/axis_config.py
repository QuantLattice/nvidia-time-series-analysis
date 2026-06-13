"""
Axis visibility and chart style configuration dataclasses.

This module defines configuration objects that control per-axis
visibility of chart elements and global chart styling.

- AxisVisibilityConfig: visibility flags for chart elements
- ChartStyle: figure and grid appearance properties

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from typing import Optional

from .types import LineStyleLiteral


@dataclass(slots=True)
class AxisVisibilityConfig:
    """
    Visibility configuration for chart elements.

    Controls which visual components of a chart are rendered,
    including titles, labels, ticks, grid, and legend.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Visibility flags
    # ------------------------------------------------------------------

    show_title: bool = True

    show_xlabel: bool = True
    show_primary_ylabel: bool = True
    show_overlay_ylabel: bool = True

    show_xticks: bool = True
    show_primary_yticks: bool = True
    show_overlay_yticks: bool = True

    show_grid: bool = True
    show_legend: bool = True

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Reset all visibility flags to their default values.

        This restores the configuration to a fully visible chart
        state.
        """

        self.show_title = True

        self.show_xlabel = True
        self.show_primary_ylabel = True
        self.show_overlay_ylabel = True

        self.show_xticks = True
        self.show_primary_yticks = True
        self.show_overlay_yticks = True

        self.show_grid = True
        self.show_legend = True


@dataclass(slots=True)
class ChartStyle:
    """
    Styling configuration for chart-level appearance.

    Defines global visual properties such as figure background,
    axes background, and grid styling.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    # ------------------------------------------------------------------
    # Figure appearance
    # ------------------------------------------------------------------

    figure_facecolor: Optional[str] = None
    axes_facecolor: Optional[str] = None

    # ------------------------------------------------------------------
    # Grid appearance
    # ------------------------------------------------------------------

    grid_color: str = "#B0B0B0"
    grid_alpha: Optional[float] = None
    grid_linestyle: LineStyleLiteral = '-'

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """
        Reset chart style to default Matplotlib-like appearance.
        """

        self.figure_facecolor = None
        self.axes_facecolor = None

        self.grid_color = "#B0B0B0"
        self.grid_alpha = None
        self.grid_linestyle = '-'
