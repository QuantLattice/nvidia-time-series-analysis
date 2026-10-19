"""
Chart-building helpers for the analysis and features sections.

Module-level functions that construct Matplotlib Figure objects from
quote data or a features DataFrame. These helpers contain no GUI or
instance state — they depend only on their arguments.

Авторы
------
Черкащенко Данил Дмитриевич,
Ловчиков Станислав Олегович,
Андреева Мария Александровна
"""

import datetime
from datetime import date
from typing import Any, List

from matplotlib.figure import Figure
from work.library.plotting.rendering import MatplotlibRenderer
from work.library.plotting.contracts import (
    PlotContext,
    ChartConfig,
    LineStyle,
    ScatterStyle,
    BoxStyle,
    HistogramStyle,
)
from work.library.plotting.stack import LayerStack
from work.library.plotting.layers import (
    CandlestickLayer,
    LineLayer,
    ScatterLayer,
    BoxLayer,
    HistogramLayer,
)


def build_quote_figure(
    quotes: List[Any],
    chart_type: str,
    start_date: date,
    end_date: date,
) -> Figure:
    """
    Build a Matplotlib Figure from the given quotes and chart type.

    Parameters
    ----------
    quotes : list[Any]
        List of quote dictionaries returned by the controller.
    chart_type : str
        Chart type identifier (``"candlestick"``, ``"line"``,
        ``"scatter"``, ``"box"``, ``"histogram"``).
    start_date : date
        Start of the date range (used in the chart title).
    end_date : date
        End of the date range (used in the chart title).

    Returns
    -------
    matplotlib.figure.Figure
        Rendered figure ready to embed in the Tkinter canvas.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """
    # Convert trade_date strings/dates to datetime for matplotlib
    dates = [
        datetime.datetime.combine(
            datetime.date.fromisoformat(q["trade_date"])
            if isinstance(q["trade_date"], str)
            else q["trade_date"],
            datetime.time(),
        )
        for q in quotes
    ]
    closes = [q["close_price"] for q in quotes]

    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    context = PlotContext(figure=fig, primary_axes=ax)
    stack = LayerStack()

    if chart_type == "candlestick":
        opens = [q["open_price"] for q in quotes]
        highs = [q["high_price"] for q in quotes]
        lows = [q["low_price"] for q in quotes]
        n = len(dates)
        if n > 1:
            span = (dates[-1] - dates[0]).days or n
            width = (span / n) * 0.8
        else:
            width = 0.6
        layer = CandlestickLayer(
            x=dates, open=opens, high=highs, low=lows,
            close=closes, width=width,
        )
    elif chart_type == "line":
        layer = LineLayer(
            x=dates, y=closes,
            style=LineStyle(label="Close price"),
        )
    elif chart_type == "scatter":
        layer = ScatterLayer(
            x=dates, y=closes,
            style=ScatterStyle(label="Close price"),
        )
    elif chart_type == "box":
        layer = BoxLayer(
            values=closes,
            style=BoxStyle(label="Close price"),
        )
    else:
        layer = HistogramLayer(
            values=closes,
            style=HistogramStyle(label="Close price"),
        )

    stack.add_layer(layer)

    title_map = {
        "candlestick": "Candlestick chart",
        "line": "Close price — line",
        "scatter": "Close price — scatter",
        "box": "Price distribution — box",
        "histogram": "Price distribution — histogram",
    }
    xlabel_map = {
        "candlestick": "Date",
        "line": "Date",
        "scatter": "Date",
        "box": "Close price (USD)",
        "histogram": "Close price (USD)",
    }
    ylabel_map = {
        "candlestick": "Price (USD)",
        "line": "Price (USD)",
        "scatter": "Price (USD)",
        "box": "Price (USD)",
        "histogram": "Frequency",
    }

    chart_title = (
        f"{title_map.get(chart_type, chart_type)}"
        f"  |  {start_date} — {end_date}"
    )
    chart_config = ChartConfig(
        title=chart_title,
        xlabel=xlabel_map.get(chart_type, "Date"),
        primary_ylabel=ylabel_map.get(chart_type, "Price (USD)"),
    )

    renderer = MatplotlibRenderer()
    renderer.render(
        stack=stack, context=context, chart_config=chart_config
    )
    fig.tight_layout()

    return fig


def build_feature_figure(
    df,
    selected_columns: List[str],
) -> Figure:
    """
    Build a Matplotlib Figure with one line per selected column.

    Parameters
    ----------
    df : pandas.DataFrame
        Features DataFrame with a DatetimeIndex.
    selected_columns : list[str]
        Column names to render as individual lines.

    Returns
    -------
    matplotlib.figure.Figure
        Rendered multi-line feature chart.

    Авторы
    ------
    Черкащенко Данил Дмитриевич,
    Ловчиков Станислав Олегович,
    Андреева Мария Александровна
    """
    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    context = PlotContext(figure=fig, primary_axes=ax)
    stack = LayerStack()

    dates = df.index.to_pydatetime()

    for col in selected_columns:
        if col not in df.columns:
            continue
        values = df[col].ffill().tolist()
        stack.add_layer(LineLayer(
            x=dates,
            y=values,
            style=LineStyle(label=col),
        ))

    chart_config = ChartConfig(
        title=f"Features: {', '.join(selected_columns)}",
        xlabel="Date",
        primary_ylabel="Value",
    )

    renderer = MatplotlibRenderer()
    renderer.render(
        stack=stack, context=context, chart_config=chart_config
    )
    fig.tight_layout()

    return fig
