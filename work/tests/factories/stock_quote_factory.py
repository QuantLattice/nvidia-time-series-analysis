"""Factory for generating StockQuote test entities.

This module provides a deterministic factory for creating instances of
StockQuote model used in unit and integration tests.

It allows:
- fast creation of valid test entities
- overriding specific fields for edge-case testing
- consistent default dataset generation

Notes
-----
All generated objects are intended for testing only and should not be
used in production workflows.
"""


import itertools
from datetime import date, timedelta

from work.scripts.db.models import StockQuote

from typing import Optional


class StockQuoteFactory:
    """Factory for StockQuote ORM entities used in tests."""

    # Each call to create() without an explicit trade_date gets a unique
    # date starting from 2020-01-01, avoiding UNIQUE(trade_date, source)
    # conflicts across tests that share the same in-memory database.
    _counter: itertools.count = itertools.count(0)

    @classmethod
    def create(
        cls,
        *,
        trade_date: Optional[date] = None,
        source: str = "test-source",
        open_price: float = 100.0,
        high_price: float = 110.0,
        low_price: float = 90.0,
        close_price: float = 105.0,
        adj_close_price: Optional[float] = 105.0,
        volume: int = 1000,
    ) -> StockQuote:
        """Create a StockQuote instance with default or overridden values.

        Parameters
        ----------
        trade_date : date, optional
            Trading date. Auto-increments from 2020-01-01 if omitted.
        source : str
            Identifier of the data source.
        open_price : float
            Opening price of the asset.
        high_price : float
            Highest price during the trading session.
        low_price : float
            Lowest price during the trading session.
        close_price : float
            Closing price of the asset.
        adj_close_price : float or None
            Adjusted closing price accounting for splits/dividends.
        volume : int
            Number of traded shares.

        Returns
        -------
        StockQuote
            Fully initialized ORM entity ready for persistence.
        """
        if trade_date is None:
            trade_date = date(2020, 1, 1) + timedelta(days=next(cls._counter))

        return StockQuote(
            trade_date=trade_date,
            source=source,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            adj_close_price=adj_close_price,
            volume=volume,
        )
