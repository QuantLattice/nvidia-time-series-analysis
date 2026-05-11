"""NVIDIA stock charts — dark & light themes, one PNG per chart.

Output structure in work/graphics/analysis/:

    dark/
        nvda_avg_price.png
        nvda_volume.png
        nvda_growth.png
        decades/
            2000s/  nvda_price_line_2000s.png
            2010s/  nvda_price_line_2010s.png
            2020s/  nvda_price_line_2020s.png
            ...
    light/
        (same structure)

Run from the project root::

    python3 -m work.output.charts
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import matplotlib
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

matplotlib.use("Agg")

GRAPHICS_DIR = Path(__file__).resolve().parents[2] / "work" / "graphics" / "analysis"


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

@dataclass
class Theme:
    """Color palette for one visual theme."""

    name:   str
    bg:     str
    panel:  str
    grid:   str
    text1:  str
    text2:  str
    green:  str
    red:    str
    blue:   str
    yellow: str
    purple: str


DARK = Theme(
    name="dark",
    bg="#0b0e11",    panel="#161b22",  grid="#2a2e39",
    text1="#eaecef", text2="#848e9c",
    green="#0ecb81", red="#f6465d",
    blue="#1e96fc",  yellow="#f0b90b", purple="#a855f7",
)

LIGHT = Theme(
    name="light",
    bg="#f0f2f5",    panel="#ffffff",  grid="#dde1e7",
    text1="#1a1a2e", text2="#555f6d",
    green="#0a8f5c", red="#d63031",
    blue="#0066cc",  yellow="#c47c00", purple="#7c3aed",
)

def _year_colors(years: list[int], t: Theme) -> dict[int, str]:
    """Map each year to a color from the theme or a colormap for large ranges."""
    fixed = [t.blue, t.green, t.red, t.yellow, t.purple]
    n = len(years)
    if n <= len(fixed):
        return {y: fixed[i] for i, y in enumerate(sorted(years))}
    positions = [i / n for i in range(n)]
    return {y: mcolors.to_hex(plt.cm.tab20(pos))
            for y, pos in zip(sorted(years), positions)}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def _load() -> pd.DataFrame:
    """Load NVDA data from the database."""

    from work.scripts.db.session import Database
    from work.scripts.services.stock_quote_service import StockQuoteService

    df = StockQuoteService(Database()).get_all_quotes_df()
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    current_year = pd.Timestamp.now().year
    df = df[df["trade_date"].dt.year.between(1990, current_year)].copy()
    df = df.sort_values("trade_date").reset_index(drop=True)
    df["year"] = df["trade_date"].dt.year
    return df


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _new_fig(title: str, t: Theme,
             figsize: tuple[float, float] = (10, 6)) -> tuple[plt.Figure, plt.Axes]:
    """Create a themed figure with one axes."""

    fig, ax = plt.subplots(figsize=figsize, facecolor=t.bg)
    ax.set_facecolor(t.panel)
    ax.set_title(title, color=t.text1, fontsize=14, fontweight="bold", pad=14)
    ax.tick_params(colors=t.text2, labelsize=11)
    for spine in ax.spines.values():
        spine.set_color(t.grid)
    ax.grid(axis="y", color=t.grid, linewidth=0.6, linestyle="--", alpha=0.7)
    ax.set_axisbelow(True)
    return fig, ax


def _label_axis(ax: plt.Axes, t: Theme, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, color=t.text2, fontsize=11)
    ax.set_ylabel(ylabel, color=t.text2, fontsize=11)


def _save(fig: plt.Figure, filename: str, t: Theme) -> None:
    path = GRAPHICS_DIR / t.name / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=t.bg)
    plt.close(fig)
    print(f"  [OK] {t.name}/{filename}")


# ---------------------------------------------------------------------------
# Chart 1 — Average close price by year
# ---------------------------------------------------------------------------

def chart_avg_price(df: pd.DataFrame, t: Theme) -> None:
    """Bar chart: average closing price per year."""

    avg = df.groupby("year")["close_price"].mean()
    yc  = _year_colors(list(avg.index), t)
    colors = [yc[y] for y in avg.index]
    n = len(avg)

    fig, ax = _new_fig("Средняя цена акции NVIDIA по годам", t,
                       figsize=(max(10, n * 0.6), 6))
    bars = ax.bar(avg.index.astype(str), avg.values,
                  color=colors, width=0.55, zorder=3)

    lbl_fs = max(7, 12 - n // 5)
    for bar, val in zip(bars, avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                val + 1.5, f"${val:.0f}",
                ha="center", va="bottom",
                color=t.text1, fontsize=lbl_fs, fontweight="bold")

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             fontsize=max(8, 11 - n // 8))
    _label_axis(ax, t, "Год", "Цена ($)")
    _save(fig, "nvda_avg_price.png", t)


# ---------------------------------------------------------------------------
# Chart 2 — Close price line over time
# ---------------------------------------------------------------------------

def chart_price_line(df: pd.DataFrame, t: Theme) -> None:
    """One PNG per decade: NVDA close price line chart."""

    df = df.copy()
    df["decade"] = (df["trade_date"].dt.year // 10) * 10

    for decade, group in df.groupby("decade"):
        group = group.sort_values("trade_date")
        y0 = int(group["trade_date"].dt.year.min())
        y1 = int(group["trade_date"].dt.year.max())
        decade_label = f"{decade}s"

        fig, ax = _new_fig(f"Цена акции NVIDIA {y0}–{y1}", t)
        ax.plot(group["trade_date"], group["close_price"],
                color=t.green, linewidth=1.5, zorder=3)
        ax.fill_between(group["trade_date"], group["close_price"],
                        alpha=0.10, color=t.green)

        for year in range(y0 + 1, y1 + 1):
            ax.axvline(pd.Timestamp(f"{year}-01-01"),
                       color=t.grid, linewidth=1, linestyle="--", alpha=0.8)
            ax.text(pd.Timestamp(f"{year}-01-01"),
                    0.97, str(year),
                    transform=ax.get_xaxis_transform(),
                    color=t.text2, fontsize=9,
                    ha="left", va="top")

        _label_axis(ax, t, "Дата", "Цена закрытия ($)")
        ax.grid(axis="x", color=t.grid, linewidth=0.6, linestyle="--", alpha=0.4)
        _save(fig, f"decades/{decade_label}/nvda_price_line_{decade_label}.png", t)


# ---------------------------------------------------------------------------
# Chart 3 — Total volume by year
# ---------------------------------------------------------------------------

def chart_volume(df: pd.DataFrame, t: Theme) -> None:
    """Bar chart: total trading volume per year."""

    vol    = df.groupby("year")["volume"].sum() / 1e9
    yc     = _year_colors(list(vol.index), t)
    colors = [yc[y] for y in vol.index]
    n = len(vol)

    fig, ax = _new_fig("Общий объём торгов NVIDIA по годам", t,
                       figsize=(max(10, n * 0.6), 6))
    bars = ax.bar(vol.index.astype(str), vol.values,
                  color=colors, width=0.55, zorder=3)

    lbl_fs = max(7, 12 - n // 5)
    for bar, val in zip(bars, vol.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                val + 0.5, f"{val:.0f} млрд",
                ha="center", va="bottom",
                color=t.text1, fontsize=lbl_fs, fontweight="bold")

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             fontsize=max(8, 11 - n // 8))
    _label_axis(ax, t, "Год", "Объём (млрд акций)")
    _save(fig, "nvda_volume.png", t)


# ---------------------------------------------------------------------------
# Chart 4 — Yearly % growth
# ---------------------------------------------------------------------------

def chart_growth(df: pd.DataFrame, t: Theme) -> None:
    """Bar chart: year-over-year % change in close price."""

    growth = df.groupby("year")["close_price"].last().pct_change() * 100
    growth = growth.dropna()
    colors = [t.green if v >= 0 else t.red for v in growth.values]
    n = len(growth)

    fig, ax = _new_fig("Годовой рост цены акции NVIDIA (%)", t,
                       figsize=(max(10, n * 0.6), 6))
    bars = ax.bar(growth.index.astype(str), growth.values,
                  color=colors, width=0.55, zorder=3)
    ax.axhline(0, color=t.text2, linewidth=1)

    lbl_fs = max(7, 12 - n // 5)
    for bar, val in zip(bars, growth.values):
        offset = 2 if val >= 0 else -8
        ax.text(bar.get_x() + bar.get_width() / 2,
                val + offset, f"{val:+.0f}%",
                ha="center", va="bottom",
                color=t.text1, fontsize=lbl_fs, fontweight="bold")

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             fontsize=max(8, 11 - n // 8))
    _label_axis(ax, t, "Год", "Изменение цены (%)")
    _save(fig, "nvda_growth.png", t)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Generate all charts for both dark and light themes."""

    print("[INFO] Loading data...")
    df = _load()
    print(f"[INFO] {len(df)} rows | "
          f"{df['trade_date'].min().date()} – {df['trade_date'].max().date()}\n")

    for theme in (DARK, LIGHT):
        print(f"── {theme.name.upper()} ─────────────────────────────")
        chart_avg_price(df, theme)
        chart_price_line(df, theme)
        chart_volume(df, theme)
        chart_growth(df, theme)
        print()

    print("[DONE]")


if __name__ == "__main__":
    main()
