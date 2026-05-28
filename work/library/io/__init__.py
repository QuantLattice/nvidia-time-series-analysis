"""Input/Output utilities for data loading and export operations.

This package provides low-level I/O functionality for reading external
data sources and exporting analysis results from the application.

Currently supports:
- CSV file loading into pandas DataFrame format;
- CSV, PNG, and PDF export for DataFrames and matplotlib figures.
"""

from work.library.io.csv_loader import CSVLoader
from work.library.io.exporter import Exporter


__all__ = [
    "CSVLoader",
    "Exporter",
]
