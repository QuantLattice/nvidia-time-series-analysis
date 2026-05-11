"""NVIDIA charts — dark & light themes, per-year folders.

Output structure in work/graphics/analysis/:

    dark/
        years/
            <year>/  nvda_candles_<year>.png  nvda_sma_<year>.png  nvda_sme_<year>.png
            ...
    light/
        years/
            <year>/  ...

SME = Smoothed Moving Average (SMMA) — slower and smoother than EMA.
SMA = Simple Moving Average.

Run from the project root::

    python3 -m work.output.candlestick
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

matplotlib.use("Agg")

from work.scripts.analytics.moving_averages import smma as _smma

GRAPHICS_DIR = Path(__file__).resolve().parents[2] / "work" / "graphics" / "analysis"


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

@dataclass
class Theme:
    name: str
    bg: str;
    panel: str;
    grid: str
    text1: str;
    text2: str
    green: str;
    red: str
    blue: str;
    yellow: str;
    purple: str


DARK = Theme(
    name="dark",
    bg="#0b0e11", panel="#161b22", grid="#2a2e39",
    text1="#eaecef", text2="#848e9c",
    green="#0ecb81", red="#f6465d",
    blue="#1e96fc", yellow="#f0b90b", purple="#a855f7",
)

LIGHT = Theme(
    name="light",
    bg="#f0f2f5", panel="#ffffff", grid="#dde1e7",
    text1="#1a1a2e", text2="#555f6d",
    green="#0a8f5c", red="#d63031",
    blue="#0066cc", yellow="#c47c00", purple="#7c3aed",
)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def _load() -> pd.DataFrame:
    """Load NVDA daily OHLCV from the database."""

    from work.scripts.db.session import Database
    from work.scripts.services.stock_quote_service import StockQuoteService

    df = StockQuoteService(Database()).get_all_quotes_df()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    current_year = pd.Timestamp.now().year
    df = df[df["trade_date"].dt.year.between(1990, current_year)].copy()
    df = df.sort_values("trade_date").reset_index(drop=True)
    df["year"] = df["trade_date"].dt.year
    return df


def _weekly(df: pd.DataFrame) -> pd.DataFrame:
    """Resample daily rows to weekly OHLCV candles."""

    w = df.set_index("trade_date").resample("W").agg(
        open_price=("open_price", "first"),
        high_price=("high_price", "max"),
        low_price=("low_price", "min"),
        close_price=("close_price", "last"),
        volume=("volume", "sum"),
    ).dropna()
    w.index.name = "week"
    return w.reset_index()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ax_style(ax: plt.Axes, t: Theme,
              xlabel: str = "", ylabel: str = "",
              grid_axis: str = "y") -> None:
    ax.set_facecolor(t.panel)
    ax.tick_params(colors=t.text2, labelsize=10)
    for sp in ax.spines.values():
        sp.set_color(t.grid)
    ax.grid(axis=grid_axis, color=t.grid, linewidth=0.6,
            linestyle="--", alpha=0.65)
    ax.set_axisbelow(True)
    if xlabel:
        ax.set_xlabel(xlabel, color=t.text2, fontsize=11)
    if ylabel:
        ax.set_ylabel(ylabel, color=t.text2, fontsize=11)


def _legend(ax: plt.Axes, t: Theme, **kw) -> None:
    leg = ax.legend(fontsize=10, **kw)
    leg.get_frame().set_facecolor(t.panel)
    leg.get_frame().set_edgecolor(t.grid)
    for txt in leg.get_texts():
        txt.set_color(t.text2)


def _save(fig: plt.Figure, path: Path, t: Theme) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=t.bg)
    plt.close(fig)
    rel = path.relative_to(GRAPHICS_DIR)
    print(f"  [OK] {t.name}/{rel}")


# ---------------------------------------------------------------------------
# Chart: candlestick (one year, weekly)
# ---------------------------------------------------------------------------

def chart_candles(weekly: pd.DataFrame, year: int, t: Theme) -> None:
    """Weekly candlestick + volume for one year."""

    df = weekly[weekly["week"].dt.year == year].reset_index(drop=True)
    if df.empty:
        return

    x = np.arange(len(df))
    cw = 0.4

    fig = plt.figure(figsize=(14, 8), facecolor=t.bg)
    ax_p = fig.add_axes([0.07, 0.32, 0.90, 0.60])
    ax_v = fig.add_axes([0.07, 0.07, 0.90, 0.22])

    _ax_style(ax_p, t, ylabel="Цена ($)")
    _ax_style(ax_v, t, ylabel="Объём (млн)")

    for i, row in df.iterrows():
        bull = row["close_price"] >= row["open_price"]
        color = t.green if bull else t.red
        lo = min(row["open_price"], row["close_price"])
        bh = max(abs(row["close_price"] - row["open_price"]), 0.01)

        ax_p.plot([i, i], [row["low_price"], row["high_price"]],
                  color=color, linewidth=1.0, zorder=2)
        ax_p.add_patch(mpatches.FancyBboxPatch(
            (i - cw / 2, lo), cw, bh,
            boxstyle="square,pad=0",
            facecolor=color, edgecolor=color,
            linewidth=0.4, zorder=3,
        ))

    # 4-week MA
    ma4 = df["close_price"].rolling(4, min_periods=1).mean()
    ax_p.plot(x, ma4, color=t.yellow, linewidth=1.8,
              zorder=4, label="MA 4 нед.")
    _legend(ax_p, t, loc="upper left")

    # Volume
    vol_c = [t.green if r["close_price"] >= r["open_price"]
             else t.red for _, r in df.iterrows()]
    ax_v.bar(x, df["volume"] / 1e6, color=vol_c, alpha=0.75, width=0.6)

    # Month ticks
    ru = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
          "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    ticks, labels, seen = [], [], None
    for i, row in df.iterrows():
        m = row["week"].month
        if m != seen:
            ticks.append(i);
            labels.append(ru[m - 1]);
            seen = m

    for ax in (ax_p, ax_v):
        ax.set_xlim(-0.8, len(df) - 0.2)
        ax.set_xticks(ticks)
    ax_p.set_xticklabels([])
    ax_v.set_xticklabels(labels, color=t.text2, fontsize=10)
    ax_p.set_ylim(df["low_price"].min() * 0.97,
                  df["high_price"].max() * 1.04)

    fig.suptitle(
        f"NVIDIA (NVDA) — {year}  "
        f"[{df['close_price'].iloc[0]:.2f}$ → {df['close_price'].iloc[-1]:.2f}$]",
        color=t.text1, fontsize=14, fontweight="bold", y=0.97,
    )
    _save(fig, GRAPHICS_DIR / t.name / "years" / str(year)
          / f"nvda_candles_{year}.png", t)


# ---------------------------------------------------------------------------
# Chart: SMA per year
# ---------------------------------------------------------------------------

def chart_sma_year(df: pd.DataFrame, year: int, t: Theme) -> None:
    """SMA 10 / 20 / 50 for one calendar year."""

    yr = df[df["year"] == year].reset_index(drop=True)
    if yr.empty:
        return

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=t.bg)
    _ax_style(ax, t, xlabel="Дата", ylabel="Цена ($)")

    ax.plot(yr["trade_date"], yr["close_price"],
            color=t.text2, linewidth=0.9, alpha=0.5, label="Цена закрытия")

    for p, color, lbl in [
        (10, t.blue, "SMA 10"),
        (20, t.yellow, "SMA 20"),
        (50, t.purple, "SMA 50"),
    ]:
        sma = yr["close_price"].rolling(p, min_periods=1).mean()
        ax.plot(yr["trade_date"], sma, color=color,
                linewidth=2.0, label=lbl)

    _legend(ax, t)
    fig.suptitle(f"NVIDIA (NVDA) — SMA {year}",
                 color=t.text1, fontsize=14, fontweight="bold")
    _save(fig, GRAPHICS_DIR / t.name / "years" / str(year)
          / f"nvda_sma_{year}.png", t)


# ---------------------------------------------------------------------------
# Chart: SME per year
# ---------------------------------------------------------------------------

def chart_sme_year(df: pd.DataFrame, year: int, t: Theme) -> None:
    """SME (Smoothed Moving Average) 10 / 20 / 50 for one calendar year."""

    yr = df[df["year"] == year].reset_index(drop=True)
    if yr.empty:
        return

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=t.bg)
    _ax_style(ax, t, xlabel="Дата", ylabel="Цена ($)")

    ax.plot(yr["trade_date"], yr["close_price"],
            color=t.text2, linewidth=0.9, alpha=0.5, label="Цена закрытия")

    for p, color, lbl in [
        (10, t.green, "SME 10"),
        (20, t.yellow, "SME 20"),
        (50, t.purple, "SME 50"),
    ]:
        sme = _smma(yr["close_price"], p)
        ax.plot(yr["trade_date"], sme, color=color,
                linewidth=2.0, label=lbl)

    _legend(ax, t)
    fig.suptitle(f"NVIDIA (NVDA) — SME {year}",
                 color=t.text1, fontsize=14, fontweight="bold")
    _save(fig, GRAPHICS_DIR / t.name / "years" / str(year)
          / f"nvda_sme_{year}.png", t)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate all charts for both themes."""

    print("[INFO] Loading data...")
    df = _load()
    weekly = _weekly(df)
    years = sorted(df["year"].unique())
    print(f"[INFO] {len(df)} daily rows | {len(weekly)} weekly candles "
          f"| {years[0]}–{years[-1]}\n")

    for theme in (DARK, LIGHT):
        print(f"── {theme.name.upper()} ─────────────────────────────")

        for year in years:
            chart_candles(weekly, year, theme)
            chart_sma_year(df, year, theme)
            chart_sme_year(df, year, theme)

        print()

    print("[DONE]")


if __name__ == "__main__":
    main()
