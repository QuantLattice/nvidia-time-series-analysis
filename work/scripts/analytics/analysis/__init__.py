"""
High-level analysis layer for exploratory data analysis (EDA)
and time-series diagnostics.

This package aggregates low-level statistical functions into
structured, report-oriented analysis components.

It is designed to provide ready-to-consume analytical outputs
for:
- reporting systems;
- visualization layers;
- machine learning feature inspection;
- time-series diagnostics.

Included analysis groups
------------------------

Descriptive analysis
    Central tendency, dispersion, distribution shape, and data quality.

Rolling analysis
    Window-based local statistics for time-series behavior.

Distribution analysis
    Quantiles, outliers, histograms, and empirical distributions.

Correlation analysis
    Pairwise correlation matrices and ranked feature relationships.

Categorical analysis
    Frequency distributions, entropy, dominance, and imbalance metrics.

Stationarity analysis
    Time-series stationarity testing (ADF test) for structural stability.
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
from .stationarity_analysis import (
    StationarityAnalysis,
    StationarityReport,
    DataFrameStationarityReport
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
    "CategoricalAnalysisReport",

    "StationarityAnalysis",
    "StationarityReport",
    "DataFrameStationarityReport"
]
