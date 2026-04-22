"""Service layer for StockQuote business logic.

This module provides a high-level API over the repository layer and converts
ORM entities into pandas DataFrames for analytical processing.
"""

import math
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import pandas as pd

from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.db.models import StockQuote
from work.scripts.db.session import Database
from work.scripts.repositories.stock_quote_repository import (
    StockQuoteRepository
)


class StockQuoteService:
    """Business service for StockQuote operations.

    This service encapsulates database access and provides DataFrame-based
    interfaces for analytics and reporting.

    Parameters
    ----------
    db : Database
        Database manager instance.
    """

    _DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    _FIELD_NAMES = {
        "trade_date",
        "source",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
        "volume",
    }
    _REQUIRED_CREATE_FIELDS = {
        "trade_date",
        "source",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume",
    }
    _PRICE_FIELDS = {
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adj_close_price",
    }

    def __init__(self, db: Database) -> None:
        """Initialize service with database manager.

        Parameters
        ----------
        db : Database
            Database connection manager.
        """

        self.db = db

    def create_quote(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a stock quote from a plain dictionary."""

        quote = self._to_entity(data)
        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            self._ensure_source_available(repo, quote.source)
            created_quote = repo.add(quote)
            return self._to_dict(created_quote)

    def update_quote_by_id(
            self,
            quote_id: int,
            data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Update a stock quote by id and return the updated record."""

        normalized_data = self._normalize_update_data(data)
        if not normalized_data:
            raise ValueError("No stock quote fields were provided for update")

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            current_quote = repo.get_by_id(quote_id)
            if current_quote is None:
                return None

            if "trade_date" in normalized_data:
                self._ensure_trade_date_available(
                    repo,
                    normalized_data["trade_date"],
                    current_quote_id=quote_id
                )
            if "source" in normalized_data:
                self._ensure_source_available(
                    repo,
                    normalized_data["source"],
                    current_quote_id=quote_id
                )

            updated_quote = repo.update_by_id(quote_id, **normalized_data)
            if updated_quote is None:
                return None

            return self._to_dict(updated_quote)

    def delete_quote_by_id(self, quote_id: int) -> bool:
        """Delete a stock quote by id."""

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return repo.delete_by_id(quote_id)

    def get_quote_by_id(self, quote_id: int) -> dict[str, Any] | None:
        """Return a stock quote by id as a plain dictionary."""

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            quote = repo.get_by_id(quote_id)
            if quote is None:
                return None

            return self._to_dict(quote)

    def get_all_quotes(self) -> list[dict[str, Any]]:
        """Return all stock quotes as plain dictionaries."""

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return [
                self._to_dict(quote)
                for quote in repo.get_all()
            ]

    def get_quotes_by_date_range(
            self,
            start_date: date | datetime | str,
            end_date: date | datetime | str
    ) -> list[dict[str, Any]]:
        """Return stock quotes within an inclusive date range."""

        normalized_start_date = self._parse_date(start_date, "start_date")
        normalized_end_date = self._parse_date(end_date, "end_date")
        if normalized_start_date > normalized_end_date:
            raise ValueError(
                "start_date must be earlier than or equal to end_date"
            )

        with self.db.session() as session:
            repo = StockQuoteRepository(session)
            return [
                self._to_dict(quote)
                for quote in repo.get_by_date_range(
                    normalized_start_date,
                    normalized_end_date
                )
            ]

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

    def _to_entity(self, data: dict[str, Any]) -> StockQuote:
        """Convert a plain dictionary into a ``StockQuote`` entity."""

        normalized_data = self._normalize_create_data(data)
        return StockQuote(**normalized_data)

    def _to_dict(self, entity: StockQuote) -> dict[str, Any]:
        """Convert a ``StockQuote`` entity into a UI-safe dictionary."""

        return {
            "id": entity.id,
            "trade_date": entity.trade_date.isoformat(),
            "source": entity.source,
            "open_price": self._serialize_number(entity.open_price),
            "high_price": self._serialize_number(entity.high_price),
            "low_price": self._serialize_number(entity.low_price),
            "close_price": self._serialize_number(entity.close_price),
            "adj_close_price": self._serialize_optional_number(
                entity.adj_close_price
            ),
            "volume": int(entity.volume),
        }

    def _normalize_create_data(
            self,
            data: dict[str, Any]
    ) -> dict[str, Any]:
        """Normalize and validate a create payload."""

        self._ensure_dict(data)
        self._validate_known_fields(data)

        missing_fields = [
            field_name
            for field_name in sorted(self._REQUIRED_CREATE_FIELDS)
            if field_name not in data or self._is_blank(data[field_name])
        ]
        if missing_fields:
            joined_fields = ", ".join(missing_fields)
            raise ValueError(
                f"Missing required stock quote fields: {joined_fields}"
            )

        normalized_data = self._normalize_fields(data)
        normalized_data.setdefault("adj_close_price", None)
        return normalized_data

    def _normalize_update_data(
            self,
            data: dict[str, Any]
    ) -> dict[str, Any]:
        """Normalize and validate an update payload."""

        self._ensure_dict(data)
        self._validate_known_fields(data)
        return self._normalize_fields(data)

    def _normalize_fields(self, data: dict[str, Any]) -> dict[str, Any]:
        """Normalize supported stock quote fields from a payload."""

        normalized_data: dict[str, Any] = {}
        for field_name, value in data.items():
            if field_name == "id":
                continue
            if field_name == "trade_date":
                normalized_data[field_name] = self._parse_date(
                    value,
                    field_name
                )
            elif field_name == "source":
                normalized_data[field_name] = self._parse_source(value)
            elif field_name in self._PRICE_FIELDS:
                required = field_name != "adj_close_price"
                normalized_data[field_name] = self._parse_price(
                    value,
                    field_name,
                    required=required
                )
            elif field_name == "volume":
                normalized_data[field_name] = self._parse_volume(value)

        return normalized_data

    def _validate_known_fields(self, data: dict[str, Any]) -> None:
        """Reject unsupported fields before persistence."""

        allowed_fields = self._FIELD_NAMES | {"id"}
        unknown_fields = set(data) - allowed_fields
        if unknown_fields:
            joined_fields = ", ".join(sorted(unknown_fields))
            raise ValueError(f"Unknown stock quote fields: {joined_fields}")

    def _ensure_dict(self, data: dict[str, Any]) -> None:
        """Ensure GUI payloads are dictionaries."""

        if not isinstance(data, dict):
            raise TypeError("Stock quote payload must be a dictionary")

    def _parse_date(
            self,
            value: date | datetime | str,
            field_name: str
    ) -> date:
        """Parse a contract date value."""

        if self._is_blank(value):
            raise ValueError(f"{field_name} is required")
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            normalized_value = value.strip()
            if not self._DATE_PATTERN.fullmatch(normalized_value):
                raise ValueError(
                    f"{field_name} must use YYYY-MM-DD format"
                )
            try:
                return date.fromisoformat(normalized_value)
            except ValueError as exc:
                raise ValueError(
                    f"{field_name} must use YYYY-MM-DD format"
                ) from exc

        raise TypeError(f"{field_name} must be a date or YYYY-MM-DD string")

    def _parse_price(
            self,
            value: Any,
            field_name: str,
            *,
            required: bool
    ) -> float | None:
        """Parse and validate a non-negative price."""

        if self._is_blank(value):
            if required:
                raise ValueError(f"{field_name} is required")
            return None
        if isinstance(value, bool):
            raise TypeError(f"{field_name} must be a number")

        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise TypeError(f"{field_name} must be a number") from exc

        if not math.isfinite(number):
            raise ValueError(f"{field_name} must be a finite number")
        if number < 0:
            raise ValueError(f"{field_name} must not be negative")

        return number

    def _parse_volume(self, value: Any) -> int:
        """Parse and validate a non-negative volume."""

        if self._is_blank(value):
            raise ValueError("volume is required")
        if isinstance(value, bool):
            raise TypeError("volume must be an integer")
        if isinstance(value, Decimal):
            if not value.is_finite() or value != value.to_integral_value():
                raise ValueError("volume must be an integer")
            volume = int(value)
        elif isinstance(value, float):
            if not value.is_integer():
                raise ValueError("volume must be an integer")
            volume = int(value)
        else:
            try:
                volume = int(value)
            except (TypeError, ValueError) as exc:
                raise TypeError("volume must be an integer") from exc

        if volume < 0:
            raise ValueError("volume must not be negative")

        return volume

    def _parse_source(self, value: Any) -> str:
        """Parse and validate a unique source string."""

        if self._is_blank(value):
            raise ValueError("source is required")
        if not isinstance(value, str):
            raise TypeError("source must be a string")

        source = value.strip()
        if not source:
            raise ValueError("source is required")
        if len(source) > 512:
            raise ValueError("source must be 512 characters or fewer")

        return source

    def _ensure_source_available(
            self,
            repo: StockQuoteRepository,
            source: str,
            *,
            current_quote_id: int | None = None
    ) -> None:
        """Ensure a source does not duplicate another record."""

        existing_quote = repo.get_by_source(source)
        if existing_quote is None:
            return
        is_current_quote = (
                current_quote_id is not None
                and existing_quote.id == current_quote_id
        )
        if is_current_quote:
            return

        raise ValueError("source already exists")

    def _serialize_number(self, value: Decimal | float | int) -> float:
        """Serialize SQLAlchemy numeric values for the GUI."""

        return float(value)

    def _serialize_optional_number(
            self,
            value: Decimal | float | int | None
    ) -> float | None:
        """Serialize optional SQLAlchemy numeric values for the GUI."""

        if value is None:
            return None

        return float(value)

    def _is_blank(self, value: Any) -> bool:
        """Return whether a GUI field value is empty."""

        return (
                value is None
                or (isinstance(value, str) and value.strip() == "")
        )

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
