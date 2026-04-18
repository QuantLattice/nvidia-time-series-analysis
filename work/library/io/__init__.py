"""Input/Output utilities for data loading operations.

This package provides low-level I/O functionality for reading external
data sources into the application.

Currently supports:
- CSV file loading into pandas DataFrame format
"""

from work.library.io.csv_loader import CSVLoader


__all__ = [
    "CSVLoader",
]
