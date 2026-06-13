"""Service layer for stock quote operations.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd

from work.scripts.db.session import Database
from work.scripts.repositories.stock_quote_repository import (
    StockQuoteRepository
)
from work.scripts.dto import (
    StockQuoteCreateDTO,
    StockQuoteUpdateDTO,
    StockQuoteDTO
)
from work.scripts.services.stock_quote_mappers import (
    to_entity,
    to_dto,
    to_dataframe,
)

from datetime import date
from typing import Optional, List, Tuple


class StockQuoteService:
    """Business service for stock quote management.

    Parameters
    ----------
    db : Database
        Database connection manager.
    """

    def __init__(self, db: Database) -> None:
        """Initialize service with a database manager."""
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create_quote(self, dto: StockQuoteCreateDTO) -> StockQuoteDTO:
        """Create a new stock quote record.

        Parameters
        ----------
        dto : StockQuoteCreateDTO
            Input data for a new stock quote.

        Returns
        -------
        StockQuoteDTO
            Created stock quote with generated identifier.
        """

        entity = to_entity(dto)
        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.create(entity)
            session.flush()
            return to_dto(entity)

    def create_quote_bulk(
        self,
        dtos: List[StockQuoteCreateDTO]
    ) -> None:
        """Create multiple stock quote records.

        Parameters
        ----------
        dtos : list[StockQuoteCreateDTO]
            Input DTOs for batch insertion.
        """

        entities = [to_entity(dto) for dto in dtos]
        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.create_bulk(entities)

    # ============================================================
    # UPDATE
    # ============================================================

    def update_quote_by_id(
        self,
        quote_id: int,
        dto: StockQuoteUpdateDTO
    ) -> Optional[StockQuoteDTO]:
        """Update an existing stock quote by identifier.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to update.
        dto : StockQuoteUpdateDTO
            Partial update payload.

        Returns
        -------
        StockQuoteDTO | None
            Updated stock quote if found, otherwise None.

        Raises
        ------
        ValueError
            If no fields are provided for update.
        """

        update_data = dto.to_dict()
        update_data = {k: v for k, v in update_data.items() if v is not None}

        if not update_data:
            raise ValueError("No fields provided for update")

        with self.db.session() as session:
            repo = StockQuoteRepository(session)

            entity = repo.get_by_id(quote_id)
            if entity is None:
                return None

            for field, value in update_data.items():
                setattr(entity, field, value)

            repo.update(entity)

            return to_dto(entity)

    # ============================================================
    # DELETE
    # ============================================================

    def delete_quote_by_id(self, quote_id: int) -> bool:
        """Delete a stock quote by identifier.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to delete.

        Returns
        -------
        bool
            True if the record was deleted, False if no record was found.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            entity = repo.get_by_id(quote_id)
            if entity is None:
                return False
            repo.delete(entity)
            return True

    def delete_all_quotes(self) -> int:
        """Delete all stock quotes. Returns number of deleted rows."""

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            count = repo.count_all()
            repo.delete_all()
            return count

    # ============================================================
    # READ
    # ============================================================

    def get_quotes_page(
        self,
        page: int,
        page_size: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> Tuple[List[StockQuoteDTO], int]:
        offset = (page - 1) * page_size

        with self.db.session() as session:
            repo = StockQuoteRepository(session=session)
            total = repo.count_all()
            quotes = repo.get_page(
                offset=offset,
                limit=page_size,
                sort_col=sort_col,
                sort_desc=sort_desc,
            )
            return [to_dto(entity=q) for q in quotes], total

    def get_quote_by_id(self, quote_id: int) -> Optional[StockQuoteDTO]:
        """Retrieve a stock quote by identifier.

        Parameters
        ----------
        quote_id : int
            Identifier of the record.

        Returns
        -------
        StockQuoteDTO | None
            Stock quote data if found, otherwise None.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            entity = repo.get_by_id(quote_id)
            if entity is None:
                return None
            return to_dto(entity)

    def get_all_quotes(self) -> List[StockQuoteDTO]:
        """Retrieve all stock quotes.

        Returns
        -------
        list[StockQuoteDTO]
            All stock quote records as DTOs.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return [to_dto(q) for q in repo.get_all()]

    def get_quotes_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> List[StockQuoteDTO]:
        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return [
                to_dto(q)
                for q in repo.get_by_date_range(start_date, end_date)
            ]

    # ============================================================
    # DATAFRAME
    # ============================================================

    def get_date_range(self) -> Tuple[Optional[date], Optional[date]]:
        """Return (min_date, max_date) across all stored quotes."""

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return repo.get_date_range()

    def get_all_quotes_df(self) -> pd.DataFrame:
        """Retrieve all stock quotes as a DataFrame.

        Returns
        -------
        pd.DataFrame
            Full dataset of stock quotes.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return to_dataframe(repo.get_all())

    def get_quotes_by_date_range_df(
        self,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """Retrieve stock quotes within a date range as a DataFrame.

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
            return to_dataframe(
                repo.get_by_date_range(start_date, end_date)
            )
