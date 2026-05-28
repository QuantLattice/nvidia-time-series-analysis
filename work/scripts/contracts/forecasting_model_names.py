"""
Forecasting model registry.

This module defines a standardized enumeration of supported
forecasting model identifiers used across the system.

These identifiers are used in:
- configuration objects;
- model selection pipelines;
- serialization and logging systems.
"""


from enum import StrEnum


class ForecastModelName(StrEnum):
    """
    Enumeration of supported forecasting model types.

    Each value corresponds to a specific forecasting strategy
    implemented in the system.

    Members
    -------
    NAIVE : str
        Naive baseline model using last observed value.

    MOVING_AVERAGE : str
        Moving average forecasting model.

    ARIMA : str
        Classical ARIMA model for time-series forecasting.

    SARIMAX : str
        Seasonal ARIMA model with exogenous components.
    """

    NAIVE = "naive"
    MOVING_AVERAGE = "moving_average"
    ARIMA = "arima"
    SARIMAX = "sarimax"
