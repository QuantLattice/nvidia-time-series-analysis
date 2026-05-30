"""
Plotting configuration contracts.

This module defines reusable dataclass-based configuration objects
used to control figure-level and chart-level rendering behavior.

The configuration layer separates visual settings from rendering
logic and is shared by plot layers, rendering backends, and session
management components.
"""


from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(slots=True)
class FigureConfig:
    """
    Figure-level rendering configuration.

    Attributes
    ----------
    figsize : Tuple[float, float], default=(12.0, 6.0)
        Figure size in inches.

    dpi : float, default=100.0
        Figure resolution in dots per inch.

    tight_layout : bool, default=True
        Whether to apply tight layout adjustment after rendering.
    """

    figsize: Tuple[float, float] = (12.0, 6.0)
    dpi: float = 100.0
    tight_layout: bool = True


@dataclass(slots=True)
class ChartConfig:
    """
    Chart-level visual configuration.

    Attributes
    ----------
    title : Optional[str], default=None
        Chart title.

    xlabel : Optional[str], default=None
        Label for the x-axis.

    ylabel : Optional[str], default=None
        Label for the y-axis.

    show_grid : bool, default=True
        Whether grid lines should be displayed.

    show_legend : bool, default=True
        Whether legend should be displayed when available.
    """

    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None

    show_grid: bool = True
    show_legend: bool = True

    def reset(self):
        """
        Reset chart metadata to its default state.

        This method clears chart title and axis labels while preserving
        display preferences such as grid and legend visibility.
        """

        self.title = None
        self.xlabel = None
        self.ylabel = None
