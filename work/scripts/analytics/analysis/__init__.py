"""
High-level analysis wrappers for exploratory data analysis.

This package combines low-level statistical functions into convenient
report-oriented analysis classes. The analysis layer is responsible
for turning scalar statistics and feature summaries into structured
report objects that are easier to consume in the GUI and reporting
modules.

Included analysis groups
------------------------
Descriptive analysis
    Central tendency, dispersion, distribution shape, and data quality.

Rolling analysis
    Window-based local statistics for time-series diagnostics.

Distribution analysis
    Quantiles, outliers, histograms, and empirical CDF summaries.

Correlation analysis
    Pairwise correlation screening and ranking.

Categorical analysis
    Category frequencies, dominance, entropy, and imbalance metrics.
"""


from .descriptive_statistics import (
    DescriptiveAnalysis,
    SeriesDescriptiveReport
)
from .rolling_analysis import (
    RollingAnalysis,
    RollingSeriesReport
)
from .distribution_statistics import (
    DistributionAnalysis,
    DistributionAnalysisReport
)
from .correlation_analysis import (
    CorrelationAnalysis,
    CorrelationAnalysisReport
)
from .categorical_analysis import (
    CategoricalAnalysis,
    CategoricalAnalysisReport
)


__all__ = [
    "DescriptiveAnalysis",
    "SeriesDescriptiveReport",

    "RollingAnalysis",
    "RollingSeriesReport",

    "DistributionAnalysis",
    "DistributionAnalysisReport",

    "CorrelationAnalysis",
    "CorrelationAnalysisReport",

    "CategoricalAnalysis",
    "CategoricalAnalysisReport"
]
