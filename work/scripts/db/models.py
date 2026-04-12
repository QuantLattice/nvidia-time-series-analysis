"""Defines database models and schema for stock market time-series data."""
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StockQuote(Base):
    __tablename__ = "stock_quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    open_price: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    high_price: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    low_price: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    close_price: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)
    adj_close_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 4), nullable=True)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
