"""Controller layer package.

This package provides controllers that act as an interface between the GUI
and service layers. Controllers handle input parsing, error handling, and
response formatting.
"""


from .stock_quote_controller import StockQuoteController


__all__ = [
    "StockQuoteController"
]
