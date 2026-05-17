"""
High-level stationarity analysis based on Augmented Dickey-Fuller test.

This module wraps the low-level ADF test into a structured analysis layer
that produces human-readable and system-consumable reports.

It extends raw statistical output with:
- hypothesis interpretation;
- decision labeling (stationary / non-stationary);
- recommendation layer for downstream processing;
- batch processing over DataFrames.
"""


from dataclasses import dataclass
from typing import List, Mapping, Optional, Union, overload
import pandas as pd

from work.scripts.analytics.ts import (
    ADFTestConfig,
    ADFTestResult,
    adf_test,
)
from work.scripts.analytics.constants import (
    ADF_HYPOTHESIS_NON_STATIONARY,
    ADF_HYPOTHESIS_STATIONARY,
    ADF_RECOMMENDATION_NON_STATIONARY,
    ADF_RECOMMENDATION_STATIONARY,
)
from work.scripts.analytics.utils import resolve_series_name


@dataclass(frozen=True)
class StationarityReport:
    """
    Stationarity analysis result for a single time series.

    Attributes
    ----------
    name : str
        Name of analyzed series.

    result : ADFTestResult
        Raw ADF statistical output.

    hypothesis : str
        Human-readable hypothesis interpretation.

    passed : bool
        Whether the series is considered stationary.

    recommendation : str
        Suggested next step (e.g., differencing, transformation).
    """

    name: str
    result: ADFTestResult
    hypothesis: str
    passed: bool
    recommendation: str


@dataclass(frozen=True)
class StationarityAnalysisFailure:
    """
    Container for failed stationarity tests.

    Attributes
    ----------
    name : str
        Column name that failed analysis.

    error : str
        Error message explaining failure reason.
    """

    name: str
    error: str


@dataclass(frozen=True)
class DataFrameStationarityReport:
    """
    Batch stationarity analysis result for a DataFrame.

    Attributes
    ----------
    reports : Mapping[str, StationarityReport]
        Successful stationarity analysis results.

    failures : List[StationarityAnalysisFailure]
        Columns that could not be analyzed.
    """

    reports: Mapping[str, StationarityReport]
    failures: List[StationarityAnalysisFailure]


class StationarityAnalysis:
    """
    High-level stationarity analysis based on the Augmented Dickey-Fuller test.

    This class wraps the low-level ADF test into a structured analysis layer
    that produces human-readable and system-consumable reports.

    It extends raw statistical output with:
    - hypothesis interpretation;
    - decision labeling (stationary / non-stationary);
    - recommendation generation for downstream processing;
    - batch processing over DataFrames.
    """

    @overload
    def analyze(
        self,
        data: pd.Series,
        config: Optional[ADFTestConfig] = None
    ) -> StationarityReport:
        """
        Analyze a single time series for stationarity.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        config: Optional[ADFTestConfig] = None
    ) -> DataFrameStationarityReport:
        """
        Analyze all numeric columns of a DataFrame for stationarity.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame],
        config: Optional[ADFTestConfig] = None
    ) -> Union[
        StationarityReport,
        DataFrameStationarityReport
    ]:
        """
        Run stationarity analysis.

        Parameters
        ----------
        data : Union[pd.Series, pd.DataFrame]
            Input time series or dataset.

        config : Optional[ADFTestConfig]
            Configuration for ADF test.

        Returns
        -------
        Union[StationarityReport, DataFrameStationarityReport]
            Analysis result depending on input type.
        """

        if isinstance(data, pd.DataFrame):
            return self._analyze_dataframe(df=data, config=config)

        return self._analyze_series(series=data, config=config)

    def _analyze_series(
        self,
        series: pd.Series,
        config: Optional[ADFTestConfig]
    ) -> StationarityReport:
        """
        Run Augmented Dickey-Fuller (ADF) stationarity analysis
        on a single series.

        This method is a low-level wrapper around ``adf_test`` that:
        - executes the statistical test;
        - interprets the result into a human-readable hypothesis;
        - attaches a recommendation for further processing.

        Parameters
        ----------
        series : pd.Series
            Input time-series data to be tested for stationarity.

        config : Optional[ADFTestConfig]
            Configuration for the ADF test, including significance level,
            regression type, and lag selection strategy.

        Returns
        -------
        StationarityReport
            Structured report containing:
            - ADF test result (statistic, p-value, critical values);
            - stationarity decision (passed/failed);
            - statistical hypothesis interpretation;
            - recommendation for downstream processing.

        Notes
        -----
        The stationarity decision is defined as::

            is_stationary = (pvalue < alpha)

        where ``alpha`` is defined in ``ADFTestConfig``.

        """

        result = adf_test(
            series=series,
            config=config
        )

        stationary = result.is_stationary

        if stationary:
            hypothesis = ADF_HYPOTHESIS_STATIONARY
            recommendation = ADF_RECOMMENDATION_STATIONARY
        else:
            hypothesis = ADF_HYPOTHESIS_NON_STATIONARY
            recommendation = ADF_RECOMMENDATION_NON_STATIONARY

        return StationarityReport(
            name=resolve_series_name(series=series),
            result=result,
            hypothesis=hypothesis,
            passed=stationary,
            recommendation=recommendation,
        )

    def _analyze_dataframe(
        self,
        df: pd.DataFrame,
        config: Optional[ADFTestConfig]
    ) -> DataFrameStationarityReport:
        """
        Run ADF stationarity analysis across all numeric columns
        in a DataFrame.

        This method:
        - filters numeric columns only;
        - applies ADF test per column;
        - aggregates successful results and failures separately.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing multiple time-series columns.

        config : Optional[ADFTestConfig]
            Configuration for ADF test applied uniformly to all columns.

        Returns
        -------
        DataFrameStationarityReport
            Container with:
            - per-column stationarity reports;
            - list of failed analyses (non-numeric / invalid series).

        Notes
        -----
        Columns that cannot be evaluated (e.g. constant or invalid series)
        are not discarded silently — they are returned in ``failures`` with
        error descriptions for traceability.
        """

        numeric_df = df.select_dtypes(include="number")

        reports: dict[str, StationarityReport] = {}
        failures: list[StationarityAnalysisFailure] = []

        for column in numeric_df.columns:
            series = numeric_df[column]

            try:
                reports[column] = self._analyze_series(
                    series=series,
                    config=config
                )
            except ValueError as exc:
                failures.append(
                    StationarityAnalysisFailure(
                        name=column,
                        error=str(exc)
                    )
                )

        return DataFrameStationarityReport(
            reports=reports,
            failures=failures
        )
