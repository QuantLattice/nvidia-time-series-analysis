"""
High-level analysis layer for exploratory data analysis (EDA)
and time-series diagnostics.

This package aggregates low-level statistical functions into
structured, report-oriented analysis components.

The analysis layer is intended to provide ready-to-consume
results for:

- reporting systems;
- visualization layers;
- machine learning feature inspection;
- time-series diagnostics;
- batch processing of tabular datasets.

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
    Augmented Dickey-Fuller testing for time-series stationarity.

Autocorrelation analysis
    Autocorrelation and partial autocorrelation diagnostics for
    lag structure and temporal dependence.
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
from .autocorrelation_analysis import (
    AutocorrelationAnalysis,
    AutocorrelationReport,
    DataFrameAutocorrelationReport
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
    "DataFrameStationarityReport",

    "AutocorrelationAnalysis",
    "AutocorrelationReport",
    "DataFrameAutocorrelationReport"
]
