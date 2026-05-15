"""
Rolling statistical utilities for exploratory data analysis.

This module provides reusable rolling-window statistics for pandas
Series, including rolling moments, local dispersion, momentum,
rate-of-change metrics, and coefficient-style stability measures.

The functions are designed for EDA, feature engineering, and
time-series diagnostics.
"""


import pandas as pd


# ==========================================
# ROLLING CENTRAL TENDENCY / DISPERSION
# ==========================================

def rolling_mean(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling mean.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling mean series.
    """

    return series.rolling(window=window, min_periods=window).mean()


def rolling_std(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling standard deviation.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling standard deviation series.
    """

    return series.rolling(window=window, min_periods=window).std()


def rolling_min(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling minimum.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling minimum series.
    """

    return series.rolling(window=window, min_periods=window).min()


def rolling_max(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling maximum.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling maximum series.
    """

    return series.rolling(window=window, min_periods=window).max()


def rolling_variance(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling variance.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling variance series.
    """

    return series.rolling(window=window, min_periods=window).var()


# ==========================================
# ROLLING DIAGNOSTICS
# ==========================================

def rolling_zscore(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling z-score.

    The z-score is computed as:

    .. math:: (x_t - \\mu_t) / \\sigma_t

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling z-score series.
    """

    mean = series.rolling(window=window, min_periods=window).mean()
    std = series.rolling(window=window, min_periods=window).std()

    return (series - mean) / std


def rolling_volatility(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling volatility.

    In this project, volatility is represented by the rolling
    standard deviation of the input series.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling volatility series.
    """

    return series.rolling(window=window, min_periods=window).std()


def rolling_momentum(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling momentum.

    Momentum is defined as the difference between the current value
    and the value ``window`` periods ago.

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Lookback window.

    Returns
    -------
    pd.Series
        Rolling momentum series.
    """

    return series - series.shift(window)


def rolling_rate_of_change(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling rate of change.

    The formula is:

    .. math:: (x_t / x_{t-N}) - 1

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Lookback window.

    Returns
    -------
    pd.Series
        Rolling rate of change series.
    """

    return (series / series.shift(periods=window)) - 1


def rolling_cv(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate rolling coefficient of variation.

    The coefficient of variation is computed as:

    .. math:: \\sigma_t / \\mu_t

    Parameters
    ----------
    series : pd.Series
        Input data series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Rolling coefficient of variation series.
    """

    mean = series.rolling(window=window, min_periods=window).mean()
    std = series.rolling(window=window, min_periods=window).std()

    return std / mean
