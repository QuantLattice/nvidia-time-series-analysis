"""
Boxplot visualization for distribution and outlier inspection.

Renders a side-by-side box-and-whisker chart for each selected numeric
column, with optional median lines and mean markers.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402


@dataclass(frozen=True)
class BoxplotConfig:
    """
    Configuration for a boxplot visualization.

    Attributes
    ----------
    columns : List[str]
        Numeric columns to include in the plot.

    title : str
        Chart title.

    xlabel : str
        X-axis label.

    ylabel : str
        Y-axis label.

    figsize : Tuple[int, int]
        Figure dimensions in inches (width, height).

    notch : bool
        Draw notched boxes to indicate confidence interval around median.

    show_means : bool
        Overlay mean marker and mean line on each box.
    """

    columns: List[str] = field(default_factory=list)
    title: str = "Boxplot"
    xlabel: str = ""
    ylabel: str = "Value"
    figsize: Tuple[int, int] = (10, 6)
    notch: bool = False
    show_means: bool = True


class Boxplot:
    """
    Builds a side-by-side boxplot for selected numeric columns.

    Columns absent from the DataFrame are silently ignored.
    """

    def build(
        self,
        df: pd.DataFrame,
        config: BoxplotConfig,
    ) -> Figure:
        """
        Build and return a boxplot figure.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        config : BoxplotConfig
            Chart configuration.

        Returns
        -------
        Figure
            Standalone matplotlib figure ready for embedding or export.
        """

        available = [c for c in config.columns if c in df.columns]
        if not available:
            available = list(df.select_dtypes(include="number").columns)

        data = [df[col].dropna().values for col in available]

        fig = Figure(figsize=config.figsize, tight_layout=True)
        ax = fig.add_subplot(111)

        bp = ax.boxplot(
            data,
            tick_labels=available,
            notch=config.notch,
            showmeans=config.show_means,
            meanline=config.show_means,
            patch_artist=True,
        )

        colors = [
            "#4C72B0", "#DD8452", "#55A868", "#C44E52",
            "#8172B2", "#937860", "#DA8BC3", "#8C8C8C",
        ]
        for patch, color in zip(bp["boxes"], colors * (len(available) // len(colors) + 1)):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        ax.set_title(config.title)
        ax.set_xlabel(config.xlabel)
        ax.set_ylabel(config.ylabel)
        ax.tick_params(axis="x", rotation=45)

        return fig
