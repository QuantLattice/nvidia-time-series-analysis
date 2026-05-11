"""Tabular NVIDIA weekly OHLCV and moving averages output — no PNG.

Run:
    python3 -m work.output.candle_tables
"""

from __future__ import annotations

import pandas as pd

from work.scripts.analytics.moving_averages import sma, smma


def _load() -> pd.DataFrame:
    from work.scripts.db.session import Database
    from work.scripts.services.stock_quote_service import StockQuoteService

    df = StockQuoteService(Database()).get_all_quotes_df()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    current_year = pd.Timestamp.now().year
    df = df[df["trade_date"].dt.year.between(1990, current_year)].copy()
    df = df.sort_values("trade_date").reset_index(drop=True)
    df["year"] = df["trade_date"].dt.year
    return df


def weekly_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.set_index("trade_date")
        .resample("W")
        .agg(
            open_price  = ("open_price",  "first"),
            high_price  = ("high_price",  "max"),
            low_price   = ("low_price",   "min"),
            close_price = ("close_price", "last"),
            volume      = ("volume",      "sum"),
        )
        .dropna()
        .reset_index()
    )


def ma_table(df: pd.DataFrame, year: int) -> pd.DataFrame:
    yr    = df[df["year"] == year].reset_index(drop=True)
    close = yr["close_price"]
    return pd.DataFrame({
        "date":    yr["trade_date"],
        "close":   close,
        "sma_10":  sma(close, 10),
        "sma_20":  sma(close, 20),
        "sma_50":  sma(close, 50),
        "smma_10": smma(close, 10),
        "smma_20": smma(close, 20),
        "smma_50": smma(close, 50),
    })


def main() -> None:
    df     = _load()
    weekly = weekly_ohlcv(df)
    years  = sorted(df["year"].unique())
    print(f"[INFO] {len(df)} daily rows | {len(weekly)} weekly candles "
          f"| {years[0]}–{years[-1]}\n")

    print("=== Weekly OHLCV (last 10 rows) ===")
    print(weekly.tail(10).to_string(index=False))
    print()

    latest = years[-1]
    print(f"=== Moving Averages (SMA / SMMA) — {latest} ===")
    print(ma_table(df, latest).to_string(index=False, float_format="%.2f"))


if __name__ == "__main__":
    main()
