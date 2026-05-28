"""
Statistical utilities for exploratory data analysis.

This package provides reusable statistical helpers used throughout
the EDA pipeline, including:
- descriptive statistics;
- rolling statistics;
- distribution analysis;
- correlation analysis;
- categorical summary metrics.

The functions are designed to operate on pandas Series and return
scalar values, Series objects, or lightweight result containers
depending on the analysis task.
"""


from .descriptive_statistics import (
    mean,
    median,
    variance,
    std,
    data_range,
    min_value,
    max_value,
    skewness,
    kurtosis,
    missing_count,
    missing_ratio,
    positive_ratio,
    negative_ratio,
    zero_ratio,
    trimmed_mean,
    mad,
    coefficient_of_variation
)
from .rolling_statistics import (
    rolling_mean,
    rolling_std,
    rolling_min,
    rolling_max,
    rolling_zscore,
    rolling_volatility,
    rolling_momentum,
    rolling_rate_of_change,
    rolling_variance,
    rolling_cv
)
from .distribution_statistics import (
    quantiles,
    iqr,
    OutlierBounds,
    outlier_bounds,
    outlier_mask,
    histogram_bins,
    HistogramResult,
    empirical_cdf,
    EmpiricalCDFResult
)
from .correlation_analysis import (
    CorrelationMatrixResult,
    correlation_matrix,
    CorrelationPair,
    correlation_pairs,
    strong_correlation,
    top_positive_correlations,
    top_negative_correlations
)
from .categorical_statistics import (
    CategoryDistribution,
    category_distribution,
    dominant_category,
    category_entropy,
    imbalance_ratio
)

__all__ = [
    "mean",
    "median",
    "variance",
    "std",
    "data_range",
    "min_value",
    "max_value",
    "skewness",
    "kurtosis",
    "missing_count",
    "missing_ratio",
    "positive_ratio",
    "negative_ratio",
    "zero_ratio",
    "trimmed_mean",
    "mad",
    "coefficient_of_variation",

    "rolling_mean",
    "rolling_std",
    "rolling_min",
    "rolling_max",
    "rolling_zscore",
    "rolling_volatility",
    "rolling_momentum",
    "rolling_rate_of_change",
    "rolling_variance",
    "rolling_cv",

    "quantiles",
    "iqr",
    "OutlierBounds",
    "outlier_bounds",
    "outlier_mask",
    "histogram_bins",
    "HistogramResult",
    "empirical_cdf",
    "EmpiricalCDFResult",

    "CorrelationMatrixResult",
    "correlation_matrix",
    "CorrelationPair",
    "correlation_pairs",
    "strong_correlation",
    "top_positive_correlations",
    "top_negative_correlations",

    "CategoryDistribution",
    "category_distribution",
    "dominant_category",
    "category_entropy",
    "imbalance_ratio"
]
