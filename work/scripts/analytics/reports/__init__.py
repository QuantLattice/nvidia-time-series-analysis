"""
EDA report assembly utilities.

This package exposes the top-level exploratory data analysis report
builder that combines multiple analytical subsystems into a single
structured result object.
"""


from .eda_report import EDAReport, EDAReportResult


__all__ = [
    "EDAReport",
    "EDAReportResult"
]
