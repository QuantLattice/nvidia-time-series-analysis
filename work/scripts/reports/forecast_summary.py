"""
Forecast summary report for the unified reporting layer.

Wraps ``ForecastReport`` from the forecasting subsystem and
exposes the result as a tabular DataFrame and a plain-text summary,
consistent with the rest of ``work.scripts.reports``.
"""

from dataclasses import dataclass
import pandas as pd

from work.scripts.forecasting.reports.forecast_report import (
    ForecastReport,
    ForecastReportResult,
)
from work.scripts.forecasting.contracts import ForecastModelConfig
from work.scripts.forecasting.constants import DEFAULT_FORECAST_HORIZON


@dataclass(frozen=True)
class ForecastSummaryResult:
    """
    Tabular and textual output of a forecast run.

    Attributes
    ----------
    predictions_table : pd.DataFrame
        Single-column DataFrame (``predicted``) indexed by the forecast
        time index.

    text_summary : str
        Human-readable summary of the forecast run.

    source : ForecastReportResult
        Original result from the forecasting subsystem.
    """

    predictions_table: pd.DataFrame
    text_summary: str
    source: ForecastReportResult


class ForecastSummary:
    """
    Generates a tabular and textual forecast summary.

    Wraps ``ForecastReport`` and converts its result into formats
    compatible with the reporting layer (DataFrame + plain text).
    """

    _SEP = "=" * 48

    def generate(
        self,
        series: pd.Series,
        config: ForecastModelConfig,
        horizon: int = DEFAULT_FORECAST_HORIZON,
    ) -> ForecastSummaryResult:
        """
        Run the forecast and return a summary report.

        Parameters
        ----------
        series : pd.Series
            Historical input time series.

        config : ForecastModelConfig
            Model configuration (Naive, MovingAverage, ARIMA, SARIMAX).

        horizon : int
            Number of future steps to predict.

        Returns
        -------
        ForecastSummaryResult
            Predictions table, text summary, and raw source result.
        """

        result = ForecastReport().generate(
            series=series,
            config=config,
            horizon=horizon,
        )

        predictions_table = result.predictions.rename("predicted").to_frame()

        text_summary = self._build_text(result)

        return ForecastSummaryResult(
            predictions_table=predictions_table,
            text_summary=text_summary,
            source=result,
        )

    # --------------------------------
    # PRIVATE
    # --------------------------------

    def _build_text(self, r: ForecastReportResult) -> str:
        model_name = r.model_config.model

        lines = [
            self._SEP,
            "  FORECAST SUMMARY",
            self._SEP,
            f"Model:            {model_name}",
            f"History size:     {r.history_size:,} observations",
            f"Forecast horizon: {r.forecast_horizon} steps",
            "",
            self._SEP,
            "  PREDICTIONS",
            self._SEP,
        ]

        for idx, val in r.predictions.items():
            lines.append(f"  {idx}    {val:.4f}")

        lines += [
            "",
            f"Min:  {r.predictions.min():.4f}",
            f"Max:  {r.predictions.max():.4f}",
            f"Mean: {r.predictions.mean():.4f}",
        ]

        return "\n".join(lines)
