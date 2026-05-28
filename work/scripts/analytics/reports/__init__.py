"""
High-level report assembly layer for analytics and time-series diagnostics.

This package provides composite report generators that aggregate multiple
analysis subsystems into unified, structured report objects suitable for:
- exploratory data analysis workflows;
- dashboard and visualization integration;
- machine learning diagnostics;
- quantitative research pipelines;
- automated reporting systems.

Available report groups
-----------------------

EDA reports
    Aggregate descriptive, distributional, rolling, categorical,
    and correlation analysis into a single exploratory analysis report.

Time-series reports
    Aggregate stationarity and autocorrelation diagnostics for
    structured time-series analysis workflows.
"""


from .eda_report import EDAReport, EDAReportResult
from .ts_report import (
    TSReport,
    TSReportResult
)


__all__ = [
    "EDAReport",
    "EDAReportResult",
    "TSReport",
    "TSReportResult"
]
