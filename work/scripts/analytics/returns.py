"""Daily and period returns calculations — issue #10."""

from __future__ import annotations

import numpy as np
import pandas as pd


def daily_returns(series: pd.Series) -> pd.Series:
    return series.pct_change()


def log_returns(series: pd.Series) -> pd.Series:
    return np.log(series / series.shift(1))


def cumulative_returns(series: pd.Series) -> pd.Series:
    return (1 + daily_returns(series)).cumprod() - 1


def yearly_return_table(df: pd.DataFrame) -> pd.DataFrame:
    """Year-end close price and YoY % change."""
    last = df.groupby("year")["close_price"].last()
    return pd.DataFrame({
        "year_end_close": last,
        "return_pct":     last.pct_change() * 100,
    })
