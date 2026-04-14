"""Service layer for StockQuote business logic.

This module provides a high-level API over the repository layer and converts
ORM entities into pandas DataFrames for analytical processing.
"""


from datetime import date
import pandas as pd

from work.scripts.db.session import Database
from work.scripts.repositories.stock_quote_repository import (
    StockQuoteRepository
)
from work.scripts.db.models import StockQuote
from work.scripts.contracts import StockQuoteSchema as S


class StockQuoteService:
    """Business service for StockQuote operations.

    This service encapsulates database access and provides DataFrame-based
    interfaces for analytics and reporting.

    Parameters
    ----------
    db : Database
        Database manager instance.
    """

    def __init__(self, db: Database) -> None:
        """Initialize service with database manager.

        Parameters
        ----------
        db : Database
            Database connection manager.
        """

        self.db = db

    def get_all_quotes_df(self) -> pd.DataFrame:
        """Retrieve all stock quotes as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Full dataset of stock quotes.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            quotes = repo.get_all()
            return self._to_dataframe(quotes)

    def get_quotes_by_date_range_df(
        self,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """Retrieve stock quotes within a date range as DataFrame.

        Parameters
        ----------
        start_date : date
            Start date of the range.
        end_date : date
            End date of the range.

        Returns
        -------
        pd.DataFrame
            Filtered stock quote dataset.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            quotes = repo.get_by_date_range(start_date, end_date)
            return self._to_dataframe(quotes)

    def add_quote(self, quote: StockQuote) -> None:
        """Insert a single stock quote.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to insert.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.add(quote)

    def add_quote_bulk(self, quotes: list[StockQuote]) -> None:
        """Insert multiple stock quotes.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM entities.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.bulk_add(quotes)

    def update_quote(self, quote: StockQuote) -> None:
        """Update stock quote.

        Parameters
        ----------
        quote : StockQuote
            Modified ORM entity.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.update(quote)

    def delete_quote(self, quote: StockQuote) -> None:
        """Delete stock quote.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to delete.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.delete(quote)

    def _to_dataframe(self, quotes: list[StockQuote]) -> pd.DataFrame:
        """Convert ORM entities to pandas DataFrame.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM objects.

        Returns
        -------
        pd.DataFrame
            Tabular representation of stock data.
        """

        return pd.DataFrame(
            [
                {
                    S.TRADE_DATE: q.trade_date,
                    S.OPEN_PRICE: float(q.open_price),
                    S.HIGH_PRICE: float(q.high_price),
                    S.LOW_PRICE: float(q.low_price),
                    S.CLOSE_PRICE: float(q.close_price),

                    S.ADJ_CLOSE_PRICE: float(q.adj_close_price)
                    if q.adj_close_price is not None
                    else None,

                    S.VOLUME: q.volume
                }
                for q in quotes
            ],
            columns=S.ALL_COLUMNS
        )
