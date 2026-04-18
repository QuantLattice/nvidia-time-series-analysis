"""Contracts package for standardized data structures.

This package provides a unified interface for data schemas and DataFrame
wrappers used across the application.

Components
----------
StockQuoteSchema
    Defines standardized column names for stock market datasets.

StockQuoteFrame
    Provides a typed wrapper around pandas DataFrame for safer and more
    expressive data access.
"""


from .stock_quote_schema import StockQuoteSchema
from .stock_quote_frame import StockQuoteFrame


__all__ = [
    "StockQuoteSchema",
    "StockQuoteFrame",
]
