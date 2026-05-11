"""Additional technical indicators — issue #12."""

from __future__ import annotations

import pandas as pd

from .moving_averages import ema


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta    = series.diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=period - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, adjust=False).mean()
    rs       = avg_gain / avg_loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def bollinger_bands(
    series: pd.Series,
    period: int = 20,
    std: float = 2.0,
) -> pd.DataFrame:
    mid   = series.rolling(period, min_periods=1).mean()
    sigma = series.rolling(period, min_periods=1).std()
    return pd.DataFrame({
        "bb_mid":   mid,
        "bb_upper": mid + std * sigma,
        "bb_lower": mid - std * sigma,
    }, index=series.index)


def macd(
    series: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    line   = ema(series, fast) - ema(series, slow)
    sig    = line.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({
        "macd":        line,
        "macd_signal": sig,
        "macd_hist":   line - sig,
    }, index=series.index)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high, low, prev = df["high_price"], df["low_price"], df["close_price"].shift(1)
    tr = pd.concat([
        high - low,
        (high - prev).abs(),
        (low  - prev).abs(),
    ], axis=1).max(axis=1)
    return tr.ewm(com=period - 1, adjust=False).mean()


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Append RSI-14, ATR-14, Bollinger Bands-20, and MACD(12,26,9) columns."""
    df    = df.copy()
    close = df["close_price"]
    df["rsi_14"] = rsi(close)
    df["atr_14"] = atr(df)
    df = pd.concat([df, bollinger_bands(close)], axis=1)
    df = pd.concat([df, macd(close)],             axis=1)
    return df
