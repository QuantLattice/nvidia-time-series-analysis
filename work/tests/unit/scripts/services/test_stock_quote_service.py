"""Unit tests for StockQuoteService.

Uses the shared in-memory SQLite session from conftest.
The Database dependency is replaced with a thin context-manager
stub that yields the test session.
"""
import pytest
from contextlib import contextmanager
from datetime import date
from unittest.mock import MagicMock

from work.scripts.dto import StockQuoteCreateDTO, StockQuoteUpdateDTO
from work.scripts.services.stock_quote_service import StockQuoteService
from work.tests.factories import StockQuoteFactory
from sqlalchemy.orm import Session


def make_service(db_session: Session) -> StockQuoteService:
    """Build a StockQuoteService wired to the test session.

    Flushes after each context-manager exit so that pending inserts/deletes
    are visible to subsequent queries within the same session.
    """
    db = MagicMock()

    @contextmanager
    def _session():
        yield db_session
        db_session.flush()

    db.session = _session
    return StockQuoteService(db=db)


def _create_dto(**overrides) -> StockQuoteCreateDTO:
    entity = StockQuoteFactory.create(**overrides)
    return StockQuoteCreateDTO(
        trade_date=entity.trade_date,
        source=entity.source,
        open_price=float(entity.open_price),
        high_price=float(entity.high_price),
        low_price=float(entity.low_price),
        close_price=float(entity.close_price),
        volume=int(entity.volume),
        adj_close_price=(
            float(entity.adj_close_price)
            if entity.adj_close_price is not None else None
        ),
    )


# =========================================================
# CREATE
# =========================================================

@pytest.mark.unit
def test_service_create_returns_dto(db_session: Session) -> None:
    """create_quote returns a DTO with correct field values."""
    service = make_service(db_session)
    dto = _create_dto()
    result = service.create_quote(dto)

    assert result.trade_date == dto.trade_date
    assert result.source == dto.source
    assert result.close_price == pytest.approx(dto.close_price)


@pytest.mark.unit
def test_service_create_bulk(db_session: Session) -> None:
    """create_quote_bulk inserts all records without errors."""
    service = make_service(db_session)
    dtos = [_create_dto(), _create_dto()]
    service.create_quote_bulk(dtos)

    all_quotes = service.get_all_quotes()
    assert len(all_quotes) >= 2


# =========================================================
# READ
# =========================================================

@pytest.mark.unit
def test_service_get_all(db_session: Session) -> None:
    """get_all_quotes returns all inserted records."""
    service = make_service(db_session)
    service.create_quote(_create_dto())
    service.create_quote(_create_dto())

    result = service.get_all_quotes()
    assert len(result) >= 2


@pytest.mark.unit
def test_service_get_by_id(db_session: Session) -> None:
    """get_quote_by_id returns the correct record."""
    service = make_service(db_session)
    created = service.create_quote(_create_dto())

    found = service.get_quote_by_id(created.id)
    assert found is not None
    assert found.id == created.id
    assert found.trade_date == created.trade_date


@pytest.mark.unit
def test_service_get_by_id_missing(db_session: Session) -> None:
    """get_quote_by_id returns None for non-existent id."""
    service = make_service(db_session)
    assert service.get_quote_by_id(99999) is None


@pytest.mark.unit
def test_service_get_quotes_page(db_session: Session) -> None:
    """get_quotes_page returns paginated results."""
    service = make_service(db_session)
    for _ in range(5):
        service.create_quote(_create_dto())

    quotes, total = service.get_quotes_page(page=1, page_size=3)
    assert len(quotes) <= 3
    assert total >= 5


@pytest.mark.unit
def test_service_get_by_date_range(db_session: Session) -> None:
    """get_quotes_by_date_range filters records correctly."""
    service = make_service(db_session)
    service.create_quote(_create_dto(trade_date=date(2021, 1, 1)))
    service.create_quote(_create_dto(trade_date=date(2021, 6, 1)))
    service.create_quote(_create_dto(trade_date=date(2022, 1, 1)))

    result = service.get_quotes_by_date_range(
        date(2021, 1, 1), date(2021, 12, 31)
    )
    assert all(
        date(2021, 1, 1) <= q.trade_date <= date(2021, 12, 31)
        for q in result
    )
    assert len(result) >= 2


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.unit
def test_service_update(db_session: Session) -> None:
    """update_quote_by_id changes the specified field."""
    service = make_service(db_session)
    created = service.create_quote(_create_dto())

    update_dto = StockQuoteUpdateDTO(source="updated-source")
    updated = service.update_quote_by_id(created.id, update_dto)

    assert updated is not None
    assert updated.source == "updated-source"


@pytest.mark.unit
def test_service_update_not_found(db_session: Session) -> None:
    """update_quote_by_id returns None for non-existent id."""
    service = make_service(db_session)
    result = service.update_quote_by_id(
        99999, StockQuoteUpdateDTO(source="x")
    )
    assert result is None


@pytest.mark.unit
def test_service_update_empty_raises(db_session: Session) -> None:
    """update_quote_by_id raises ValueError when no fields provided."""
    service = make_service(db_session)
    created = service.create_quote(_create_dto())

    with pytest.raises(ValueError):
        service.update_quote_by_id(created.id, StockQuoteUpdateDTO())


# =========================================================
# DELETE
# =========================================================

@pytest.mark.unit
def test_service_delete(db_session: Session) -> None:
    """delete_quote_by_id removes the record and returns True."""
    service = make_service(db_session)
    created = service.create_quote(_create_dto())

    deleted = service.delete_quote_by_id(created.id)
    assert deleted is True
    assert service.get_quote_by_id(created.id) is None


@pytest.mark.unit
def test_service_delete_not_found(db_session: Session) -> None:
    """delete_quote_by_id returns False when record does not exist."""
    service = make_service(db_session)
    assert service.delete_quote_by_id(99999) is False


@pytest.mark.unit
def test_service_delete_all(db_session: Session) -> None:
    """delete_all_quotes removes every record and returns count."""
    service = make_service(db_session)
    service.create_quote_bulk([_create_dto(), _create_dto()])

    count = service.delete_all_quotes()
    assert count >= 2
    assert service.get_all_quotes() == []


# =========================================================
# DATAFRAME
# =========================================================

@pytest.mark.unit
def test_service_get_all_quotes_df(db_session: Session) -> None:
    """get_all_quotes_df returns a non-empty DataFrame."""
    service = make_service(db_session)
    service.create_quote(_create_dto())

    df = service.get_all_quotes_df()
    assert len(df) >= 1
    assert 'close_price' in df.columns


@pytest.mark.unit
def test_service_get_quotes_by_date_range_df(db_session: Session) -> None:
    """get_quotes_by_date_range_df filters by date correctly."""
    service = make_service(db_session)
    service.create_quote(_create_dto(trade_date=date(2019, 1, 1)))
    service.create_quote(_create_dto(trade_date=date(2019, 7, 1)))
    service.create_quote(_create_dto(trade_date=date(2020, 1, 1)))

    df = service.get_quotes_by_date_range_df(
        date(2019, 1, 1), date(2019, 12, 31)
    )
    assert len(df) >= 2
    assert all(df['trade_date'] <= date(2019, 12, 31))
