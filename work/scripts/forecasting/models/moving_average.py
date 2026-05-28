"""
Moving average forecasting model.

This module implements a forecasting baseline that predicts future
values as the mean of the most recent observations over a fixed
rolling window.

The model is useful for:
- short-horizon smoothing-based forecasts;
- baseline comparison;
- low-complexity time-series forecasting.
"""


from typing import Optional
import pandas as pd

from work.scripts.forecasting.models import BaseForecast


class MovingAverageForecast(BaseForecast):
    """
    Moving average forecasting model.

    This model forecasts future values using the arithmetic mean of the
    last ``window`` valid observations from the training series.

    Attributes
    ----------
    window : int
        Rolling window size used to compute the forecast baseline.

    mean_value : Optional[float]
        Mean value computed during fitting.
    """

    def __init__(
        self,
        window: int
    ) -> None:
        """
        Initialize the moving average forecasting model.

        Parameters
        ----------
        window : int
            Number of recent observations used to compute the forecast mean.

        Raises
        ------
        ValueError
            If ``window`` is less than or equal to zero.
        """

        super().__init__()
        self.window = window

        if window <= 0:
            raise ValueError(
                "window must be greater than 0."
            )

        self.mean_value: Optional[float] = None

    def fit(
        self,
        series: pd.Series
    ) -> None:
        """
        Fit the moving average model on a time series.

        The model stores the mean of the last ``window`` valid observations
        and marks itself as fitted.

        Parameters
        ----------
        series : pd.Series
            Input training series.

        Raises
        ------
        ValueError
            If the series is empty or shorter than the configured window.
        """

        clean = series.dropna()

        if clean.empty:
            raise ValueError("Series is empty.")

        if len(clean) < self.window:
            raise ValueError(
                "Series length is smaller than moving average window."
            )

        self.mean_value = float(
            clean.iloc[-self.window:].mean()
        )
        self._is_fitted = True

    def predict(
        self,
        steps: int
    ) -> pd.Series:
        """
        Predict future values using the fitted moving average.

        Parameters
        ----------
        steps : int
            Number of forecast steps.

        Returns
        -------
        pd.Series
            Forecast series containing the fitted mean repeated ``steps``
            times.
        """

        self._validate_predict(steps=steps)

        return pd.Series(
            data=[self.mean_value] * steps,
        )
