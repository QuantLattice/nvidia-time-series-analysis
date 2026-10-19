"""
Technical indicators module for time-series analysis.

This module provides implementations of commonly used financial
technical indicators such as:

- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Volatility (rolling standard deviation of log returns)
- Momentum

RSI indicators are provided in the rsi submodule.

All functions operate on pandas Series and return either:
- pd.Series (single-feature indicators)
- pd.DataFrame (multi-output indicators)

These indicators are designed for feature engineering pipelines
in quantitative analysis and machine learning workflows.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd
import numpy as np

from work.scripts.contracts import AnalyticsFeatureNames as FN
from work.scripts.analytics.indicators.rsi import (
    RSIMethod,
    rsi,
    rsi_sma,
    rsi_wilder
)

__all__ = [
    'RSIMethod',
    'rsi',
    'rsi_sma',
    'rsi_wilder',
    'macd',
    'bollinger_bands',
    'volatility',
    'momentum'
]


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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    series : pd.Series
        Input price series.
    window : int
        Rolling window size.
    num_std : float
        Number of standard deviations for band width.

    Returns
    -------
    pd.DataFrame
        DataFrame containing middle band, upper band, lower band,
        bandwidth, and %B (position inside bands).
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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
