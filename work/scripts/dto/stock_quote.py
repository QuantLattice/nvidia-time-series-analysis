"""Data Transfer Objects (DTO) for stock quote operations.

This module defines structured data containers used to transfer stock
quote data between application layers (e.g., GUI, services, repositories).

DTOs decouple the external interface (GUI, CSV import) from the internal
ORM models, improving maintainability, validation, and flexibility.

DTO Types
---------
- StockQuoteCreateDTO : Used when creating new records
- StockQuoteUpdateDTO : Used for partial updates
- StockQuoteDTO       : Used for returning data to presentation layer
"""
from dataclasses import dataclass

from datetime import date
from typing import Optional


# ============================================================
# CREATE DTO
# ============================================================

@dataclass(slots=True)
class StockQuoteCreateDTO:
    """DTO for creating a new stock quote.

    This object represents validated input data coming from external
    sources such as GUI forms or CSV import pipelines.

    Parameters
    ----------
    trade_date : date
        Trading date of the record.
    source : str
        Data source identifier (e.g., file name, provider, or API).
    open_price : float
        Opening price for the trading day.
    high_price : float
        Highest price during the trading day.
    low_price : float
        Lowest price during the trading day.
    close_price : float
        Closing price for the trading day.
    volume : int
        Trading volume (number of shares).
    adj_close_price : float | None, optional
        Adjusted closing price accounting for corporate actions.

    Notes
    -----
    - All required fields must be provided.
    - This DTO is typically converted into an ORM entity before persistence.
    """

    trade_date: date
    source: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    adj_close_price: Optional[float] = None


# ============================================================
# UPDATE DTO
# ============================================================

@dataclass(slots=True)
class StockQuoteUpdateDTO:
    """DTO for partial update of an existing stock quote.

    This object allows updating only selected fields of a stock quote.
    Fields set to None are ignored during the update operation.

    Parameters
    ----------
    trade_date : date | None
    source : str | None
    open_price : float | None
    high_price : float | None
    low_price : float | None
    close_price : float | None
    adj_close_price : float | None
    volume : int | None

    Notes
    -----
    - Intended for PATCH-like updates.
    - Only non-None values should be applied to the database.
    """

    trade_date: Optional[date] = None
    source: Optional[str] = None
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    adj_close_price: Optional[float] = None
    volume: Optional[int] = None

    def to_dict(self) -> dict[str, object]:
        """Convert DTO to dictionary for update operations.

        Returns
        -------
        dict[str, object]
            Dictionary representation of fields.

        Notes
        -----
        - Includes all fields, including None values.
        - Filtering of None values should be handled
          at service/repository layer.
        """

        return {
            "trade_date": self.trade_date,
            "source": self.source,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "adj_close_price": self.adj_close_price,
            "volume": self.volume,
        }


# ============================================================
# READ DTO
# ============================================================

@dataclass(slots=True)
class StockQuoteDTO:
    """DTO representing a stock quote for output/presentation.

    This object is used to transfer data from the service layer to the
    presentation layer (e.g., GUI, reports).

    Parameters
    ----------
    id : int
        Unique identifier of the record.
    trade_date : date
        Trading date.
    source : str
        Data source identifier.
    open_price : float
    high_price : float
    low_price : float
    close_price : float
    adj_close_price : float | None
    volume : int

    Notes
    -----
    - This DTO is read-only and should not be used for persistence.
    - Typically constructed from ORM models.
    """

    id: int
    trade_date: date
    source: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    adj_close_price: Optional[float]
    volume: int
