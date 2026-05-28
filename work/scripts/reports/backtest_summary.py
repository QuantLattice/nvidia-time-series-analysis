"""
Backtest summary report for the unified reporting layer.

Wraps ``BacktestReport`` from the forecasting subsystem and exposes
the result as a metrics DataFrame, an actual-vs-predicted DataFrame,
and a plain-text summary — consistent with the rest of
``work.scripts.reports``.
"""

from dataclasses import dataclass
import pandas as pd

from work.scripts.forecasting.reports.backtest_report import (
    BacktestReport,
    BacktestReportResult,
)
from work.scripts.forecasting.contracts import ForecastModelConfig
from work.scripts.forecasting.constants import DEFAULT_TEST_RATIO


@dataclass(frozen=True)
class BacktestSummaryResult:
    """
    Tabular and textual output of a backtest run.

    Attributes
    ----------
    metrics_table : pd.DataFrame
        One-row DataFrame with columns: mae, mse, rmse, mape.

    comparison_table : pd.DataFrame
        Two-column DataFrame (``actual``, ``predicted``) aligned on the
        test index.

    text_summary : str
        Human-readable summary of the backtest run.

    source : BacktestReportResult
        Original result from the forecasting subsystem.
    """

    metrics_table: pd.DataFrame
    comparison_table: pd.DataFrame
    text_summary: str
    source: BacktestReportResult


class BacktestSummary:
    """
    Generates a tabular and textual backtest summary.

    Wraps ``BacktestReport`` and converts its result into formats
    compatible with the reporting layer (DataFrames + plain text).
    """

    _SEP = "=" * 48

    def generate(
        self,
        series: pd.Series,
        config: ForecastModelConfig,
        test_ratio: float = DEFAULT_TEST_RATIO,
    ) -> BacktestSummaryResult:
        """
        Run the backtest and return a summary report.

        Parameters
        ----------
        series : pd.Series
            Historical input time series.

        config : ForecastModelConfig
            Model configuration (Naive, MovingAverage, ARIMA, SARIMAX).

        test_ratio : float
            Fraction of the series reserved for the test set.

        Returns
        -------
        BacktestSummaryResult
            Metrics table, comparison table, text summary, and raw result.
        """

        result = BacktestReport().generate(
            series=series,
            config=config,
            test_ratio=test_ratio,
        )

        metrics_table = self._build_metrics_table(result)
        comparison_table = self._build_comparison_table(result)
        text_summary = self._build_text(result)

        return BacktestSummaryResult(
            metrics_table=metrics_table,
            comparison_table=comparison_table,
            text_summary=text_summary,
            source=result,
        )

    # --------------------------------
    # PRIVATE
    # --------------------------------

    def _build_metrics_table(self, r: BacktestReportResult) -> pd.DataFrame:
        m = r.metrics
        return pd.DataFrame(
            [{
                "model":    r.model_config.model,
                "mae":      round(m.mae, 6),
                "mse":      round(m.mse, 6),
                "rmse":     round(m.rmse, 6),
                "mape":     round(m.mape, 6),
                "train_n":  r.train_size,
                "test_n":   r.test_size,
            }]
        ).set_index("model")

    def _build_comparison_table(self, r: BacktestReportResult) -> pd.DataFrame:
        return pd.DataFrame({
            "actual":    r.actual,
            "predicted": r.predictions,
        })

    def _build_text(self, r: BacktestReportResult) -> str:
        m = r.metrics
        model_name = r.model_config.model

        lines = [
            self._SEP,
            "  BACKTEST SUMMARY",
            self._SEP,
            f"Model:       {model_name}",
            f"Train size:  {r.train_size:,} observations",
            f"Test size:   {r.test_size:,} observations",
            "",
            self._SEP,
            "  ERROR METRICS",
            self._SEP,
            f"  MAE:   {m.mae:.6f}",
            f"  MSE:   {m.mse:.6f}",
            f"  RMSE:  {m.rmse:.6f}",
            f"  MAPE:  {m.mape:.6f}",
            "",
            self._SEP,
            "  ACTUAL vs PREDICTED (first 10 rows)",
            self._SEP,
        ]

        pairs = list(zip(r.actual.items(), r.predictions.items()))
        for (idx, actual), (_, pred) in pairs[:10]:
            lines.append(f"  {idx}   actual={actual:.4f}   pred={pred:.4f}   Δ={actual - pred:+.4f}")

        if len(pairs) > 10:
            lines.append(f"  ... ({len(pairs) - 10} more rows)")

        return "\n".join(lines)
