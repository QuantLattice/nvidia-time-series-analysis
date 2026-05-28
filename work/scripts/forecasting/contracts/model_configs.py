"""
Forecasting model configuration definitions.

This module defines immutable configuration objects for
various time-series forecasting models.

Each configuration represents a fully typed specification
of model hyperparameters used for training and inference.

Supported model families:
- Naive baseline models;
- Moving average models;
- ARIMA models;
- SARIMAX models.
"""


from dataclasses import dataclass
from typing import Literal, Union, TypeAlias
from work.scripts.contracts import ForecastModelName
from typing import Tuple


@dataclass(frozen=True)
class NaiveConfig:
    """
    Configuration for naive forecasting model.

    The naive model typically uses the last observed value
    as the forecast for all future time steps.

    Attributes
    ----------
    model : Literal[ForecastModelName.NAIVE]
        Identifier of the forecasting model type.
    """

    model: Literal[ForecastModelName.NAIVE] = ForecastModelName.NAIVE


@dataclass(frozen=True)
class MovingAverageConfig:
    """
    Configuration for moving average forecasting model.

    This model forecasts future values using the average
    of the last observed values over a fixed rolling window.

    Attributes
    ----------
    window : int
        Size of the rolling window used for averaging.

    model : Literal[ForecastModelName.MOVING_AVERAGE]
        Identifier of the forecasting model type.
    """

    window: int
    model: Literal[ForecastModelName.MOVING_AVERAGE] = \
        ForecastModelName.MOVING_AVERAGE


@dataclass(frozen=True)
class ARIMAConfig:
    """
    Configuration for ARIMA forecasting model.

    ARIMA is a classical statistical forecasting model that
    combines autoregression, differencing, and moving average
    components.

    Attributes
    ----------
    order : Tuple[int, int, int]
        (p, d, q) parameters defining ARIMA structure:
        - p: autoregressive order;
        - d: differencing order;
        - q: moving average order.

    model : Literal[ForecastModelName.ARIMA]
        Identifier of the forecasting model type.
    """

    order: Tuple[int, int, int]
    model: Literal[ForecastModelName.ARIMA] = ForecastModelName.ARIMA


@dataclass(frozen=True)
class SARIMAXConfig:
    """
    Configuration for SARIMAX forecasting model.

    SARIMAX extends ARIMA by incorporating seasonality and
    exogenous variables (not explicitly modeled here).

    Attributes
    ----------
    order : Tuple[int, int, int]
        Non-seasonal ARIMA order (p, d, q).

    seasonal_order : Tuple[int, int, int, int]
        Seasonal components (P, D, Q, s), where:
        - P: seasonal autoregressive order;
        - D: seasonal differencing;
        - Q: seasonal moving average order;
        - s: seasonal period.

    model : Literal[ForecastModelName.SARIMAX]
        Identifier of the forecasting model type.
    """

    order: Tuple[int, int, int]
    seasonal_order: Tuple[int, int, int, int]
    model: Literal[ForecastModelName.SARIMAX] = ForecastModelName.SARIMAX


ForecastModelConfig: TypeAlias = Union[
    NaiveConfig,
    MovingAverageConfig,
    ARIMAConfig,
    SARIMAXConfig,
]
"""
Union type representing all supported forecasting model configurations.

This alias is used throughout the forecasting pipeline to enforce
type-safe model specification and enable polymorphic handling
of different forecasting strategies.
"""
