"""Unit tests for StockQuoteRepository.

This module validates CRUD operations of the repository layer against
the real MySQL database. Each test runs inside a transaction that is
rolled back on teardown, so no test data persists.

Because the table contains real NVDA data (1 257 rows), assertions check
for the presence or absence of specific test entities by source rather
than relying on total row counts.

Test coverage includes:
- single entity creation
- bulk insertion
- updates
- deletions
- query operations (by id, full scan, date filtering)
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
    """Inserted entity is retrievable via get_all."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create(source="test/create-single")
    repo.add(entity)
    db_session.commit()

    sources = {r.source for r in repo.get_all()}

    assert "test/create-single" in sources


@pytest.mark.unit
def test_create_bulk(db_session: Session) -> None:
    """All bulk-inserted entities are retrievable via get_all."""

    repo = StockQuoteRepository(db_session)

    entities = [
        StockQuoteFactory.create(source="test/bulk-1"),
        StockQuoteFactory.create(source="test/bulk-2", adj_close_price=None),
    ]
    repo.bulk_add(entities)
    db_session.commit()

    sources = {r.source for r in repo.get_all()}

    assert "test/bulk-1" in sources
    assert "test/bulk-2" in sources


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.unit
def test_update(db_session: Session) -> None:
    """Updated source value is reflected on the next read."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create(source="test/update-old")
    repo.add(entity)
    db_session.commit()

    entity.source = "test/update-new"
    repo.update(entity)
    db_session.commit()

    found = repo.get_by_id(entity.id)

    assert found is not None
    assert found.source == "test/update-new"


# =========================================================
# DELETE
# =========================================================

@pytest.mark.unit
def test_delete(db_session: Session) -> None:
    """Deleted entity is no longer returned by get_all."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create(source="test/to-delete")
    repo.add(entity)
    db_session.commit()

    repo.delete(entity)
    db_session.commit()

    sources = {r.source for r in repo.get_all()}

    assert "test/to-delete" not in sources


# =========================================================
# READ
# =========================================================

@pytest.mark.unit
def test_get_by_id(db_session: Session) -> None:
    """Entity is retrievable by its primary key."""

    repo = StockQuoteRepository(db_session)

    entity = StockQuoteFactory.create(source="test/by-id")
    repo.add(entity)
    db_session.commit()

    found = repo.get_by_id(entity.id)

    assert found is not None
    assert found.source == "test/by-id"


@pytest.mark.unit
def test_get_all(db_session: Session) -> None:
    """Both bulk-inserted sources appear in the full result set."""

    repo = StockQuoteRepository(db_session)

    repo.bulk_add([
        StockQuoteFactory.create(source="test/all-a"),
        StockQuoteFactory.create(source="test/all-b"),
    ])
    db_session.commit()

    sources = {r.source for r in repo.get_all()}

    assert "test/all-a" in sources
    assert "test/all-b" in sources


@pytest.mark.unit
def test_get_by_date_range(db_session: Session) -> None:
    """Only entities whose trade_date falls inside the range are returned.

    Uses year-2000 dates — no real NVDA data exists there, so the result
    contains exactly the rows inserted by this test.
    """

    repo = StockQuoteRepository(db_session)

    inside = [
        StockQuoteFactory.create(source="test/range-1", trade_date=date(2000, 1, 1)),
        StockQuoteFactory.create(source="test/range-2", trade_date=date(2000, 1, 11)),
    ]
    outside = StockQuoteFactory.create(source="test/range-3", trade_date=date(2000, 1, 21))

    repo.bulk_add(inside + [outside])
    db_session.commit()

    result_sources = {
        r.source
        for r in repo.get_by_date_range(date(2000, 1, 1), date(2000, 1, 15))
    }

    assert "test/range-1" in result_sources
    assert "test/range-2" in result_sources
    assert "test/range-3" not in result_sources
