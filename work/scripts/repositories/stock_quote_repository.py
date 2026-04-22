"""Repository layer for StockQuote database operations.

This module implements a repository pattern for accessing and manipulating
StockQuote entities in the database. It encapsulates all direct ORM queries
and provides a clean abstraction over SQLAlchemy session operations.
"""


from datetime import date
from collections.abc import Iterable

from sqlalchemy.orm import Session

from work.scripts.db.models import StockQuote


class StockQuoteRepository:
    """Data access layer for StockQuote entity.

    This repository provides CRUD operations and query methods for stock
    price data stored in the database.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy database session.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Parameters
        ----------
        session : Session
            Active SQLAlchemy session.
        """

        self.session = session

    _UPDATABLE_FIELDS = {
        "trade_date",
        "source",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
        "volume",
    }

    def get_all(self) -> list[StockQuote]:
        """Retrieve all stock quote records.

        Returns
        -------
        list[StockQuote]
            List of all stored stock quotes.
        """

        return (
            self.session.query(StockQuote)
            .order_by(StockQuote.trade_date.asc())
            .all()
        )

    def get_by_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> list[StockQuote]:
        """Retrieve stock quotes within a date range.

        Parameters
        ----------
        start_date : date
            Start of the date range (inclusive).
        end_date : date
            End of the date range (inclusive).

        Returns
        -------
        list[StockQuote]
            Filtered list of stock quotes.
        """

        return (
            self.session.query(StockQuote)
            .filter(StockQuote.trade_date.between(start_date, end_date))
            .all()
        )

    def get_by_id(self, quote_id: int) -> StockQuote | None:
        """Retrieve a stock quote by its primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the stock quote.

        Returns
        -------
        StockQuote | None
            Found record or None if not exists.
        """

        return self.session.get(StockQuote, quote_id)

    def get_by_trade_date(self, trade_date: date) -> StockQuote | None:
        """Retrieve the first stock quote with the given trade date."""

        return (
            self.session.query(StockQuote)
            .filter(StockQuote.trade_date == trade_date)
            .first()
        )

    def get_by_source(self, source: str) -> StockQuote | None:
        """Retrieve the first stock quote with the given source."""

        return (
            self.session.query(StockQuote)
            .filter(StockQuote.source == source)
            .first()
        )

    def add(self, quote: StockQuote) -> StockQuote:
        """Add a new stock quote to the session.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be persisted.
        """

        self.session.add(quote)
        self.session.flush()
        self.session.refresh(quote)
        return quote

    def bulk_add(self, quotes: Iterable[StockQuote]) -> list[StockQuote]:
        """Add multiple stock quotes to the session.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM entities to be added.
        """

        quote_list = list(quotes)
        self.session.add_all(quote_list)
        self.session.flush()
        for quote in quote_list:
            self.session.refresh(quote)
        return quote_list

    def update(self, quote: StockQuote) -> StockQuote:
        """Update an existing stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            Modified ORM entity.
        """

        merged_quote = self.session.merge(quote)
        self.session.flush()
        self.session.refresh(merged_quote)
        return merged_quote

    def update_by_id(
        self,
        quote_id: int,
        **fields  # type: ignore
    ) -> StockQuote | None:
        """Update stock quote fields by primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to update.
        **fields
            Key-value pairs of fields to update.
        """

        unknown_fields = set(fields) - self._UPDATABLE_FIELDS
        if unknown_fields:
            unknown = ", ".join(sorted(unknown_fields))
            raise ValueError(f"Unknown stock quote fields: {unknown}")

        quote = self.get_by_id(quote_id)
        if quote is None:
            return None

        for field_name, value in fields.items():
            setattr(quote, field_name, value)

        self.session.flush()
        self.session.refresh(quote)
        return quote

    def delete(self, quote: StockQuote) -> bool:
        """Delete a stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be deleted.
        """

        self.session.delete(quote)
        self.session.flush()
        return True

    def delete_by_id(self, quote_id: int) -> bool:
        """Delete stock quote by primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to delete.
        """

        obj = self.get_by_id(quote_id)

        if obj is None:
            return False

        self.delete(obj)
        return True
