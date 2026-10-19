"""Validation and normalization utilities for StockQuote datasets.

This package provides preprocessing helpers for tabular stock market data,
including normalization of raw input frames and validation of data types,
missing values, and business rules.

Components
----------
StockQuoteNormalizer
    Utility for cleaning and standardizing raw stock quote DataFrames.

StockQuoteValidator
    Utility for validating StockQuote DataFrames against schema and
    business constraints.
"""


from .stock_quote_normalizer import (
    StockQuoteNormalizer
)
from .stock_quote_validator import (
    StockQuoteValidator
)


__all__ = [
    "StockQuoteNormalizer",

    "StockQuoteValidator",
]
