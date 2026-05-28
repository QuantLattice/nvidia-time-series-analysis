"""
Categorized histogram for comparing value distributions across categories.

Renders overlapping semi-transparent histograms, one per unique value
of the category column, allowing direct visual distribution comparison.
"""

from dataclasses import dataclass
from typing import Tuple

import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402


@dataclass(frozen=True)
class CategorizedHistogramConfig:
    """
    Configuration for a categorized histogram.

    Attributes
    ----------
    value_column : str
        Numeric column whose distribution is plotted.

    category_column : str
        Categorical column used to split data into series.

    bins : int
        Number of histogram bins.

    alpha : float
        Opacity of each histogram layer (0.0 – 1.0).

    title : str
        Chart title.

    xlabel : str
        X-axis label. Defaults to value_column when empty.

    ylabel : str
        Y-axis label.

    figsize : Tuple[int, int]
        Figure dimensions in inches (width, height).
    """

    value_column: str
    category_column: str
    bins: int = 30
    alpha: float = 0.6
    title: str = "Categorized Histogram"
    xlabel: str = ""
    ylabel: str = "Frequency"
    figsize: Tuple[int, int] = (10, 6)


class CategorizedHistogram:
    """
    Builds overlapping histograms for each unique value in a category column.
    """

    def build(
        self,
        df: pd.DataFrame,
        config: CategorizedHistogramConfig,
    ) -> Figure:
        """
        Build and return a categorized histogram figure.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        config : CategorizedHistogramConfig
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
            values = df.loc[mask, config.value_column].dropna()
            ax.hist(
                values,
                bins=config.bins,
                alpha=config.alpha,
                label=str(cat),
                edgecolor="white",
                linewidth=0.4,
            )

        ax.set_title(config.title)
        ax.set_xlabel(config.xlabel or config.value_column)
        ax.set_ylabel(config.ylabel)
        ax.legend()

        return fig
