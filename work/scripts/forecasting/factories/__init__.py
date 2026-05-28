"""
Forecast model factory utilities.

This module provides a unified factory interface for constructing
time-series forecasting models from configuration objects.

It abstracts model instantiation logic and ensures consistent
initialization of forecasting algorithms across the codebase.

Supported models include:
- Naive forecasting
- Moving average forecasting
- ARIMA models
- SARIMAX models
"""


from .forecast_model_factory import ForecastModelFactory


__all__ = [
    "ForecastModelFactory",
]
