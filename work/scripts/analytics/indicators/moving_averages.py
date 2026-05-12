"""
Moving average indicator functions for financial time series.

This module provides implementations of common moving average
techniques used in technical analysis and feature engineering.
"""


import pandas as pd


def sma(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate simple moving average (SMA).

    The SMA is computed as the arithmetic mean of the previous
    ``window`` observations.

    Parameters
    ----------
    series : pd.Series
        Input price series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Simple moving average series.
    """

    return series.rolling(
        window=window,
        min_periods=window
    ).mean()


def ema(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate exponential moving average (EMA).

    The EMA applies exponentially decreasing weights to older
    observations, giving more importance to recent values.

    Parameters
    ----------
    series : pd.Series
        Input price series.

    window : int
        Exponential moving average span.

    Returns
    -------
    pd.Series
        Exponential moving average series.
    """

    return series.ewm(
        span=window,
        adjust=False
    ).mean()


def vwma(
    price_series: pd.Series,
    volume_series: pd.Series,
    window: int
) -> pd.Series:
    """
    Calculate volume weighted moving average (VWMA).

    The VWMA weights price values by trading volume, giving
    greater importance to periods with higher market activity.

    The formula is:

    SUM(price * volume) / SUM(volume)

    over the rolling window.

    Parameters
    ----------
    price_series : pd.Series
        Input price series.

    volume_series : pd.Series
        Trading volume series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Volume weighted moving average series.
    """

    weighted_price = price_series * volume_series

    rolling_weighted_sum = weighted_price.rolling(
        window=window,
        min_periods=window
    ).sum()

    rolling_volume_sum = volume_series.rolling(
        window=window,
        min_periods=window
    ).sum()

    return rolling_weighted_sum / rolling_volume_sum
