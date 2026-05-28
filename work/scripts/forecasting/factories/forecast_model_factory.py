"""
Forecast model factory implementation.

This module provides a centralized factory responsible for
instantiating forecasting models based on declarative configuration
objects.

It decouples model selection logic from business code and enables
extensible model registration in a single location.
"""


from work.scripts.contracts import ForecastModelName
from work.scripts.forecasting.models import (
    BaseForecast,
    NaiveForecast,
    MovingAverageForecast,
    ARIMAForecast,
    SARIMAXForecast,
)
from work.scripts.forecasting.contracts import ForecastModelConfig


class ForecastModelFactory:
    """
    Factory for creating time-series forecasting models.

    This factory maps configuration objects to concrete forecasting
    model implementations, providing a unified entry point for model
    instantiation.

    The design follows the Factory pattern to decouple model creation
    from usage logic.

    Methods
    -------
    create(config)
        Instantiate a forecasting model based on the provided config.
    """

    @staticmethod
    def create(config: ForecastModelConfig) -> BaseForecast:
        """
        Create a forecasting model instance from configuration.

        Parameters
        ----------
        config : ForecastModelConfig
            Configuration object describing:
            - model type
            - model-specific hyperparameters

        Returns
        -------
        BaseForecast
            Initialized forecasting model instance.

        Raises
        ------
        ValueError
            If the provided model type is not supported.

        Notes
        -----
        This method acts as a central registry for all forecasting models.
        Each model is initialized with its corresponding configuration
        parameters.
        """

        if config.model == ForecastModelName.NAIVE:
            return NaiveForecast()

        if config.model == ForecastModelName.MOVING_AVERAGE:
            return MovingAverageForecast(window=config.window)

        if config.model == ForecastModelName.ARIMA:
            return ARIMAForecast(order=config.order)

        if config.model == ForecastModelName.SARIMAX:
            return SARIMAXForecast(
                order=config.order,
                seasonal_order=config.seasonal_order
            )

        raise ValueError(f"Unsupported model: {config.model}")
