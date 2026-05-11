"""Moving average implementations — issue #11."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=1).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def smma(series: pd.Series, period: int) -> pd.Series:
    """Smoothed Moving Average (SMMA / RMA)."""
    result = series.copy() * np.nan
    if len(series) < period:
        return result
    result.iloc[period - 1] = series.iloc[:period].mean()
    for i in range(period, len(series)):
        result.iloc[i] = (result.iloc[i - 1] * (period - 1) + series.iloc[i]) / period
    return result


def add_moving_averages(
    df: pd.DataFrame,
    periods: tuple[int, ...] = (10, 20, 50),
) -> pd.DataFrame:
    """Append SMA, EMA, and SMMA columns for each period to *df*."""
    df = df.copy()
    for p in periods:
        df[f"sma_{p}"]  = sma(df["close_price"], p)
        df[f"ema_{p}"]  = ema(df["close_price"], p)
        df[f"smma_{p}"] = smma(df["close_price"], p)
    return df
