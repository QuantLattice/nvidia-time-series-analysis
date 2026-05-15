"""
Descriptive analysis wrappers for exploratory data analysis.

The analysis supports both a single pandas Series and a DataFrame
containing multiple series.
"""


from dataclasses import dataclass
from typing import Mapping, Union, overload
import pandas as pd


from work.scripts.analytics.constants import DEFAULT_TRIM_RATIO
from work.scripts.analytics.utils import resolve_series_name
from work.scripts.analytics.statistics import (
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


@dataclass(frozen=True)
class SeriesDescriptiveReport:
    """
    Descriptive summary for a single pandas Series.

    Attributes
    ----------
    name : str
        Resolved series name.

    mean : float
        Arithmetic mean.

    median : float
        Median value.

    variance : float
        Sample variance.

    std : float
        Sample standard deviation.

    data_range : float
        Difference between maximum and minimum values.

    min : float
        Minimum value.

    max : float
        Maximum value.

    skewness : float
        Sample skewness.

    kurtosis : float
        Sample kurtosis.

    missing_count : int
        Number of missing observations.

    missing_ratio : float
        Share of missing observations.

    positive_ratio : float
        Share of values greater than zero.

    negative_ratio : float
        Share of values less than zero.

    zero_ratio : float
        Share of values equal to zero.

    trimmed_mean : float
        Mean after trimming the distribution tails.

    mad : float
        Median absolute deviation.

    coefficient_of_variation : float
        Ratio of standard deviation to mean.
    """

    name: str

    mean: float
    median: float

    variance: float
    std: float

    data_range: float
    min: float
    max: float

    skewness: float
    kurtosis: float

    missing_count: int
    missing_ratio: float

    positive_ratio: float
    negative_ratio: float
    zero_ratio: float

    trimmed_mean: float
    mad: float

    coefficient_of_variation: float


class DescriptiveAnalysis:
    """
    Build descriptive reports for pandas Series and DataFrames.

    The class acts as a convenient wrapper around the statistical
    helper functions from the analytics.statistics package and
    returns structured report objects instead of raw scalar values.
    """

    @overload
    def analyze(
        self,
        data: pd.Series,
        trim: float = DEFAULT_TRIM_RATIO
    ) -> SeriesDescriptiveReport:
        """
        Analyze a single pandas Series.

        This overload is selected when the input data is a
        ``pandas.Series``.

        Parameters
        ----------
        data : pd.Series
            Input series to analyze.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        Returns
        -------
        SeriesDescriptiveReport
            Structured descriptive statistics report for the input
            series.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        trim: float = DEFAULT_TRIM_RATIO
    ) -> Mapping[str, SeriesDescriptiveReport]:
        """
        Analyze all columns in a pandas DataFrame.

        This overload is selected when the input data is a
        ``pandas.DataFrame``.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame whose columns will be analyzed
            independently.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        Returns
        -------
        Mapping[str, SeriesDescriptiveReport]
            Mapping between DataFrame column names and descriptive
            analysis reports.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame],
        trim: float = DEFAULT_TRIM_RATIO
    ) -> Union[
        SeriesDescriptiveReport,
        Mapping[str, SeriesDescriptiveReport]
    ]:
        """
        Analyze a Series or DataFrame using descriptive statistics.

        Parameters
        ----------
        data : Union[pd.Series, pd.DataFrame]
            Input data structure to analyze.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        Returns
        -------
        Union[
            SeriesDescriptiveReport,
            Mapping[str, SeriesDescriptiveReport]
        ]
            Descriptive analysis report object for Series input, or a
            mapping of reports for DataFrame input.

        Notes
        -----
        The concrete return type depends on the runtime type of
        ``data``:

        - ``pd.Series`` ->
          ``SeriesDescriptiveReport``
        - ``pd.DataFrame`` ->
          ``Mapping[str, SeriesDescriptiveReport]``
        """

        if isinstance(data, pd.DataFrame):
            return self._analyze_dataframe(
                df=data,
                trim=trim
            )

        return self._analyze_series(
            series=data,
            trim=trim
        )

    def _analyze_series(
        self,
        series: pd.Series,
        trim: float = DEFAULT_TRIM_RATIO
    ) -> SeriesDescriptiveReport:
        """
        Build a descriptive report for a single Series.

        Parameters
        ----------
        series : pd.Series
            Input series.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        Returns
        -------
        SeriesDescriptiveReport
            Structured descriptive statistics report.
        """

        return SeriesDescriptiveReport(
            name=resolve_series_name(series=series),

            mean=mean(series=series),
            median=median(series=series),

            variance=variance(series=series),
            std=std(series=series),

            data_range=data_range(series=series),
            min=min_value(series=series),
            max=max_value(series=series),

            skewness=skewness(series=series),
            kurtosis=kurtosis(series=series),

            missing_count=missing_count(series=series),
            missing_ratio=missing_ratio(series=series),

            positive_ratio=positive_ratio(series=series),
            negative_ratio=negative_ratio(series=series),
            zero_ratio=zero_ratio(series=series),

            trimmed_mean=trimmed_mean(series=series, trim=trim),
            mad=mad(series=series),

            coefficient_of_variation=coefficient_of_variation(series=series),
        )

    def _analyze_dataframe(
        self,
        df: pd.DataFrame,
        trim: float = DEFAULT_TRIM_RATIO
    ) -> Mapping[str, SeriesDescriptiveReport]:
        """
        Build descriptive reports for all columns in a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.

        trim : float, default=DEFAULT_TRIM_RATIO
            Tail trimming ratio used for trimmed mean calculation.

        Returns
        -------
        Mapping[str, SeriesDescriptiveReport]
            Mapping from column names to descriptive reports.
        """

        return {
            col: self._analyze_series(
                series=df[col],
                trim=trim
            )
            for col in df.columns
        }
