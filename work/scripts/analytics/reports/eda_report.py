"""
High-level exploratory data analysis report generation.

This module combines the specialized analysis layers from the analytics
package into a unified EDA report object. The resulting report aggregates
descriptive, distributional, rolling-window, categorical, and correlation
analysis results for a given DataFrame.

The report is intended for:
- GUI rendering;
- CSV / table export;
- analytical summaries;
- downstream visualization workflows.
"""


from dataclasses import dataclass
from typing import Mapping, List, Literal, Optional
import pandas as pd

from work.scripts.analytics.analysis import (
    SeriesDescriptiveReport,
    DistributionAnalysisReport,
    RollingSeriesReport,
    CategoricalAnalysisReport,
    CorrelationAnalysisReport,
    DescriptiveAnalysis,
    DistributionAnalysis,
    RollingAnalysis,
    CategoricalAnalysis,
    CorrelationAnalysis
)
from work.scripts.analytics.constants import (
    DEFAULT_HISTOGRAM_BINS,
    DEFAULT_OUTLIER_IQR_MULTIPLIER,
    ROLLING_WINDOWS,
    DEFAULT_TRIM_RATIO,
    DEFAULT_QUANTILE_PROBS,
    DEFAULT_CORRELATION_METHOD,
    DEFAULT_TOP_CORRELATIONS_COUNT,
    DEFAULT_STRONG_CORRELATION_THRESHOLD
)


@dataclass(frozen=True)
class EDAReportResult:
    """
    Aggregated exploratory data analysis result.

    Attributes
    ----------
    descriptive : Mapping[str, SeriesDescriptiveReport]
        Descriptive analysis reports for numeric columns.

    distribution : Mapping[str, DistributionAnalysisReport]
        Distribution analysis reports for numeric columns.

    rolling : Mapping[str, Mapping[int, RollingSeriesReport]]
        Rolling-window analysis reports for numeric columns.

    categorical : Mapping[str, CategoricalAnalysisReport]
        Categorical analysis reports for categorical columns.

    correlation : Optional[CorrelationAnalysisReport]
        Correlation analysis report for numeric columns, or ``None``
        when the numeric subset contains fewer than two columns.
    """

    descriptive: Mapping[str, SeriesDescriptiveReport]

    distribution: Mapping[str, DistributionAnalysisReport]

    rolling: Mapping[str, Mapping[int, RollingSeriesReport]]

    categorical: Mapping[str, CategoricalAnalysisReport]

    correlation: Optional[CorrelationAnalysisReport]


class EDAReport:
    """
    Build a full exploratory data analysis report for a DataFrame.

    This class orchestrates the specialized analysis layers and merges
    their outputs into a single structured result object.

    The generated report contains:
    - descriptive statistics for numeric columns;
    - distribution statistics for numeric columns;
    - rolling-window statistics for numeric columns;
    - categorical statistics for categorical columns;
    - optional correlation analysis for numeric columns.
    """

    def __init__(self) -> None:
        """
        Initialize EDA report generator with default analysis engines.
        """

        self.descriptive_analysis = DescriptiveAnalysis()
        self.distribution_analysis = DistributionAnalysis()
        self.rolling_analysis = RollingAnalysis()
        self.categorical_analysis = CategoricalAnalysis()
        self.correlation_analysis = CorrelationAnalysis()

    def generate(
        self,
        df: pd.DataFrame,
        rolling_windows: List[int] = ROLLING_WINDOWS,
        quantile_probs: List[float] = DEFAULT_QUANTILE_PROBS,
        trim: float = DEFAULT_TRIM_RATIO,
        outlier_k: float = DEFAULT_OUTLIER_IQR_MULTIPLIER,
        histogram_bins_count: int = DEFAULT_HISTOGRAM_BINS,
        correlation_method: Literal[
            "pearson",
            "spearman",
            "kendall"
        ] = DEFAULT_CORRELATION_METHOD,
        strong_threshold: float = DEFAULT_STRONG_CORRELATION_THRESHOLD,
        top_n: int = DEFAULT_TOP_CORRELATIONS_COUNT
    ) -> EDAReportResult:
        """
        Generate a full exploratory data analysis report.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset to analyze.

        rolling_windows : Sequence[int], default=ROLLING_WINDOWS
            Rolling windows used for rolling analysis.

        quantile_probs : Sequence[float], default=DEFAULT_QUANTILE_PROBS
            Quantile probabilities used for distribution analysis.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        outlier_k : float, default=DEFAULT_OUTLIER_IQR_MULTIPLIER
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int, default=DEFAULT_HISTOGRAM_BINS
            Number of histogram bins used in distribution analysis.

        correlation_method : {'pearson', 'spearman', 'kendall'},
            default=DEFAULT_CORRELATION_METHOD
            Correlation method used for pairwise correlation analysis.

        strong_threshold : float, default=DEFAULT_STRONG_CORRELATION_THRESHOLD
            Minimum absolute correlation required to classify a pair
            as strong.

        top_n : int, default=DEFAULT_TOP_CORRELATIONS_COUNT
            Number of top positive and negative correlations to keep.

        Returns
        -------
        EDAReportResult
            Aggregated exploratory data analysis report.
        """

        numeric_df = df.select_dtypes(include="number")

        categorical_df = df.select_dtypes(
            include=["object", "category", "bool"]
        )

        descriptive = self.descriptive_analysis.analyze(
            data=numeric_df,
            trim=trim
        )

        distribution = self.distribution_analysis.analyze(
            data=numeric_df,
            quantile_probs=quantile_probs,
            outlier_k=outlier_k,
            histogram_bins_count=histogram_bins_count
        )

        rolling = self.rolling_analysis.analyze(
            data=numeric_df,
            window=rolling_windows
        )

        categorical = self.categorical_analysis.analyze(
            data=categorical_df
        )

        correlation: Optional[CorrelationAnalysisReport]

        if numeric_df.shape[1] >= 2:
            correlation = self.correlation_analysis.analyze(
                df=numeric_df,
                method=correlation_method,
                strong_threshold=strong_threshold,
                top_n=top_n
            )
        else:
            correlation = None

        return EDAReportResult(
            descriptive=descriptive,
            distribution=distribution,
            rolling=rolling,
            categorical=categorical,
            correlation=correlation
        )
