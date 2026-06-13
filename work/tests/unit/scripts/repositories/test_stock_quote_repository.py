"""Unit tests for StockQuoteRepository.

This module validates CRUD operations of the repository layer.

Test coverage includes:
- single entity creation
- bulk insertion
- updates
- deletions
- query operations (by id, full scan, date filtering, pagination)
- count and date range queries

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


# =========================================================
# COUNT
# =========================================================

@pytest.mark.unit
def test_count_all_empty(db_session: Session) -> None:
    """count_all returns 0 when the table is empty."""
    repo = StockQuoteRepository(db_session)
    assert repo.count_all() == 0


@pytest.mark.unit
def test_count_all(db_session: Session) -> None:
    """count_all returns the correct number of inserted rows."""
    repo = StockQuoteRepository(db_session)
    entities = [StockQuoteFactory.create(), StockQuoteFactory.create()]
    repo.create_bulk(entities)
    db_session.commit()
    assert repo.count_all() == 2


# =========================================================
# DELETE ALL
# =========================================================

@pytest.mark.unit
def test_delete_all(db_session: Session) -> None:
    """delete_all removes every row from the table."""
    repo = StockQuoteRepository(db_session)
    repo.create_bulk([StockQuoteFactory.create(), StockQuoteFactory.create()])
    db_session.commit()

    repo.delete_all()
    db_session.commit()

    assert repo.count_all() == 0


# =========================================================
# PAGINATION
# =========================================================

@pytest.mark.unit
def test_get_page_returns_correct_slice(db_session: Session) -> None:
    """get_page returns the right number of rows for offset/limit."""
    repo = StockQuoteRepository(db_session)
    entities = [StockQuoteFactory.create() for _ in range(5)]
    repo.create_bulk(entities)
    db_session.commit()

    page = repo.get_page(offset=0, limit=3)
    assert len(page) == 3


@pytest.mark.unit
def test_get_page_offset(db_session: Session) -> None:
    """get_page with offset skips the right number of rows."""
    repo = StockQuoteRepository(db_session)
    entities = [StockQuoteFactory.create() for _ in range(4)]
    repo.create_bulk(entities)
    db_session.commit()

    page = repo.get_page(offset=3, limit=10)
    assert len(page) == 1


@pytest.mark.unit
def test_get_page_sort_desc(db_session: Session) -> None:
    """get_page with sort_desc=True returns rows in descending order."""
    repo = StockQuoteRepository(db_session)
    e1 = StockQuoteFactory.create(trade_date=date(2023, 1, 1))
    e2 = StockQuoteFactory.create(trade_date=date(2023, 6, 1))
    repo.create_bulk([e1, e2])
    db_session.commit()

    page = repo.get_page(
        offset=0, limit=10, sort_col='trade_date', sort_desc=True
    )
    dates = [r.trade_date for r in page]
    assert dates == sorted(dates, reverse=True)


# =========================================================
# DATE RANGE QUERY
# =========================================================

@pytest.mark.unit
def test_get_date_range_empty(db_session: Session) -> None:
    """get_date_range returns (None, None) when table is empty."""
    repo = StockQuoteRepository(db_session)
    min_d, max_d = repo.get_date_range()
    assert min_d is None
    assert max_d is None


@pytest.mark.unit
def test_get_date_range(db_session: Session) -> None:
    """get_date_range returns correct min and max dates."""
    repo = StockQuoteRepository(db_session)
    dates = [date(2023, 3, 1), date(2023, 1, 1), date(2023, 6, 15)]
    entities = [StockQuoteFactory.create(trade_date=d) for d in dates]
    repo.create_bulk(entities)
    db_session.commit()

    min_d, max_d = repo.get_date_range()
    assert min_d == date(2023, 1, 1)
    assert max_d == date(2023, 6, 15)


# =========================================================
# EDGE CASES
# =========================================================

@pytest.mark.unit
def test_get_by_id_not_found(db_session: Session) -> None:
    """get_by_id returns None for a non-existent id."""
    repo = StockQuoteRepository(db_session)
    assert repo.get_by_id(99999) is None


@pytest.mark.unit
def test_get_by_date_range_no_match(db_session: Session) -> None:
    """get_by_date_range returns empty list when no records match."""
    repo = StockQuoteRepository(db_session)
    entity = StockQuoteFactory.create(trade_date=date(2022, 1, 1))
    repo.create(entity)
    db_session.commit()

    result = repo.get_by_date_range(date(2023, 1, 1), date(2023, 12, 31))
    assert result == []
