"""
Clustered bar chart for comparing multiple numeric columns per category.

Each unique value in the group column forms one cluster on the x-axis;
each numeric column becomes a bar within that cluster.
"""

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402


@dataclass(frozen=True)
class ClusteredBarConfig:
    """
    Configuration for a clustered bar chart.

    Attributes
    ----------
    group_column : str
        Categorical column used to form bar clusters on the x-axis.

    value_columns : List[str]
        Numeric columns rendered as individual bars within each cluster.

    agg : str
        Aggregation applied per group before plotting (e.g. 'mean').

    title : str
        Chart title.

    xlabel : str
        X-axis label. Defaults to group_column when empty.

    ylabel : str
        Y-axis label.

    figsize : Tuple[int, int]
        Figure dimensions in inches (width, height).
    """

    group_column: str
    value_columns: List[str]
    agg: str = "mean"
    title: str = "Clustered Bar Chart"
    xlabel: str = ""
    ylabel: str = "Value"
    figsize: Tuple[int, int] = (10, 6)


class ClusteredBarChart:
    """
    Builds a grouped bar chart from a DataFrame.

    Each unique value in ``config.group_column`` becomes a cluster on
    the x-axis; each column in ``config.value_columns`` becomes a bar
    within that cluster, computed with ``config.agg``.
    """

    def build(
        self,
        df: pd.DataFrame,
        config: ClusteredBarConfig,
    ) -> Figure:
        """
        Build and return a clustered bar chart figure.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        config : ClusteredBarConfig
            Chart configuration.

        Returns
        -------
        Figure
            Standalone matplotlib figure ready for embedding or export.
        """

        available = [c for c in config.value_columns if c in df.columns]
        grouped = df.groupby(config.group_column)[available].agg(config.agg)

        categories = grouped.index.tolist()
        n_groups = len(categories)
        n_bars = len(available)
        x = np.arange(n_groups)
        bar_width = 0.8 / max(n_bars, 1)

        fig = Figure(figsize=config.figsize, tight_layout=True)
        ax = fig.add_subplot(111)

        for i, col in enumerate(available):
            offset = (i - n_bars / 2) * bar_width + bar_width / 2
            ax.bar(x + offset, grouped[col], width=bar_width, label=col)

        ax.set_title(config.title)
        ax.set_xlabel(config.xlabel or config.group_column)
        ax.set_ylabel(config.ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels([str(c) for c in categories], rotation=45, ha="right")
        ax.legend()

        return fig
