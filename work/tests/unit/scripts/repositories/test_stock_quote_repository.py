"""Unit tests for StockQuoteRepository.

This module validates CRUD operations of the repository layer.

Test coverage includes:
- single entity creation
- bulk insertion
- updates
- deletions
- query operations (by id, full scan, date filtering)

All tests use an isolated in-memory SQLite database.
"""


import pytest
from datetime import date

from work.scripts.repositories import StockQuoteRepository
from work.tests.factories import StockQuoteFactory

from sqlalchemy.orm import Session


# =========================================================
# CREATE
# =========================================================

@pytest.mark.unit
def test_create_single(db_session: Session) -> None:
    """Test insertion of a single StockQuote entity."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create()

    repo.create(entity)
    db_session.commit()

    result = repo.get_all()

    assert len(result) == 1
    assert result[0].source == entity.source


@pytest.mark.unit
def test_create_bulk(db_session: Session) -> None:
    """Test bulk insertion of multiple StockQuote entities."""

    repo = StockQuoteRepository(db_session)

    entities = [
        StockQuoteFactory.create(),
        StockQuoteFactory.create(adj_close_price=None)
    ]

    repo.create_bulk(entities)
    db_session.commit()

    result = repo.get_all()

    assert len(result) == len(entities)
    assert any(
        e.adj_close_price == entities[0].adj_close_price
        for e in result
    )
    assert any(
        e.adj_close_price == entities[1].adj_close_price
        for e in result
    )


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.unit
def test_update(db_session: Session) -> None:
    """Test update operation for existing entity."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create(source="old")
    repo.create(entity)
    db_session.commit()

    entity.source = "updated"
    repo.update(entity)
    db_session.commit()

    result = repo.get_by_id(entity.id)

    if result is not None:
        assert result.source == entity.source


# =========================================================
# DELETE
# =========================================================

@pytest.mark.unit
def test_delete(db_session: Session) -> None:
    """Test deletion of an entity."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create()
    repo.create(entity)
    db_session.commit()

    repo.delete(entity)
    db_session.commit()

    result = repo.get_all()

    assert len(result) == 0


# =========================================================
# READ
# =========================================================

@pytest.mark.unit
def test_get_by_id(db_session: Session) -> None:
    """Test retrieval of entity by primary key."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create()
    repo.create(entity)
    db_session.commit()

    found = repo.get_by_id(entity.id)

    assert found is not None
    assert found.source == entity.source


@pytest.mark.unit
def test_get_all(db_session: Session) -> None:
    """Test retrieval of all entities."""

    repo = StockQuoteRepository(db_session)

    entities = [
        StockQuoteFactory.create(source="a"),
        StockQuoteFactory.create(source="b")
    ]
    repo.create_bulk(entities)
    db_session.commit()

    result = repo.get_all()

    assert len(result) == len(entities)
    assert any(e.source == entities[0].source for e in result)
    assert any(e.source == entities[1].source for e in result)


@pytest.mark.unit
def test_get_by_date_range(db_session: Session) -> None:
    """Test filtering entities by trade date range."""

    repo = StockQuoteRepository(db_session)

    entities = [
        StockQuoteFactory.create(trade_date=date(2024, 1, 1)),
        StockQuoteFactory.create(trade_date=date(2024, 1, 11)),
        StockQuoteFactory.create(trade_date=date(2024, 1, 21)),
    ]
    repo.create_bulk(entities)
    db_session.commit()

    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 15)
    expected = [
        e for e in entities
        if start_date <= e.trade_date <= end_date
    ]

    result = repo.get_by_date_range(start_date, end_date)

    assert len(result) == len(expected)
