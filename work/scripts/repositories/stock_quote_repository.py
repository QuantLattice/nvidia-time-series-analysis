"""Repository layer for StockQuote database operations.

This module implements the repository pattern for accessing and
manipulating StockQuote entities using SQLAlchemy ORM.

The repository encapsulates all direct database interactions and provides
a clean abstraction over persistence logic, isolating the service layer
from ORM-specific details.

Responsibilities
----------------
- CRUD operations for StockQuote entities
- Querying data using domain-relevant methods
- Managing persistence within a given session scope

Notes
-----
- This layer operates strictly with ORM models (StockQuote).
- It does not contain business logic.
- Transaction management is handled externally (e.g., Database.session).
"""


from sqlalchemy.orm import Session

from work.scripts.db.models import StockQuote

from datetime import date
from typing import Optional, List


class StockQuoteRepository:
    """Data access layer for StockQuote entity.

    Provides methods for creating, reading, updating, and deleting stock
    quote records in the database.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy database session.

    Notes
    -----
    - The repository does not commit transactions.
    - All operations are executed within the provided session.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Parameters
        ----------
        session : Session
            Active SQLAlchemy session.
        """

        self.session = session

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, quote: StockQuote) -> None:
        """Add a new stock quote entity to the session.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be persisted.

        Notes
        -----
        The entity is staged for insertion. Commit is handled externally.
        """

        self.session.add(quote)

    def create_bulk(self, quotes: List[StockQuote]) -> None:
        """Add multiple stock quote entities to the session.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM entities to be added.

        Notes
        -----
        Suitable for batch insert operations.
        """

        self.session.add_all(quotes)

    # ============================================================
    # UPDATE
    # ============================================================

    def update(self, quote: StockQuote) -> None:
        """Update an existing stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            ORM entity with updated fields.

        Notes
        -----
        Uses SQLAlchemy merge to synchronize detached instances.
        """

        self.session.merge(quote)

    # ============================================================
    # DELETE
    # ============================================================
    def delete(self, quote: StockQuote) -> None:
        """Delete a stock quote entity.

        Parameters
        ----------
        quote : StockQuote
            ORM entity to be deleted.
        """

        self.session.delete(quote)

    # ============================================================
    # READ
    # ============================================================

    def get_by_id(self, quote_id: int) -> Optional[StockQuote]:
        """Retrieve a stock quote by its primary key.

        Parameters
        ----------
        quote_id : int
            Identifier of the stock quote.

        Returns
        -------
        StockQuote | None
            Found entity or None if not exists.
        """

        return self.session.get(StockQuote, quote_id)

    def get_all(self) -> List[StockQuote]:
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
    ) -> List[StockQuote]:
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
