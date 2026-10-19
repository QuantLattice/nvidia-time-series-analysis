"""Repository layer for StockQuote database operations.

Implements the repository pattern for StockQuote entities using
SQLAlchemy ORM. Encapsulates all direct database interactions and
provides a clean abstraction over persistence logic.

Read/query methods are provided via StockQuoteRepositoryQueryMixin.

Notes
-----
- This layer operates strictly with ORM models (StockQuote).
- It does not contain business logic.
- Transaction management is handled externally (e.g. Database.session).

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

from typing import List

from sqlalchemy.orm import Session

from work.scripts.db.models import StockQuote
from work.scripts.repositories.stock_quote_repository_queries import (
    StockQuoteRepositoryQueryMixin,
)


class StockQuoteRepository(StockQuoteRepositoryQueryMixin):
    """Data access layer for StockQuote entity.

    Provides CRUD operations for stock quote records.
    Read/query methods are inherited from
    StockQuoteRepositoryQueryMixin.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy database session.

    Notes
    -----
    - The repository does not commit transactions.
    - All operations are executed within the provided session.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Parameters
        ----------
        session : Session
            Active SQLAlchemy session.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.session.add(quote)

    def create_bulk(self, quotes: List[StockQuote]) -> None:
        """Add multiple stock quote entities to the session.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM entities to be added.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.session.add_all(quotes)

    # ============================================================
    # UPDATE
    # ============================================================

    def update(self, quote: StockQuote) -> None:
        """Update an existing stock quote entity via merge.

        Parameters
        ----------
        quote : StockQuote
            ORM entity with updated fields.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.session.delete(quote)

    def delete_all(self) -> None:
        """Delete all stock quote records.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.session.query(StockQuote).delete(
            synchronize_session=False
        )
