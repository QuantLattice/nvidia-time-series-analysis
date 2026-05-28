"""
Technical indicators module for time-series analysis.

This module provides implementations of commonly used financial
technical indicators such as:

- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Volatility (rolling standard deviation of log returns)
- Momentum

All functions operate on pandas Series and return either:
- pd.Series (single-feature indicators)
- pd.DataFrame (multi-output indicators)

These indicators are designed for feature engineering pipelines
in quantitative analysis and machine learning workflows.
"""


import pandas as pd
import numpy as np
from enum import StrEnum

from work.scripts.contracts import AnalyticsFeatureNames as FN


class RSIMethod(StrEnum):
    """
    Method used for RSI smoothing.

    Attributes
    ----------
    SMA : simple moving average smoothing
    WILDER : Wilder's exponential smoothing (classic RSI)
    """

    SMA = "sma"
    WILDER = "wilder"


# =========================================================
# RSI
# =========================================================

def rsi(
    series: pd.Series,
    window: int,
    method: RSIMethod
) -> pd.Series:
    """
    Relative Strength Index (RSI) dispatcher.

    Parameters
    ----------
    series : pd.Series
        Input price series.

    window : int
        Lookback period for RSI calculation.

    method : RSIMethod
        Smoothing method (SMA or WILDER).

    Returns
    -------
    pd.Series
        RSI values in range [0, 100].
    """

    if method == RSIMethod.SMA:
        return rsi_sma(series=series, window=window)

    if method == RSIMethod.WILDER:
        return rsi_wilder(series=series, window=window)

    raise ValueError(f"Unknown RSI method: {method}")


def rsi_sma(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    RSI using Simple Moving Average smoothing.

    Notes
    -----
    Classical RSI formulation using mean gains/losses.
    """

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(
        window=window,
        min_periods=window
    ).mean()
    avg_loss = loss.rolling(
        window=window,
        min_periods=window
    ).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def rsi_wilder(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    RSI using Wilder's smoothing method.

    Notes
    -----
    This is the original RSI formulation proposed by J. Welles Wilder.
    It uses recursive exponential smoothing instead of simple rolling mean.
    """

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rsi = pd.Series(
        data=np.nan,
        index=series.index,
        dtype=float
    )

    avg_gain = gain.iloc[1:window + 1].mean()
    avg_loss = loss.iloc[1:window + 1].mean()

    if avg_loss == 0:
        rsi.iloc[window] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi.iloc[window] = 100 - (100 / (1 + rs))

    for i in range(window + 1, len(series)):
        avg_gain = (avg_gain * (window - 1) + gain.iloc[i]) / window
        avg_loss = (avg_loss * (window - 1) + loss.iloc[i]) / window

        if avg_loss == 0:
            rsi.iloc[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi.iloc[i] = 100 - (100 / (1 + rs))

    return rsi


# =========================================================
# MACD
# =========================================================

def macd(
    series: pd.Series,
    fast_window: int,
    slow_window: int,
    signal_window: int
) -> pd.DataFrame:
    """
    Moving Average Convergence Divergence (MACD).

    Parameters
    ----------
    series : pd.Series
        Input price series.

    fast_window : int
        Fast EMA window.

    slow_window : int
        Slow EMA window.

    signal_window : int
        Signal line EMA window.

    Returns
    -------
    pd.DataFrame
        DataFrame with MACD line, signal line, and histogram.
    """

    ema_fast = series.ewm(
        span=fast_window,
        adjust=False
    ).mean()
    ema_slow = series.ewm(
        span=slow_window,
        adjust=False
    ).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(
        span=signal_window,
        adjust=False
    ).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame(
        data={
            FN.MACD: macd_line,
            FN.MACD_SIGNAL: signal_line,
            FN.MACD_HISTOGRAM: histogram
        },
        index=series.index
    )


# =========================================================
# BOLLINGER BANDS
# =========================================================

def bollinger_bands(
    series: pd.Series,
    window: int,
    num_std: float
) -> pd.DataFrame:
    """
    Bollinger Bands indicator.

    Parameters
    ----------
    series : pd.Series
        Input price series.

    window : int
        Rolling window size.

    num_std : float, optional
        Number of standard deviations for band width.

    Returns
    -------
    pd.DataFrame
        DataFrame containing:
        - middle band (SMA)
        - upper band
        - lower band
        - bandwidth
        - %B (position inside bands)
    """

    middle_band = series.rolling(
        window=window,
        min_periods=window
    ).mean()
    rolling_std = series.rolling(
        window=window,
        min_periods=window
    ).std(ddof=0)

    upper_band = middle_band + num_std * rolling_std
    lower_band = middle_band - num_std * rolling_std

    bandwidth = (upper_band - lower_band) / middle_band
    percent_b = (series - lower_band) / (upper_band - lower_band)

    return pd.DataFrame(
        data={
            FN.BOLLINGER_MIDDLE_BASE: middle_band,
            FN.BOLLINGER_UPPER_BASE: upper_band,
            FN.BOLLINGER_LOWER_BASE: lower_band,
            FN.BOLLINGER_BANDWIDTH_BASE: bandwidth,
            FN.BOLLINGER_PERCENT_B_BASE: percent_b
        },
        index=series.index
    )


# =========================================================
# VOLATILITY
# =========================================================

def volatility(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Rolling volatility based on log returns.

    Parameters
    ----------
    series : pd.Series
        Price series.

    window : int
        Rolling window size.

    Returns
    -------
    pd.Series
        Volatility estimate (rolling std of log returns).
    """

    log_ret = pd.Series(
        data=np.log(series / series.shift(periods=1)),
        index=series.index,
        name=series.name
    )

    return log_ret.rolling(
        window=window,
        min_periods=window
    ).std(ddof=0)


# =========================================================
# MOMENTUM
# =========================================================

def momentum(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    Price momentum indicator.

    Parameters
    ----------
    series : pd.Series
        Input price series.

    window : int
        Lookback window.

    Returns
    -------
    pd.Series
        Momentum values (P_t - P_{t-window}).
    """

    return series - series.shift(periods=window)
