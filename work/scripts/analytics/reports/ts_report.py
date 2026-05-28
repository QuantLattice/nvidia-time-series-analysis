"""
Composite time-series reporting utilities.

This module combines multiple time-series diagnostic analyses into
a single unified reporting interface.

The report layer aggregates:
- stationarity diagnostics (ADF test);
- autocorrelation analysis (ACF/PACF);
- per-series failure tracking.

The resulting report objects are designed for downstream use in:
- quantitative research pipelines;
- forecasting diagnostics;
- visualization systems;
- automated analytical reporting.
"""


from dataclasses import dataclass
from typing import (
    Optional,
    Mapping,
    List
)
import pandas as pd

from work.scripts.analytics.analysis import (
    StationarityReport,
    AutocorrelationReport,
    StationarityAnalysis,
    AutocorrelationAnalysis,
    DataFrameStationarityReport,
    DataFrameAutocorrelationReport
)
from work.scripts.analytics.ts import (
    ADFTestConfig,
    AutocorrelationConfig
)


@dataclass(frozen=True)
class TimeSeriesReport:
    """
    Combined analytical report for a single time series.

    This report aggregates multiple time-series diagnostics into
    a unified structure for convenient downstream consumption.

    Attributes
    ----------
    stationarity : Optional[StationarityReport]
        Stationarity analysis result produced by the ADF test.

    autocorrelation : Optional[AutocorrelationReport]
        Autocorrelation and partial autocorrelation diagnostics.
    """

    stationarity: Optional[StationarityReport]
    autocorrelation: Optional[AutocorrelationReport]


@dataclass(frozen=True)
class TimeSeriesReportFailure:
    """
    Failure container for time-series report generation.

    Stores diagnostic errors encountered during individual
    analytical stages for a specific series.

    Attributes
    ----------
    name : str
        Name of the analyzed series.

    stationarity_error : Optional[str], default=None
        Error raised during stationarity analysis.

    autocorrelation_error : Optional[str], default=None
        Error raised during autocorrelation analysis.
    """

    name: str
    stationarity_error: Optional[str] = None
    autocorrelation_error: Optional[str] = None


@dataclass(frozen=True)
class TSReportResult:
    """
    Aggregated result of multi-series time-series analysis.

    Attributes
    ----------
    reports : Mapping[str, TimeSeriesReport]
        Successfully generated reports indexed by series name.

    failures : List[TimeSeriesReportFailure]
        Collection of analysis failures encountered during
        report generation.
    """

    reports: Mapping[str, TimeSeriesReport]
    failures: List[TimeSeriesReportFailure]


class TSReport:
    """
    High-level time-series report generator.

    This class orchestrates multiple analytical subsystems and
    combines their outputs into a unified time-series report.

    Included diagnostics
    --------------------
    - stationarity testing via the Augmented Dickey-Fuller test;
    - autocorrelation analysis (ACF);
    - partial autocorrelation analysis (PACF);
    - structured failure collection.

    Notes
    -----
    Only numeric columns are included in the analysis pipeline.
    Non-numeric columns are ignored automatically.
    """

    def __init__(self) -> None:
        """
        Initialize time-series analysis components.
        """

        self.stationarity_analysis = StationarityAnalysis()
        self.autocorrelation_analysis = AutocorrelationAnalysis()

    def generate(
        self,
        df: pd.DataFrame,
        stationarity_config: Optional[ADFTestConfig] = None,
        autocorrelation_config: Optional[AutocorrelationConfig] = None
    ) -> TSReportResult:
        """
        Generate a comprehensive time-series diagnostics report.

        The method applies stationarity and autocorrelation analysis
        to all numeric columns in the provided DataFrame and combines
        the results into a unified report structure.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing one or more time-series columns.

        stationarity_config : Optional[ADFTestConfig], default=None
            Configuration for the Augmented Dickey-Fuller stationarity test.
            If ``None``, default configuration values are used.

        autocorrelation_config : Optional[AutocorrelationConfig], default=None
            Configuration for autocorrelation and partial autocorrelation
            analysis. If ``None``, default configuration values are used.

        Returns
        -------
        TSReportResult
            Structured report containing:
            - successfully generated analytical reports;
            - per-series diagnostic failures.

        Notes
        -----
        Only numeric columns are analyzed.

        If analysis of a specific series fails, the error is captured
        and stored in the resulting failure collection instead of
        interrupting the full report generation process.
        """

        numeric_df = df.select_dtypes(include="number")

        stationarity_report: DataFrameStationarityReport = (
            self.stationarity_analysis.analyze(
                data=numeric_df,
                config=stationarity_config
            )
        )

        autocorrelation_report: DataFrameAutocorrelationReport = (
            self.autocorrelation_analysis.analyze(
                data=numeric_df,
                config=autocorrelation_config
            )
        )

        combined_reports: Mapping[str, TimeSeriesReport] = {}
        combined_failures: Mapping[str, TimeSeriesReportFailure] = {}

        all_columns = set(stationarity_report.reports) | \
            set(autocorrelation_report.reports)

        for column in all_columns:
            combined_reports[column] = TimeSeriesReport(
                stationarity=stationarity_report.reports.get(column),
                autocorrelation=autocorrelation_report.reports.get(column),
            )

        for failure in stationarity_report.failures:
            combined_failures[failure.name] = TimeSeriesReportFailure(
                name=failure.name,
                stationarity_error=failure.error,
            )

        for failure in autocorrelation_report.failures:
            existing = combined_failures.get(failure.name)

            if existing is None:
                combined_failures[failure.name] = TimeSeriesReportFailure(
                    name=failure.name,
                    autocorrelation_error=failure.error,
                )
            else:
                combined_failures[failure.name] = TimeSeriesReportFailure(
                    name=failure.name,
                    stationarity_error=existing.stationarity_error,
                    autocorrelation_error=failure.error,
                )

        return TSReportResult(
            reports=combined_reports,
            failures=list(combined_failures.values()),
        )
