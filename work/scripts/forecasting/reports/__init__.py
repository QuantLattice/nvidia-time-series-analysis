"""
High-level forecasting report assembly utilities.

This package provides composite report builders that combine model
training, forecasting, and evaluation into structured result objects.

Available report groups
-----------------------
Forecast reports
    Generate future-value forecasts for a fitted forecasting model.

Backtest reports
    Evaluate forecasting models on chronological train/test splits
    and compute standard error metrics.

These report builders are intended for:
- forecasting workflows;
- model benchmarking;
- backtesting pipelines;
- GUI and export layers.
"""


from .forecast_report import (
    ForecastReport,
    ForecastReportResult
)
from .backtest_report import (
    BacktestReport,
    ForecastMetrics,
    BacktestReportResult,
)


__all__ = [
    "ForecastReport",
    "ForecastReportResult",
    "BacktestReport",
    "ForecastMetrics",
    "BacktestReportResult",
]
