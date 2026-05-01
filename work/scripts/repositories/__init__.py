"""Repository layer package.

This package contains repository classes responsible for database access
and ORM operations. Repositories encapsulate all persistence logic and
provide a clean interface for the service layer.
"""


from .stock_quote_repository import StockQuoteRepository


__all__ = [
    "StockQuoteRepository"
]
