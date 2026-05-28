"""
Distribution-oriented exploratory analysis utilities.

The analysis includes:
- quantile estimation;
- interquartile range statistics;
- Tukey outlier detection;
- histogram summaries;
- empirical cumulative distribution functions.
"""


from dataclasses import dataclass
from typing import Mapping, List, Union, overload
import pandas as pd

from work.scripts.analytics.constants import (
    DEFAULT_OUTLIER_IQR_MULTIPLIER,
    DEFAULT_HISTOGRAM_BINS,
    DEFAULT_QUANTILE_PROBS
)
from work.scripts.analytics.utils import resolve_series_name
from work.scripts.analytics.statistics import (
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


@dataclass(frozen=True)
class DistributionAnalysisReport:
    """
    Distribution summary report for a single Series.

    Attributes
    ----------
    name : str
        Resolved series name.

    quantiles : Mapping[float, float]
        Mapping between quantile probabilities and corresponding
        estimated values.

    iqr : float
        Interquartile range.

    outlier_bounds : OutlierBounds
        Lower and upper Tukey outlier boundaries.

    outlier_count : int
        Number of detected outliers.

    outlier_ratio : float
        Share of observations classified as outliers.

    histogram : HistogramResult
        Histogram bin counts and edges.

    empirical_cdf : EmpiricalCDFResult
        Empirical cumulative distribution function values.
    """

    name: str

    quantiles: Mapping[float, float]

    iqr: float

    outlier_bounds: OutlierBounds
    outlier_count: int
    outlier_ratio: float

    histogram: HistogramResult

    empirical_cdf: EmpiricalCDFResult


class DistributionAnalysis:
    """
    Perform distribution-oriented exploratory analysis.

    This class wraps low-level statistical helpers into structured
    report objects for Series and DataFrame inputs.
    """

    @overload
    def analyze(
        self,
        data: pd.Series,
        quantile_probs: List[float],
        outlier_k: float = DEFAULT_OUTLIER_IQR_MULTIPLIER,
        histogram_bins_count: int = DEFAULT_HISTOGRAM_BINS
    ) -> DistributionAnalysisReport:
        """
        Analyze the distribution of a single pandas Series.

        This overload is selected when the input data is a
        ``pandas.Series``.

        Parameters
        ----------
        data : pd.Series
            Input series to analyze.

        quantile_probs : List[float], default=DEFAULT_QUANTILE_PROBS
            Quantile probabilities to estimate.

        outlier_k : float,
            default=DEFAULT_OUTLIER_IQR_MULTIPLIER
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int,
            default=DEFAULT_HISTOGRAM_BINS
            Number of histogram bins.

        Returns
        -------
        DistributionAnalysisReport
            Structured distribution analysis report for the input
            series.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        quantile_probs: List[float],
        outlier_k: float = DEFAULT_OUTLIER_IQR_MULTIPLIER,
        histogram_bins_count: int = DEFAULT_HISTOGRAM_BINS
    ) -> Mapping[str, DistributionAnalysisReport]:
        """
        Analyze distributions for all DataFrame columns.

        This overload is selected when the input data is a
        ``pandas.DataFrame``.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame whose columns will be analyzed
            independently.

        quantile_probs : List[float], default=DEFAULT_QUANTILE_PROBS
            Quantile probabilities to estimate.

        outlier_k : float,
            default=DEFAULT_OUTLIER_IQR_MULTIPLIER
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int,
            default=DEFAULT_HISTOGRAM_BINS
            Number of histogram bins.

        Returns
        -------
        Mapping[str, DistributionAnalysisReport]
            Mapping between DataFrame column names and distribution
            analysis reports.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame],
        quantile_probs: List[float] = DEFAULT_QUANTILE_PROBS,
        outlier_k: float = DEFAULT_OUTLIER_IQR_MULTIPLIER,
        histogram_bins_count: int = DEFAULT_HISTOGRAM_BINS
    ) -> Union[
        DistributionAnalysisReport,
        Mapping[str, DistributionAnalysisReport]
    ]:
        """
        Analyze the statistical distribution of input data.

        Parameters
        ----------
        data : Union[pd.Series, pd.DataFrame]
            Input data structure to analyze.

        quantile_probs : List[float], default=DEFAULT_QUANTILE_PROBS
            Quantile probabilities to estimate.

        outlier_k : float,
            default=DEFAULT_OUTLIER_IQR_MULTIPLIER
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int,
            default=DEFAULT_HISTOGRAM_BINS
            Number of histogram bins.

        Returns
        -------
        Union[
            DistributionAnalysisReport,
            Mapping[str, DistributionAnalysisReport]
        ]
            Distribution analysis report object for Series input, or
            a mapping of reports for DataFrame input.

        Notes
        -----
        The concrete return type depends on the runtime type of
        ``data``:

        - ``pd.Series`` ->
          ``DistributionAnalysisReport``
        - ``pd.DataFrame`` ->
          ``Mapping[str, DistributionAnalysisReport]``
        """

        if isinstance(data, pd.DataFrame):
            return self._analyze_dataframe(
                df=data,
                quantile_probs=quantile_probs,
                outlier_k=outlier_k,
                histogram_bins_count=histogram_bins_count
            )
        return self._analyze_series(
            series=data,
            quantile_probs=quantile_probs,
            outlier_k=outlier_k,
            histogram_bins_count=histogram_bins_count
        )

    def _analyze_series(
        self,
        series: pd.Series,
        quantile_probs: List[float],
        outlier_k: float,
        histogram_bins_count: int
    ) -> DistributionAnalysisReport:
        """
        Build a distribution analysis report for a single Series.

        Parameters
        ----------
        series : pd.Series
            Input series.

        quantile_probs : List[float]
            Quantile probabilities to estimate.

        outlier_k : float
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int
            Number of histogram bins.

        Returns
        -------
        DistributionAnalysisReport
            Structured distribution analysis report.
        """

        quantile_result = quantiles(
            series=series,
            probs=quantile_probs
        )

        iqr_result = iqr(series=series)

        bounds = outlier_bounds(
            series=series,
            k=outlier_k
        )

        outliers = outlier_mask(
            series=series,
            k=outlier_k
        )

        histogram = histogram_bins(
            series=series,
            bins=histogram_bins_count
        )

        cdf = empirical_cdf(series=series)

        return DistributionAnalysisReport(
            name=resolve_series_name(series=series),

            quantiles=quantile_result,

            iqr=iqr_result,

            outlier_bounds=bounds,
            outlier_count=int(outliers.sum()),
            outlier_ratio=float(outliers.mean()),

            histogram=histogram,

            empirical_cdf=cdf
        )

    def _analyze_dataframe(
        self,
        df: pd.DataFrame,
        quantile_probs: List[float],
        outlier_k: float,
        histogram_bins_count: int
    ) -> Mapping[str, DistributionAnalysisReport]:
        """
        Build distribution reports for all DataFrame columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.

        quantile_probs : List[float]
            Quantile probabilities to estimate.

        outlier_k : float
            Tukey IQR multiplier used for outlier detection.

        histogram_bins_count : int
            Number of histogram bins.

        Returns
        -------
        Mapping[str, DistributionAnalysisReport]
            Mapping between column names and distribution reports.
        """

        return {
            column: self._analyze_series(
                series=df[column],
                quantile_probs=quantile_probs,
                outlier_k=outlier_k,
                histogram_bins_count=histogram_bins_count
            )
            for column in df.columns
        }
