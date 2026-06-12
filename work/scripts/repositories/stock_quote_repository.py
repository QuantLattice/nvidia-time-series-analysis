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


from sqlalchemy import func
from sqlalchemy.orm import Session

from work.scripts.db.models import StockQuote

from datetime import date
from typing import Optional, List, Tuple


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

    def delete_all(self) -> None:
        """Delete all stock quote records."""

        self.session.query(StockQuote).delete(synchronize_session=False)

    # ============================================================
    # READ
    # ============================================================

    def count_all(self) -> int:
        return self.session.query(StockQuote).count()

    def get_page(
        self,
        offset: int,
        limit: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> list[StockQuote]:
        col = getattr(StockQuote, sort_col, StockQuote.trade_date)
        order = col.desc() if sort_desc else col.asc()
        return (
            self.session.query(StockQuote)
            .order_by(order)
            .offset(offset)
            .limit(limit)
            .all()
        )

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
        end_date: date,
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
            .order_by(StockQuote.trade_date.asc())
            .all()
        )

    def get_date_range(self) -> Tuple[Optional[date], Optional[date]]:
        """Return (min_date, max_date) of all stored quotes, or (None, None) if empty."""

        min_date, max_date = self.session.query(
            func.min(StockQuote.trade_date),
            func.max(StockQuote.trade_date),
        ).one()
        return min_date, max_date
