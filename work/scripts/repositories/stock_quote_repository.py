"""Repository layer for StockQuote database operations.

This module implements a repository pattern for accessing and manipulating
StockQuote entities in the database. It encapsulates all direct ORM queries
and provides a clean abstraction over SQLAlchemy session operations.
"""


from sqlalchemy.orm import Session
from datetime import date

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

    def get_all(self) -> list[StockQuote]:
        """Retrieve all stock quote records.

        Returns
        -------
        list[StockQuote]
            List of all stored stock quotes.
        """

        return self.session.query(StockQuote).all()
    
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

    def add(self, quote: StockQuote) -> None:
        """Add a new stock quote to the session.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be persisted.
        """

        self.session.add(quote)

    def bulk_add(self, quotes: list[StockQuote]) -> None:
        """Add multiple stock quotes to the session.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM entities to be added.
        """

        self.session.add_all(quotes)

    def update(self, quote: StockQuote) -> None:
        """Update an existing stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            Modified ORM entity.
        """

        self.session.merge(quote)

    def update_by_id(
        self,
        quote_id: int,
        **fields  # type: ignore
    ) -> None:
        """Update stock quote fields by primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to update.
        **fields
            Key-value pairs of fields to update.
        """

        self.session.query(StockQuote).filter(
            StockQuote.id == quote_id
        ).update(fields, synchronize_session=False)  # type: ignore

    def delete(self, quote: StockQuote) -> None:
        """Delete a stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be deleted.
        """

        self.session.delete(quote)

    def delete_by_id(self, quote_id: int) -> None:
        """Delete stock quote by primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to delete.
        """

        obj = self.get_by_id(quote_id)

        if obj is not None:
            self.delete(obj)
