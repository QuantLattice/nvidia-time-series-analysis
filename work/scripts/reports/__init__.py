"""
Report generation layer for stock data analysis.

This package provides structured report generators that produce
ready-to-consume objects for GUI rendering, CSV export, and printing.

Included reports
----------------
TextReport
    Human-readable plain-text dataset summary.

StatisticalReport
    Comprehensive per-column statistical metrics table.

PivotReport
    Grouped aggregation pivot table.
"""

from .text_report import TextReport, TextReportResult
from .statistical_report import StatisticalReport, StatisticalReportResult
from .pivot_report import PivotReport, PivotReportResult, PivotReportConfig
from .forecast_summary import ForecastSummary, ForecastSummaryResult
from .backtest_summary import BacktestSummary, BacktestSummaryResult


__all__ = [
    "TextReport",
    "TextReportResult",
    "StatisticalReport",
    "StatisticalReportResult",
    "PivotReport",
    "PivotReportResult",
    "PivotReportConfig",
    "ForecastSummary",
    "ForecastSummaryResult",
    "BacktestSummary",
    "BacktestSummaryResult",
]
