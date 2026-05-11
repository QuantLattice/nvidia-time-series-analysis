"""Service layer for stock quote operations.

This module provides the application-level API for creating, updating,
deleting, and retrieving stock quote data. It bridges the presentation
layer, the repository layer, and the ORM model layer.

The service is responsible for:
- converting DTOs to ORM entities
- converting ORM entities to DTOs
- exposing read methods for GUI and analytics layers
- preparing DataFrames for reporting and analysis
"""


import pandas as pd

from work.scripts.db.session import Database
from work.scripts.repositories.stock_quote_repository import (
    StockQuoteRepository
)
from work.scripts.db.models import StockQuote
from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.dto import (
    StockQuoteCreateDTO,
    StockQuoteUpdateDTO,
    StockQuoteDTO
)

from datetime import date
from typing import Optional, List


class StockQuoteService:
    """Business service for stock quote management.

    This service encapsulates repository access and performs conversions
    between DTOs, ORM entities, and pandas DataFrames.

    Parameters
    ----------
    db : Database
        Database connection manager used to create transactional sessions.

    Notes
    -----
    - Create operations accept StockQuoteCreateDTO.
    - Update operations accept StockQuoteUpdateDTO.
    - Read operations return StockQuoteDTO or pandas DataFrame.
    """

    def __init__(self, db: Database) -> None:
        """Initialize service with a database manager.

        Parameters
        ----------
        db : Database
            Database connection manager.
        """

        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create_quote(self, data: dict) -> dict:
        """Create a new stock quote record.

        Parameters
        ----------
        data : dict
            Raw field values for a new stock quote.

        Returns
        -------
        dict
            Created stock quote with generated identifier.
        """

        if isinstance(data.get("trade_date"), str):
            data = {**data, "trade_date": date.fromisoformat(data["trade_date"])}

        dto = StockQuoteCreateDTO(**data)
        entity = self._to_entity(dto)

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            saved = repo.add(entity)
            session.flush()
            return self._serialize(saved)

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

        entities = [self._to_entity(dto) for dto in dtos]

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            repo.bulk_add(entities)

    # ============================================================
    # UPDATE
    # ============================================================

    def update_quote_by_id(
        self,
        quote_id: int,
        dto: StockQuoteUpdateDTO
    ) -> Optional[dict]:
        """Update an existing stock quote by identifier.

        Parameters
        ----------
        quote_id : int
            Identifier of the record to update.
        dto : StockQuoteUpdateDTO
            Partial update payload.

        Returns
        -------
        dict | None
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

            return self._serialize(entity)

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
            return repo.delete_by_id(quote_id)

    # ============================================================
    # READ
    # ============================================================

    def get_quote_by_id(self, quote_id: int) -> Optional[dict]:
        """Retrieve a stock quote by identifier.

        Parameters
        ----------
        quote_id : int
            Identifier of the record.

        Returns
        -------
        dict | None
            Stock quote data if found, otherwise None.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            entity = repo.get_by_id(quote_id)

            if entity is None:
                return None

            return self._serialize(entity)

    def get_all_quotes(self) -> List[dict]:
        """Retrieve all stock quotes.

        Returns
        -------
        list[dict]
            All stock quote records as plain dictionaries.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)

            return [self._serialize(q) for q in repo.get_all()]

    def get_quotes_by_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> List[StockQuoteDTO]:
        """Retrieve stock quotes within a date range.

        Parameters
        ----------
        start_date : date
            Start of the date range.
        end_date : date
            End of the date range.

        Returns
        -------
        list[StockQuoteDTO]
            Matching stock quote records as DTOs.
        """

        with self.db.session() as session:
            repo = StockQuoteRepository(session)

            return [
                self._to_dto(q)
                for q in repo.get_by_date_range(start_date, end_date)
            ]

    # ============================================================
    # DATAFRAME
    # ============================================================

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

            quotes = repo.get_by_date_range(start_date, end_date)

            return self._to_dataframe(quotes)

    # ============================================================
    # DTO ↔ ORM
    # ============================================================

    def _to_entity(self, dto: StockQuoteCreateDTO) -> StockQuote:
        """Convert creation DTO into ORM entity.

        Parameters
        ----------
        dto : StockQuoteCreateDTO
            Input DTO with stock quote data.

        Returns
        -------
        StockQuote
            ORM entity ready for persistence.
        """

        return StockQuote(
            trade_date=dto.trade_date,
            source=dto.source,
            open_price=dto.open_price,
            high_price=dto.high_price,
            low_price=dto.low_price,
            close_price=dto.close_price,
            volume=dto.volume,
            adj_close_price=dto.adj_close_price,
        )

    def _serialize(self, entity: StockQuote) -> dict:
        """Convert ORM entity into a plain dictionary.

        Parameters
        ----------
        entity : StockQuote
            ORM entity loaded from the database.

        Returns
        -------
        dict
            Serialized stock quote suitable for presentation and API layers.
        """

        return {
            "id":              entity.id,
            "trade_date":      entity.trade_date,
            "source":          entity.source,
            "open_price":      float(entity.open_price),
            "high_price":      float(entity.high_price),
            "low_price":       float(entity.low_price),
            "close_price":     float(entity.close_price),
            "adj_close_price": float(entity.adj_close_price)
                               if entity.adj_close_price is not None else None,
            "volume":          int(entity.volume),
        }

    def _to_dataframe(self, quotes: List[StockQuote]) -> pd.DataFrame:
        """Convert ORM entities to a pandas DataFrame.

        Parameters
        ----------
        quotes : list[StockQuote]
            List of ORM objects.

        Returns
        -------
        pd.DataFrame
            Tabular representation of stock quote data.
        """

        return pd.DataFrame(
            [
                {
                    S.TRADE_DATE: q.trade_date,
                    S.SOURCE: q.source,
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
