"""
Forecasting model implementations.

Available models
----------------
BaseForecast
    Abstract base class defining the forecasting API.

NaiveForecast
    Baseline model that repeats the last observed value.

MovingAverageForecast
    Forecasting model based on a fixed rolling mean.

ARIMAForecast
    ARIMA-based statistical forecasting model.

SARIMAXForecast
    Seasonal ARIMA forecasting model with advanced time-series structure.
"""


from .base import BaseForecast
from .naive import NaiveForecast
from .moving_average import MovingAverageForecast
from .arima import ARIMAForecast
from .sarimax import SARIMAXForecast


__all__ = [
    "BaseForecast",
    "NaiveForecast",
    "MovingAverageForecast",
    "ARIMAForecast",
    "SARIMAXForecast",
]
