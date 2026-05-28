"""
Time-series forecasting framework.

This package provides a complete forecasting pipeline including:
- model implementations;
- evaluation utilities;
- backtesting and forecasting report generation.

The design is modular and separates:
- model logic (forecasting algorithms);
- evaluation logic (metrics and splitting);
- orchestration layer (reports and pipelines).

Supported forecasting models:
- Naive forecast
- Moving average forecast
- ARIMA
- SARIMAX

Supported evaluation utilities:
- chronological train/test splitting
- standard regression metrics (MAE, MSE, RMSE, MAPE)

Supported reporting workflows:
- forecast generation reports
- backtesting reports
"""


from .models import (
    BaseForecast,
    NaiveForecast,
    MovingAverageForecast,
    ARIMAForecast,
    SARIMAXForecast,
)
from .evaluation import (
    chronological_split,
    TrainTestSplitResult,
    mae,
    mse,
    rmse,
    mape
)
from .reports import (
    ForecastReport,
    ForecastMetrics,
    BacktestReportResult,
    BacktestReport
)


__all__ = [
    "BaseForecast",
    "NaiveForecast",
    "MovingAverageForecast",
    "ARIMAForecast",
    "SARIMAXForecast",

    "chronological_split",
    "TrainTestSplitResult",
    "mae",
    "mse",
    "rmse",
    "mape",

    "ForecastReport",
    "ForecastMetrics",
    "BacktestReportResult",
    "BacktestReport"
]
