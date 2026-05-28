"""
ARIMA forecasting model implementation.

This module provides a wrapper around statsmodels ARIMA implementation,
exposing a unified forecasting interface compatible with BaseForecast.

The model supports:
- autoregressive components (AR);
- integration (I) for differencing;
- moving average (MA) components.

It is intended for stationary or differenced time-series forecasting.

Notes
-----
This implementation is a thin wrapper over statsmodels.tsa.arima.model.ARIMA.
"""


from statsmodels.tsa.arima.model import (  # type: ignore
    ARIMA,
    ARIMAResults
)
import pandas as pd
from typing import Tuple, Optional, cast
import numpy as np

from work.scripts.forecasting.models import BaseForecast


class ARIMAForecast(BaseForecast):
    """
    Autoregressive Integrated Moving Average (ARIMA) forecasting model.

    This class wraps the statsmodels ARIMA implementation and provides
    a unified interface for fitting and forecasting time-series data.

    Parameters
    ----------
    order : tuple of int (p, d, q)
        ARIMA model order:
        - p: number of autoregressive terms
        - d: number of differencing operations
        - q: number of moving average terms

    Attributes
    ----------
    order : tuple of int
        Model configuration (p, d, q).
    model : ARIMAResults or None
        Fitted ARIMA model instance after training.
    """

    def __init__(
        self,
        order: Tuple[int, int, int]
    ) -> None:
        """
        Initialize ARIMA forecasting model.

        Parameters
        ----------
        order : tuple of int (p, d, q)
            Configuration of the ARIMA model:
            - p: number of autoregressive terms
            - d: degree of differencing
            - q: number of moving average terms

        Notes
        -----
        The model is not fitted upon initialization.
        Call `fit()` before using `predict()`.
        """

        super().__init__()
        self.order = order
        self.model: Optional[ARIMAResults] = None

    def fit(
        self,
        series: pd.Series
    ) -> None:
        """
        Fit the ARIMA model to the input time-series.

        Parameters
        ----------
        series : pd.Series
            Input time-series data. NaN values are automatically removed.

        Raises
        ------
        ValueError
            If the input series is empty after removing missing values.

        Notes
        -----
        The model is trained using statsmodels ARIMA implementation.
        After fitting, internal state is stored for forecasting.
        """

        clean = series.dropna()

        if clean.empty:
            raise ValueError("Series is empty.")

        model = ARIMA(
            endog=clean,
            order=self.order
        )

        fit_result = model.fit()  # type: ignore
        self.model = cast(typ=ARIMAResults, val=fit_result)

        self._is_fitted = True

    def predict(self, steps: int) -> pd.Series:
        """
        Generate forecasts for a given number of future steps.

        Parameters
        ----------
        steps : int
            Number of future time steps to forecast.

        Returns
        -------
        pd.Series
            Forecasted values.

        Raises
        ------
        RuntimeError
            If the model has not been fitted.
        ValueError
            If steps <= 0 (handled in base class validation).
        """

        self._validate_predict(steps=steps)

        if self.model is None:
            raise RuntimeError(
                "Model must be initialized before prediction."
            )

        forecast_raw = self.model.forecast(steps=steps)  # type: ignore
        forecast = cast(np.ndarray, forecast_raw)

        return pd.Series(
            data=np.asarray(forecast),
        )
