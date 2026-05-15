"""
Rolling window analysis wrappers for time-series analytics.

The analysis supports:
- single rolling windows;
- multiple rolling windows;
- Series inputs;
- DataFrame inputs.
"""


from dataclasses import dataclass
from typing import Mapping, List, Union, overload, cast
import pandas as pd

from work.scripts.analytics.utils import resolve_series_name
from work.scripts.analytics.statistics import (
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


@dataclass(frozen=True)
class RollingSeriesReport:
    """
    Rolling statistical analysis report for a single Series.

    Attributes
    ----------
    name : str
        Resolved series name.

    window : int
        Rolling window size used for analysis.

    rolling_mean : pd.Series
        Rolling arithmetic mean.

    rolling_std : pd.Series
        Rolling standard deviation.

    rolling_min : pd.Series
        Rolling minimum values.

    rolling_max : pd.Series
        Rolling maximum values.

    rolling_zscore : pd.Series
        Rolling z-score normalization.

    rolling_volatility : pd.Series
        Rolling volatility estimate.

    rolling_momentum : pd.Series
        Rolling momentum values.

    rolling_rate_of_change : pd.Series
        Rolling rate of change values.

    rolling_variance : pd.Series
        Rolling variance values.

    rolling_cv : pd.Series
        Rolling coefficient of variation.
    """

    name: str
    window: int

    rolling_mean: pd.Series
    rolling_std: pd.Series
    rolling_min: pd.Series
    rolling_max: pd.Series
    rolling_zscore: pd.Series
    rolling_volatility: pd.Series
    rolling_momentum: pd.Series
    rolling_rate_of_change: pd.Series
    rolling_variance: pd.Series
    rolling_cv: pd.Series


class RollingAnalysis:
    """
    Build rolling-statistics reports for pandas Series and DataFrames.

    The class acts as a convenience wrapper around the reusable
    statistical helpers from ``work.scripts.analytics.statistics`` and
    returns structured report objects instead of raw Series values.
    """

    @overload
    def analyze(
        self,
        data: pd.Series,
        window: int
    ) -> RollingSeriesReport:
        """
        Analyze a Series using a single rolling window.

        Parameters
        ----------
        data : pd.Series
            Input series.

        window : int
            Rolling window size.

        Returns
        -------
        RollingSeriesReport
            Rolling analysis report for the specified window.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.Series,
        window: List[int]
    ) -> Mapping[int, RollingSeriesReport]:
        """
        Analyze a Series using multiple rolling windows.

        Parameters
        ----------
        data : pd.Series
            Input series.

        window : list[int]
            Collection of rolling window sizes.

        Returns
        -------
        Mapping[int, RollingSeriesReport]
            Mapping between window size and rolling analysis report.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        window: int
    ) -> Mapping[str, RollingSeriesReport]:
        """
        Analyze all DataFrame columns using a single rolling window.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame.

        window : int
            Rolling window size.

        Returns
        -------
        Mapping[str, RollingSeriesReport]
            Mapping between column names and rolling analysis reports.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        window: List[int]
    ) -> Mapping[str, Mapping[int, RollingSeriesReport]]:
        """
        Analyze all DataFrame columns using multiple rolling windows.

        Parameters
        ----------
        data : pd.DataFrame
            Input DataFrame.

        window : list[int]
            Collection of rolling window sizes.

        Returns
        -------
        Mapping[str, Mapping[int, RollingSeriesReport]]
            Nested mapping in format:
            ``column -> window -> report``.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame],
        window: Union[int, List[int]],
    ) -> Union[
        RollingSeriesReport,
        Mapping[int, RollingSeriesReport],
        Mapping[str, RollingSeriesReport],
        Mapping[str, Mapping[int, RollingSeriesReport]]
    ]:
        """
        Analyze rolling statistics for Series or DataFrame input.

        Parameters
        ----------
        data : pd.Series | pd.DataFrame
            Input time-series data.

        window : int | list[int]
            Single rolling window or collection of rolling windows.

        Returns
        -------
        RollingSeriesReport
            Returned when input is ``pd.Series`` and ``window`` is int.

        Mapping[int, RollingSeriesReport]
            Returned when input is ``pd.Series`` and ``window`` is a
            list of integers.

        Mapping[str, RollingSeriesReport]
            Returned when input is ``pd.DataFrame`` and ``window`` is
            int.

        Mapping[str, Mapping[int, RollingSeriesReport]]
            Returned when input is ``pd.DataFrame`` and ``window`` is
            a list of integers.

        Notes
        -----
        The concrete return type depends on both the runtime type of
        ``data`` and the type of ``window``.
        """

        if isinstance(data, pd.DataFrame):
            result = self._analyze_dataframe(df=data, window=window)
            if isinstance(window, int):
                result = cast(
                    typ=Mapping[str, RollingSeriesReport],
                    val=result
                )
                return result
            else:
                result = cast(
                    typ=Mapping[str, Mapping[int, RollingSeriesReport]],
                    val=result
                )
                return result

        return self._analyze_series(series=data, window=window)

    def _analyze_series(
        self,
        series: pd.Series,
        window: Union[int, List[int]],
    ) -> Union[
        RollingSeriesReport,
        Mapping[int, RollingSeriesReport]
    ]:
        """
        Analyze rolling statistics for a single Series.

        Parameters
        ----------
        series : pd.Series
            Input series.

        window : int | list[int]
            Single rolling window or collection of windows.

        Returns
        -------
        Union[RollingSeriesReport, Mapping[int, RollingSeriesReport]]
            Rolling analysis result.
        """

        if isinstance(window, list):
            return {
                w: self._build_report(series=series, window=w)
                for w in window
            }

        return self._build_report(series=series, window=window)

    def _analyze_dataframe(
        self,
        df: pd.DataFrame,
        window: Union[int, List[int]],
    ) -> Mapping[
        str,
        Union[
            RollingSeriesReport,
            Mapping[int, RollingSeriesReport]
        ]
    ]:
        """
        Analyze rolling statistics for all DataFrame columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.

        window : int | list[int]
            Single rolling window or collection of windows.

        Returns
        -------
        Mapping[
            str,
            Union[RollingSeriesReport, Mapping[int, RollingSeriesReport]]
        ]
            Mapping between column names and rolling analysis results.
        """

        return {
            col: self._analyze_series(
                series=df[col],
                window=window
            )
            for col in df.columns
        }

    def _build_report(
        self,
        series: pd.Series,
        window: int
    ) -> RollingSeriesReport:
        """
        Build rolling analysis report for a single window.

        Parameters
        ----------
        series : pd.Series
            Input series.

        window : int
            Rolling window size.

        Returns
        -------
        RollingSeriesReport
            Structured rolling statistics report.
        """

        return RollingSeriesReport(
            name=resolve_series_name(series=series),
            window=window,

            rolling_mean=rolling_mean(series=series, window=window),
            rolling_std=rolling_std(series=series, window=window),
            rolling_min=rolling_min(series=series, window=window),
            rolling_max=rolling_max(series=series, window=window),

            rolling_zscore=rolling_zscore(series=series, window=window),

            rolling_volatility=rolling_volatility(
                series=series,
                window=window
            ),
            rolling_momentum=rolling_momentum(series=series, window=window),
            rolling_rate_of_change=rolling_rate_of_change(
                series=series,
                window=window
            ),

            rolling_variance=rolling_variance(series=series, window=window),
            rolling_cv=rolling_cv(series=series, window=window),
        )
