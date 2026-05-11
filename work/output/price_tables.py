"""Tabular NVIDIA price, volume, and growth output — no PNG.

Run:
    python3 -m work.output.price_tables
"""

from __future__ import annotations

import pandas as pd


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


def avg_price_table(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("year")["close_price"].mean().rename("avg_close_usd").to_frame()


def volume_table(df: pd.DataFrame) -> pd.DataFrame:
    return (df.groupby("year")["volume"].sum() / 1e9).rename("total_volume_bn").to_frame()


def growth_table(df: pd.DataFrame) -> pd.DataFrame:
    pct = df.groupby("year")["close_price"].last().pct_change() * 100
    return pct.rename("yoy_growth_pct").to_frame()


def main() -> None:
    df = _load()
    print(f"[INFO] {len(df)} rows | "
          f"{df['trade_date'].min().date()} – {df['trade_date'].max().date()}\n")

    print("=== Average Close Price by Year (USD) ===")
    print(avg_price_table(df).to_string(float_format="%.2f"))
    print()

    print("=== Total Trading Volume by Year (billions) ===")
    print(volume_table(df).to_string(float_format="%.1f"))
    print()

    print("=== Year-over-Year Price Growth (%) ===")
    print(growth_table(df).to_string(float_format="%+.1f"))


if __name__ == "__main__":
    main()
