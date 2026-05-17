"""
High-level autocorrelation analysis for time-series diagnostics.

This module combines autocorrelation and partial autocorrelation
statistics into structured reports suitable for exploratory analysis,
model identification, and time-series diagnostics.

The analysis layer provides:
- autocorrelation and partial autocorrelation computation;
- strongest lag detection;
- statistically significant lag screening;
- batch analysis for DataFrame inputs with failure isolation.

The resulting reports are intended for:
- EDA workflows;
- autoregressive model selection;
- forecasting preparation;
- report generation and visualization.
"""


from dataclasses import dataclass
import pandas as pd
from typing import Mapping, List, overload, Optional, Union

from work.scripts.analytics.ts import (
    AutocorrelationConfig,
    AutocorrelationResult,
    PartialAutocorrelationResult,
    autocorrelation_series,
    partial_autocorrelation_series,
    strongest_autocorrelation_lag,
    strongest_partial_autocorrelation_lag,
    significant_autocorrelation_lags,
    significant_partial_autocorrelation_lags
)
from work.scripts.analytics.utils import resolve_series_name


@dataclass(frozen=True)
class AutocorrelationReport:
    """
    Container with autocorrelation analysis results for a single series.

    Attributes
    ----------
    name : str
        Resolved series name.

    acf : AutocorrelationResult
        Autocorrelation coefficients and confidence intervals.

    pacf : PartialAutocorrelationResult
        Partial autocorrelation coefficients and confidence intervals.

    strongest_acf_lag : int
        Lag with the largest absolute autocorrelation value.

    strongest_pacf_lag : int
        Lag with the largest absolute partial autocorrelation value.

    significant_acf_lags : pd.Series
        Boolean mask identifying significant autocorrelation lags.

    significant_pacf_lags : pd.Series
        Boolean mask identifying significant partial autocorrelation lags.
    """

    name: str
    acf: AutocorrelationResult
    pacf: PartialAutocorrelationResult
    strongest_acf_lag: int
    strongest_pacf_lag: int
    significant_acf_lags: pd.Series
    significant_pacf_lags: pd.Series


@dataclass(frozen=True)
class AutocorrelationAnalysisFailure:
    """
    Container describing a failed autocorrelation analysis.

    Attributes
    ----------
    name : str
        Name of the column that failed analysis.

    error : str
        Error message explaining the failure reason.
    """

    name: str
    error: str


@dataclass(frozen=True)
class DataFrameAutocorrelationReport:
    """
    Batch autocorrelation analysis result for a DataFrame.

    Attributes
    ----------
    reports : Mapping[str, AutocorrelationReport]
        Successful analysis results indexed by column name.

    failures : List[AutocorrelationAnalysisFailure]
        Columns that could not be analyzed successfully.
    """

    reports: Mapping[str, AutocorrelationReport]
    failures: List[AutocorrelationAnalysisFailure]


class AutocorrelationAnalysis:
    """
    High-level autocorrelation analysis pipeline.

    This class combines autocorrelation and partial autocorrelation
    statistics into a single report-oriented interface.

    The analysis workflow includes:
    - ACF computation;
    - PACF computation;
    - strongest lag detection;
    - significant lag identification;
    - batch processing of numeric DataFrame columns.
    """

    @overload
    def analyze(
        self,
        data: pd.Series,
        config: Optional[AutocorrelationConfig] = None
    ) -> AutocorrelationReport:
        """
        Analyze autocorrelation structure for a single time series.
        """
        ...

    @overload
    def analyze(
        self,
        data: pd.DataFrame,
        config: Optional[AutocorrelationConfig] = None
    ) -> DataFrameAutocorrelationReport:
        """
        Analyze autocorrelation structure for all numeric columns
        of a DataFrame.
        """
        ...

    def analyze(
        self,
        data: Union[pd.Series, pd.DataFrame],
        config: Optional[AutocorrelationConfig] = None
    ) -> Union[AutocorrelationReport, DataFrameAutocorrelationReport]:
        """
        Analyze a Series or DataFrame using autocorrelation diagnostics.

        Parameters
        ----------
        data : pd.Series | pd.DataFrame
            Input time-series data.

        config : Optional[AutocorrelationConfig], optional
            Configuration controlling lag computation and confidence
            interval estimation.

        Returns
        -------
        AutocorrelationReport | DataFrameAutocorrelationReport
            Analysis result for Series input, or batch result for
            DataFrame input.

        Notes
        -----
        The concrete return type depends on the runtime type of `data`:
        - ``pd.Series`` -> ``AutocorrelationReport``
        - ``pd.DataFrame`` -> ``DataFrameAutocorrelationReport``
        """

        if isinstance(data, pd.DataFrame):
            return self._analyze_dataframe(df=data, config=config)

        return self._analyze_series(series=data, config=config)

    def _analyze_series(
        self,
        series: pd.Series,
        config: Optional[AutocorrelationConfig]
    ) -> AutocorrelationReport:
        """
        Build an autocorrelation report for a single Series.

        Parameters
        ----------
        series : pd.Series
            Input series.

        config : Optional[AutocorrelationConfig]
            Autocorrelation configuration.

        Returns
        -------
        AutocorrelationReport
            Structured autocorrelation report.
        """

        acf_result = autocorrelation_series(
            series=series,
            config=config,
        )

        pacf_result = partial_autocorrelation_series(
            series=series,
            config=config,
        )

        return AutocorrelationReport(
            name=resolve_series_name(series=series),
            acf=acf_result,
            pacf=pacf_result,
            strongest_acf_lag=strongest_autocorrelation_lag(acf_result),
            strongest_pacf_lag=strongest_partial_autocorrelation_lag(
                pacf_result
            ),
            significant_acf_lags=significant_autocorrelation_lags(acf_result),
            significant_pacf_lags=significant_partial_autocorrelation_lags(
                pacf_result
            ),
        )

    def _analyze_dataframe(
        self,
        df: pd.DataFrame,
        config: Optional[AutocorrelationConfig]
    ) -> DataFrameAutocorrelationReport:
        """
        Build autocorrelation reports for all numeric DataFrame columns.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame.

        config : Optional[AutocorrelationConfig]
            Autocorrelation configuration.

        Returns
        -------
        DataFrameAutocorrelationReport
            Batch autocorrelation analysis result with per-column reports
            and collected failures.
        """

        numeric_df = df.select_dtypes(include="number")

        reports: Mapping[str, AutocorrelationReport] = {}
        failures: List[AutocorrelationAnalysisFailure] = []

        for column in numeric_df.columns:
            series = numeric_df[column]

            try:
                reports[column] = self._analyze_series(
                    series=series,
                    config=config,
                )
            except ValueError as exc:
                failures.append(
                    AutocorrelationAnalysisFailure(
                        name=column,
                        error=str(exc),
                    )
                )

        return DataFrameAutocorrelationReport(
            reports=reports,
            failures=failures,
        )
