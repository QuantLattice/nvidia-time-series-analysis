"""
Schema definitions for stock quote data.

This package contains schema constants and column alias mappings used
by the CSV import pipeline, normalization stage, and validation stage.
"""


from .column_aliases import StockQuoteColumnAliases
from .stock_quote_schema import StockQuoteSchema


__all__ = [
    "StockQuoteSchema",
    "StockQuoteColumnAliases",
]
