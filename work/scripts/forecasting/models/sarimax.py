"""
SARIMAX forecasting model implementation.

This module provides a wrapper around statsmodels SARIMAX model,
supporting both non-seasonal and seasonal time-series forecasting.

The model extends ARIMA by incorporating:
- seasonal components;
- exogenous-like structure (though not used here explicitly);
- improved flexibility for complex seasonal patterns.

It is suitable for seasonal financial and temporal datasets.

Notes
-----
This is a lightweight wrapper over statsmodels.tsa.statespace.SARIMAX.
"""


from typing import Optional, Tuple, cast
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import (  # type: ignore
    SARIMAX,
    SARIMAXResults
)

from work.scripts.forecasting.models import BaseForecast


class SARIMAXForecast(BaseForecast):
    """
    Seasonal AutoRegressive Integrated Moving Average
    with eXogenous features (SARIMAX).

    This class provides a unified interface for fitting and forecasting
    seasonal time-series models using statsmodels SARIMAX implementation.

    Parameters
    ----------
    order : tuple of int (p, d, q)
        Non-seasonal ARIMA order.
    seasonal_order : tuple of int (P, D, Q, s)
        Seasonal component:
        - P: seasonal AR order
        - D: seasonal differencing
        - Q: seasonal MA order
        - s: seasonal period length

    Attributes
    ----------
    order : tuple of int
        Non-seasonal configuration.
    seasonal_order : tuple of int
        Seasonal configuration.
    model : SARIMAXResults or None
        Fitted model instance.
    """

    def __init__(
        self,
        order: Tuple[int, int, int],
        seasonal_order: Tuple[int, int, int, int]
    ) -> None:
        """
        Initialize SARIMAX forecasting model.

        Parameters
        ----------
        order : tuple of int (p, d, q)
            Non-seasonal ARIMA configuration.
        seasonal_order : tuple of int (P, D, Q, s)
            Seasonal component configuration:
            - P: seasonal autoregressive order
            - D: seasonal differencing order
            - Q: seasonal moving average order
            - s: length of seasonal cycle

        Notes
        -----
        The model is not fitted upon initialization.
        Call `fit()` before calling `predict()`.
        """

        super().__init__()

        self.order = order
        self.seasonal_order = seasonal_order

        self.model: Optional[SARIMAXResults] = None

    def fit(
        self,
        series: pd.Series
    ) -> None:
        """
        Fit the SARIMAX model to the input time-series.

        Parameters
        ----------
        series : pd.Series
            Input time-series data. Missing values are removed automatically.

        Raises
        ------
        ValueError
            If the series is empty after cleaning.

        Notes
        -----
        Stationarity and invertibility constraints are disabled
        for flexibility, allowing the model to handle a wider range
        of real-world series.
        """

        clean = series.dropna()

        if clean.empty:
            raise ValueError("Series is empty.")

        model = SARIMAX(
            endog=clean,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fit_result = model.fit(disp=False)  # type: ignore

        self.model = cast(
            SARIMAXResults,
            fit_result
        )

        self._is_fitted = True

    def predict(
        self,
        steps: int
    ) -> pd.Series:
        """
        Generate forecasts for future time steps.

        Parameters
        ----------
        steps : int
            Number of steps ahead to forecast.

        Returns
        -------
        pd.Series
            Forecasted values as a sequence.

        Raises
        ------
        RuntimeError
            If the model has not been fitted prior to prediction.
        ValueError
            If steps <= 0 (handled in base class).
        """

        self._validate_predict(steps=steps)

        if self.model is None:
            raise RuntimeError(
                "Model must be initialized before prediction."
            )

        forecast_raw = self.model.forecast(steps=steps)  # type: ignore
        forecast = cast(np.ndarray, forecast_raw)

        return pd.Series(
            data=forecast
        )
