"""Categorical feature generation — issue #13."""

from __future__ import annotations

import pandas as pd


def add_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of *df* with derived categorical columns appended."""
    df = df.copy()
    dt = df["trade_date"]

    df["decade"]      = (dt.dt.year // 10) * 10
    df["quarter"]     = dt.dt.quarter
    df["month"]       = dt.dt.month
    df["day_of_week"] = dt.dt.dayofweek          # 0 = Monday … 4 = Friday
    df["is_bullish"]  = df["close_price"] >= df["open_price"]
    df["trend_label"] = pd.cut(
        df["close_price"].pct_change() * 100,
        bins=[-float("inf"), -2, -0.5, 0.5, 2, float("inf")],
        labels=["strong_down", "down", "flat", "up", "strong_up"],
    )
    return df
