"""Exploratory data analysis statistics — issue #14."""

from __future__ import annotations

import pandas as pd

_OHLCV = ["open_price", "high_price", "low_price", "close_price", "volume"]


def describe_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    return df[_OHLCV].describe()


def yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("year")
    return pd.DataFrame({
        "avg_close":    g["close_price"].mean(),
        "min_close":    g["close_price"].min(),
        "max_close":    g["close_price"].max(),
        "total_volume": g["volume"].sum(),
        "trading_days": g["close_price"].count(),
    })


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df[_OHLCV].corr()


def print_eda_report(df: pd.DataFrame) -> None:
    print("=== OHLCV Descriptive Statistics ===")
    print(describe_ohlcv(df).to_string())
    print("\n=== Yearly Summary ===")
    print(yearly_summary(df).to_string())
    print("\n=== Correlation Matrix ===")
    print(correlation_matrix(df).to_string())
