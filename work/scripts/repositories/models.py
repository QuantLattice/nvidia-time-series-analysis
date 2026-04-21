"""Typed repository payloads for stock quote persistence."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class StockQuoteCreate:
    """Complete field set required to create a stock quote."""

    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    adj_close_price: float | None = None


@dataclass(slots=True)
class StockQuoteUpdate:
    """Partial field set for updating a stock quote."""

    trade_date: date | None = None
    open_price: float | None = None
    high_price: float | None = None
    low_price: float | None = None
    close_price: float | None = None
    adj_close_price: float | None = None
    volume: int | None = None

    def to_field_dict(self) -> dict[str, object]:
        """Return all update fields keyed by model column name."""

        return {
            "trade_date": self.trade_date,
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price,
            "adj_close_price": self.adj_close_price,
            "volume": self.volume,
        }
