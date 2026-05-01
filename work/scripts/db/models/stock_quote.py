"""ORM model for stock price data.

This module defines the StockQuote model, which represents historical
financial time series data for a stock (e.g., NVIDIA).
"""

from datetime import date

from sqlalchemy import Date, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from work.scripts.db.base import Base


class StockQuote(Base):
    """Stock price record for a single trading day.

    This model stores OHLC (Open, High, Low, Close) data along with trading
    volume and adjusted close price.

    Attributes
    ----------
    id : int
        Unique identifier of the record.
    trade_date : date
        Trading date of the record.
    source : str
        The source from which the share was added
    open_price : float
        Opening price.
    high_price : float
        Highest price during the trading day.
    low_price : float
        Lowest price during the trading day.
    close_price : float
        Closing price.
    adj_close_price : float | None
        Adjusted closing price (may be None).
    volume : int
        Trading volume.
    """

    __tablename__ = "stock_quotes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    trade_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        unique=False
    )

    source: Mapped[str] = mapped_column(
        String(length=512),
        nullable=False,
        unique=False
    )

    open_price: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=False
    )
    high_price: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=False
    )
    low_price: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=False
    )
    close_price: Mapped[float] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=False
    )

    adj_close_price: Mapped[float | None] = mapped_column(
        Numeric(precision=10, scale=4),
        nullable=True
    )

    volume: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
