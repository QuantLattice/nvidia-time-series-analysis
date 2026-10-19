"""
Relative Strength Index (RSI) indicator implementations.

This module provides RSI calculation functions using both
Simple Moving Average (SMA) and Wilder's exponential smoothing.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd
import numpy as np
from enum import StrEnum


class RSIMethod(StrEnum):
    """
    Method used for RSI smoothing.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    SMA : simple moving average smoothing
    WILDER : Wilder's exponential smoothing (classic RSI)
    """

    SMA = "sma"
    WILDER = "wilder"


def rsi(
    series: pd.Series,
    window: int,
    method: RSIMethod
) -> pd.Series:
    """
    Relative Strength Index (RSI) dispatcher.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

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

    rsi_values = 100 - (100 / (1 + rs))

    return rsi_values


def rsi_wilder(
    series: pd.Series,
    window: int
) -> pd.Series:
    """
    RSI using Wilder's smoothing method.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Notes
    -----
    Original RSI formulation by J. Welles Wilder. Uses recursive
    exponential smoothing instead of simple rolling mean.
    """

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    rsi_values = pd.Series(
        data=np.nan,
        index=series.index,
        dtype=float
    )

    avg_gain = gain.iloc[1:window + 1].mean()
    avg_loss = loss.iloc[1:window + 1].mean()

    if avg_loss == 0:
        rsi_values.iloc[window] = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi_values.iloc[window] = 100 - (100 / (1 + rs))

    for i in range(window + 1, len(series)):
        avg_gain = (
            (avg_gain * (window - 1) + gain.iloc[i]) / window
        )
        avg_loss = (
            (avg_loss * (window - 1) + loss.iloc[i]) / window
        )

        if avg_loss == 0:
            rsi_values.iloc[i] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi_values.iloc[i] = 100 - (100 / (1 + rs))

    return rsi_values
