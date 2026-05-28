"""
Naive baseline forecasting model.

This module implements a simple baseline forecaster that repeats the
last observed value for all future time steps.

The model is useful for:
- baseline comparison;
- quick sanity checks;
- benchmarking more advanced forecasting methods.
"""


from typing import Optional
import pandas as pd

from work.scripts.forecasting.models import BaseForecast


class NaiveForecast(BaseForecast):
    """
    Naive forecasting model.

    This model uses the last observed non-missing value from the training
    series as the forecast for all future time steps.

    Attributes
    ----------
    last_value : Optional[float]
        Last observed value extracted during fitting.
    """

    def __init__(self) -> None:
        """
        Initialize the naive forecasting model.

        The model starts without a stored forecast value and becomes
        usable after fitting.
        """

        super().__init__()
        self.last_value: Optional[float] = None

    def fit(
        self,
        series: pd.Series
    ) -> None:
        """
        Fit the naive model on a time series.

        The fitting procedure stores the last valid observation from the
        series and marks the model as fitted.

        Parameters
        ----------
        series : pd.Series
            Input training series.

        Raises
        ------
        ValueError
            If the input series contains no valid observations.
        """

        clean = series.dropna()

        if clean.empty:
            raise ValueError("Series is empty.")

        self.last_value = float(clean.iloc[-1])
        self._is_fitted = True

    def predict(
        self,
        steps: int
    ) -> pd.Series:
        """
        Predict future values using the last observed value.

        Parameters
        ----------
        steps : int
            Number of forecast steps.

        Returns
        -------
        pd.Series
            Forecast series containing the same value repeated ``steps`` times.
        """

        self._validate_predict(steps=steps)

        return pd.Series(
            data=[self.last_value] * steps,
        )
