"""
Statistics text helpers for the analysis and features sections.

Module-level functions that compute descriptive statistics and return
formatted multi-line strings. These helpers contain no GUI or instance
state — they depend only on their arguments.

Авторы
------
Черкащенко Данил Дмитриевич,
Ловчиков Станислав Олегович,
Андреева Мария Александровна
"""

import statistics as st
from datetime import date
from typing import Any, List


def build_stats_text(
    quotes: List[Any],
    start_date: date,
    end_date: date,
) -> str:
    """
    Compute descriptive stats for close price, high/low, and volume.

    Parameters
    ----------
    quotes : list[Any]
        List of quote dictionaries returned by the controller.
    start_date : date
        Start of the analyzed date range.
    end_date : date
        End of the analyzed date range.

    Returns
    -------
    str
        Formatted multi-line statistics text.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    closes = [q["close_price"] for q in quotes]
    volumes = [q["volume"] for q in quotes]
    highs = [q["high_price"] for q in quotes]
    lows = [q["low_price"] for q in quotes]

    def fmt_vol(v: float) -> str:
        """Format volume as human-readable string (K/M suffix).

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        if v >= 1_000_000:
            return f"{v / 1_000_000:.2f}M"
        if v >= 1_000:
            return f"{v / 1_000:.1f}K"
        return str(int(v))

    lines = [
        "Период:",
        f"  {start_date}",
        f"  {end_date}",
        f"Торговых дней: {len(quotes)}",
        "",
        "─── Цена закрытия ───",
        f"Мин:     ${min(closes):.2f}",
        f"Макс:    ${max(closes):.2f}",
        f"Среднее: ${sum(closes)/len(closes):.2f}",
        f"Медиана: ${st.median(closes):.2f}",
        f"σ:       ${st.stdev(closes):.2f}" if len(closes) > 1 else "",
        "",
        "─── High / Low ──────",
        f"Max High: ${max(highs):.2f}",
        f"Min Low:  ${min(lows):.2f}",
        f"Диапазон: ${max(highs) - min(lows):.2f}",
        "",
        "─── Объём торгов ────",
        f"Мин:     {fmt_vol(min(volumes))}",
        f"Макс:    {fmt_vol(max(volumes))}",
        f"Среднее: {fmt_vol(sum(volumes)/len(volumes))}",
    ]

    return "\n".join(lines)


def build_feature_stats_text(
    df,
    selected_columns: List[str],
) -> str:
    """
    Compute descriptive stats for each selected feature column.

    Parameters
    ----------
    df : pandas.DataFrame
        Features DataFrame with a DatetimeIndex.
    selected_columns : list[str]
        Column names to summarize.

    Returns
    -------
    str
        Formatted multi-line statistics text.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """

    lines: List[str] = []
    for col in selected_columns:
        if col not in df.columns:
            continue
        values = [v for v in df[col].dropna().tolist()]
        if not values:
            continue
        lines.append(f"── {col} ──")
        lines.append(f"  Кол-во: {len(values)}")
        lines.append(f"  Мин:    {min(values):.4f}")
        lines.append(f"  Макс:   {max(values):.4f}")
        lines.append(f"  Среднее:{sum(values)/len(values):.4f}")
        lines.append(f"  Медиана:{st.median(values):.4f}")
        if len(values) > 1:
            lines.append(f"  σ:      {st.stdev(values):.4f}")
        lines.append("")

    return "\n".join(lines)
