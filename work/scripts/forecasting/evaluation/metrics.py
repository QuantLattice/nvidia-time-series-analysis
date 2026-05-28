"""
Forecasting error metrics.

This module wraps standard regression metrics commonly used in
time-series forecasting evaluation.

All metrics operate on aligned actual vs predicted series and
return scalar error values.

Metrics included:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
"""


import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_percentage_error
)


def mae(actual: pd.Series, predicted: pd.Series) -> float:
    """
    Mean Absolute Error (MAE).

    Measures the average absolute difference between actual
    and predicted values.

    Parameters
    ----------
    actual : pd.Series
        Ground truth values.
    predicted : pd.Series
        Model predictions.

    Returns
    -------
    float
        MAE value.
    """

    return mean_absolute_error(actual, predicted)


def mse(actual: pd.Series, predicted: pd.Series) -> float:
    """
    Mean Squared Error (MSE).

    Measures the average squared difference between actual
    and predicted values, penalizing larger errors more heavily.

    Parameters
    ----------
    actual : pd.Series
        Ground truth values.
    predicted : pd.Series
        Model predictions.

    Returns
    -------
    float
        MSE value.
    """

    return mean_squared_error(actual, predicted)


def rmse(actual: pd.Series, predicted: pd.Series) -> float:
    """
    Root Mean Squared Error (RMSE).

    Square root of MSE, representing error in original units
    of the target variable.

    Parameters
    ----------
    actual : pd.Series
        Ground truth values.
    predicted : pd.Series
        Model predictions.

    Returns
    -------
    float
        RMSE value.
    """

    return root_mean_squared_error(actual, predicted)


def mape(actual: pd.Series, predicted: pd.Series) -> float:
    """
    Mean Absolute Percentage Error (MAPE).

    Measures prediction error as a percentage of actual values.

    Parameters
    ----------
    actual : pd.Series
        Ground truth values.
    predicted : pd.Series
        Model predictions.

    Returns
    -------
    float
        MAPE value (fractional, e.g. 0.1 = 10%).
    """

    return mean_absolute_percentage_error(actual, predicted)
