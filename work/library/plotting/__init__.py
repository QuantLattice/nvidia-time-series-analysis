"""
Reusable matplotlib chart builders for stock data visualization.

Each builder accepts a pandas DataFrame and a typed configuration
object, and returns a standalone ``matplotlib.figure.Figure`` that can
be embedded in tkinter via ``FigureCanvasTkAgg`` or exported to PNG/PDF.

Included builders
-----------------
ClusteredBarChart
    Grouped bar chart comparing multiple numeric columns per category.

CategorizedHistogram
    Overlapping histograms per category for distribution comparison.

Boxplot
    Box-and-whisker plot for distribution and outlier visualization.

CategorizedScatterPlot
    Scatter plot with per-category color encoding.
"""

from .clustered_bar import ClusteredBarChart, ClusteredBarConfig
from .categorized_histogram import CategorizedHistogram, CategorizedHistogramConfig
from .boxplot import Boxplot, BoxplotConfig
from .scatter_plot import CategorizedScatterPlot, ScatterPlotConfig


__all__ = [
    "ClusteredBarChart",
    "ClusteredBarConfig",
    "CategorizedHistogram",
    "CategorizedHistogramConfig",
    "Boxplot",
    "BoxplotConfig",
    "CategorizedScatterPlot",
    "ScatterPlotConfig",
]
