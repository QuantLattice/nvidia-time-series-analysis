"""
Data mapping utilities for stock quote import pipeline.

This package provides mappers that convert raw external datasets
into the internal contract schema used by downstream processing.
"""


from .stock_quote_mapper import (
    StockQuoteMapper
)


__all__ = [
    "StockQuoteMapper",
]
