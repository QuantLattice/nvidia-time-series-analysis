"""Unit tests for stock quote mapper functions.

Covers to_entity, to_dto, and to_dataframe conversions.
"""
import pytest
from datetime import date

from work.scripts.dto import StockQuoteCreateDTO, StockQuoteDTO
from work.scripts.db.models import StockQuote
from work.scripts.services.stock_quote_mappers import (
    to_entity,
    to_dto,
    to_dataframe,
)


# =========================================================
# to_entity
# =========================================================

@pytest.mark.unit
def test_to_entity_basic_fields() -> None:
    """to_entity maps all DTO fields onto the ORM model."""
    dto = StockQuoteCreateDTO(
        trade_date=date(2024, 3, 15),
        source="csv-import",
        open_price=100.0,
        high_price=110.0,
        low_price=95.0,
        close_price=108.0,
        volume=5000,
        adj_close_price=107.5,
    )
    entity = to_entity(dto)

    assert isinstance(entity, StockQuote)
    assert entity.trade_date == date(2024, 3, 15)
    assert entity.source == "csv-import"
    assert entity.open_price == pytest.approx(100.0)
    assert entity.high_price == pytest.approx(110.0)
    assert entity.low_price == pytest.approx(95.0)
    assert entity.close_price == pytest.approx(108.0)
    assert entity.volume == 5000
    assert entity.adj_close_price == pytest.approx(107.5)


@pytest.mark.unit
def test_to_entity_none_adj_close() -> None:
    """to_entity preserves None for optional adj_close_price."""
    dto = StockQuoteCreateDTO(
        trade_date=date(2024, 1, 1),
        source="src",
        open_price=50.0,
        high_price=55.0,
        low_price=48.0,
        close_price=52.0,
        volume=1000,
        adj_close_price=None,
    )
    entity = to_entity(dto)
    assert entity.adj_close_price is None


# =========================================================
# to_dto
# =========================================================

@pytest.mark.unit
def test_to_dto_basic_fields() -> None:
    """to_dto maps all ORM entity fields onto the DTO."""
    entity = StockQuote(
        id=42,
        trade_date=date(2024, 5, 10),
        source="api",
        open_price=200.0,
        high_price=210.0,
        low_price=195.0,
        close_price=205.0,
        adj_close_price=204.0,
        volume=12000,
    )
    dto = to_dto(entity)

    assert isinstance(dto, StockQuoteDTO)
    assert dto.id == 42
    assert dto.trade_date == date(2024, 5, 10)
    assert dto.source == "api"
    assert dto.open_price == pytest.approx(200.0)
    assert dto.close_price == pytest.approx(205.0)
    assert dto.volume == 12000


@pytest.mark.unit
def test_to_dto_none_adj_close() -> None:
    """to_dto preserves None for optional adj_close_price."""
    entity = StockQuote(
        id=1,
        trade_date=date(2024, 1, 1),
        source="s",
        open_price=10.0,
        high_price=11.0,
        low_price=9.0,
        close_price=10.5,
        adj_close_price=None,
        volume=100,
    )
    assert to_dto(entity).adj_close_price is None


# =========================================================
# to_dataframe
# =========================================================

@pytest.mark.unit
def test_to_dataframe_columns() -> None:
    """to_dataframe produces a DataFrame with the expected columns."""
    entity = StockQuote(
        id=1,
        trade_date=date(2024, 1, 1),
        source="s",
        open_price=10.0,
        high_price=11.0,
        low_price=9.0,
        close_price=10.5,
        adj_close_price=10.5,
        volume=100,
    )
    df = to_dataframe([entity])

    expected_cols = {
        'trade_date', 'source',
        'open_price', 'high_price', 'low_price',
        'close_price', 'adj_close_price', 'volume',
    }
    assert expected_cols.issubset(set(df.columns))


@pytest.mark.unit
def test_to_dataframe_row_count() -> None:
    """to_dataframe returns one row per entity."""
    entities = [
        StockQuote(
            id=i, trade_date=date(2024, 1, i),
            source="s", open_price=10.0, high_price=11.0,
            low_price=9.0, close_price=10.5,
            adj_close_price=None, volume=100,
        )
        for i in range(1, 4)
    ]
    df = to_dataframe(entities)
    assert len(df) == 3


@pytest.mark.unit
def test_to_dataframe_empty() -> None:
    """to_dataframe on empty list returns an empty DataFrame."""
    df = to_dataframe([])
    assert len(df) == 0
