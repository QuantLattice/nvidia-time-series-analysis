"""
Categorized scatter plot with per-category color encoding.

Renders a standard 2-D scatter plot where each point is colored
by its category, making cluster structure and group separation
immediately visible.
"""

from dataclasses import dataclass
from typing import Tuple

import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402


@dataclass(frozen=True)
class ScatterPlotConfig:
    """
    Configuration for a categorized scatter plot.

    Attributes
    ----------
    x_column : str
        Column mapped to the x-axis.

    y_column : str
        Column mapped to the y-axis.

    category_column : str
        Column used for per-category color encoding.

    title : str
        Chart title.

    alpha : float
        Point opacity (0.0 – 1.0).

    point_size : int
        Marker size in points².

    figsize : Tuple[int, int]
        Figure dimensions in inches (width, height).
    """

    x_column: str
    y_column: str
    category_column: str
    title: str = "Scatter Plot"
    alpha: float = 0.7
    point_size: int = 20
    figsize: Tuple[int, int] = (10, 6)


class CategorizedScatterPlot:
    """
    Builds a scatter plot with distinct colors per category.
    """

    def build(
        self,
        df: pd.DataFrame,
        config: ScatterPlotConfig,
    ) -> Figure:
        """
        Build and return a categorized scatter plot figure.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        config : ScatterPlotConfig
            Chart configuration.

        Returns
        -------
        Figure
            Standalone matplotlib figure ready for embedding or export.
        """

        fig = Figure(figsize=config.figsize, tight_layout=True)
        ax = fig.add_subplot(111)

        categories = sorted(df[config.category_column].dropna().unique())

        for cat in categories:
            mask = df[config.category_column] == cat
            subset = df.loc[mask]
            ax.scatter(
                subset[config.x_column],
                subset[config.y_column],
                label=str(cat),
                alpha=config.alpha,
                s=config.point_size,
            )

        ax.set_title(config.title)
        ax.set_xlabel(config.x_column)
        ax.set_ylabel(config.y_column)
        ax.legend()

        return fig
