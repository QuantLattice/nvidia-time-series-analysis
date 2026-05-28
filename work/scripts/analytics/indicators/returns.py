"""
Return-based indicator functions for financial time series.

This module provides common return calculations used in analytics,
feature engineering, and forecasting workflows.
"""


import numpy as np
import pandas as pd


def daily_return(series: pd.Series) -> pd.Series:
    """
    Calculate simple daily return.

    The formula is:

    (P_t / P_{t-1}) - 1

    Parameters
    ----------
    series : pd.Series
        Price series.

    Returns
    -------
    pd.Series
        Daily return series.
    """

    return series.pct_change()


def log_return(series: pd.Series) -> pd.Series:
    """
    Calculate logarithmic return.

    The formula is:

    ln(P_t / P_{t-1})

    Parameters
    ----------
    series : pd.Series
        Price series.

    Returns
    -------
    pd.Series
        Log return series.
    """

    return pd.Series(
        data=np.log(series / series.shift(periods=1)),
        index=series.index,
        name=series.name
    )


def rolling_return(series: pd.Series, window: int) -> pd.Series:
    """
    Calculate rolling return over a fixed window.

    The formula is:

    (P_t / P_{t-N}) - 1

    Parameters
    ----------
    series : pd.Series
        Price series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling return series.
    """

    return series.pct_change(periods=window)


def cumulative_return(series: pd.Series) -> pd.Series:
    """
    Calculate cumulative return.

    The formula is:

    (P_t / P_0) - 1

    Parameters
    ----------
    series : pd.Series
        Price series.

    Returns
    -------
    pd.Series
        Cumulative return series.
    """

    return series / series.iloc[0] - 1
