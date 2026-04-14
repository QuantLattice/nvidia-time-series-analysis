"""Contracts package for standardized data schemas.

This package defines schema constants and DataFrame wrappers used to ensure
consistent column naming across the application.
"""

from .stock_quote_schema import StockQuoteSchema
from .stock_quote_frame import StockQuoteFrame

__all__ = ["StockQuoteSchema", "StockQuoteFrame"]
