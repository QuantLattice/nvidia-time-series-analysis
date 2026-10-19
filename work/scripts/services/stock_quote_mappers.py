"""Mapping helpers for stock quote data conversions.

This module provides pure functions for converting between
StockQuoteCreateDTO, StockQuote ORM entities, and pandas DataFrames.
It is intentionally free of business logic so that the conversions
can be tested and reused independently of the service layer.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd

from work.scripts.db.models import StockQuote
from work.scripts.contracts.schemas import StockQuoteSchema as S
from work.scripts.dto import StockQuoteCreateDTO, StockQuoteDTO
from typing import List


def to_entity(dto: StockQuoteCreateDTO) -> StockQuote:
    """Convert creation DTO into ORM entity.

    Parameters
    ----------
    dto : StockQuoteCreateDTO
        Input DTO with stock quote data.

    Returns
    -------
    StockQuote
        ORM entity ready for persistence.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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


def to_dto(entity: StockQuote) -> StockQuoteDTO:
    """Convert ORM entity into read DTO.

    Parameters
    ----------
    entity : StockQuote
        ORM entity loaded from the database.

    Returns
    -------
    StockQuoteDTO
        DTO suitable for presentation and API response layers.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    return StockQuoteDTO(
        id=entity.id,
        trade_date=entity.trade_date,
        source=entity.source,
        open_price=float(entity.open_price),
        high_price=float(entity.high_price),
        low_price=float(entity.low_price),
        close_price=float(entity.close_price),

        adj_close_price=float(entity.adj_close_price)
        if entity.adj_close_price is not None
        else None,

        volume=entity.volume,
    )


def to_dataframe(quotes: List[StockQuote]) -> pd.DataFrame:
    """Convert ORM entities to a pandas DataFrame.

    Parameters
    ----------
    quotes : list[StockQuote]
        List of ORM objects.

    Returns
    -------
    pd.DataFrame
        Tabular representation of stock quote data.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
