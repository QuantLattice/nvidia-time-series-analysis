"""Test factories package.

This package provides factory classes for generating synthetic test objects
used in unit and integration testing.

Factories reduce duplication in tests and provide a consistent way to
create valid and edge-case data structures.
"""


from .stock_quote_factory import StockQuoteFactory
from .dataframe_factory import DataFrameFactory


__all__ = [
    "StockQuoteFactory",
    "DataFrameFactory",
]
