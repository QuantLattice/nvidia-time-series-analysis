"""Unit tests for StockQuoteRepository — mocked SQLAlchemy session.

Each test constructs a repository with a MagicMock session and verifies
that the correct session methods are called with the correct arguments.
No real database connection is required.

Test coverage:
- add: session.add called, entity returned
- bulk_add: session.add_all called
- update: session.merge called
- delete: session.delete called
- delete_by_id: returns True when found, False when not found
- get_by_id: delegates to session.get
- get_all: delegates to session.query().all()
- get_by_date_range: delegates to session.query().filter().all()
"""

import pytest
from datetime import date
from unittest.mock import MagicMock, call

from work.scripts.repositories import StockQuoteRepository
from work.tests.factories import StockQuoteFactory


def _repo() -> tuple[StockQuoteRepository, MagicMock]:
    session = MagicMock()
    return StockQuoteRepository(session), session


# =========================================================
# ADD
# =========================================================

@pytest.mark.unit
def test_create_single() -> None:
    """add() calls session.add and returns the entity."""

    repo, session = _repo()
    entity = StockQuoteFactory.create(source="test/create-single")

    result = repo.add(entity)

    session.add.assert_called_once_with(entity)
    assert result is entity


# =========================================================
# BULK ADD
# =========================================================

@pytest.mark.unit
def test_create_bulk() -> None:
    """bulk_add() calls session.add_all with the full list."""

    repo, session = _repo()
    entities = [
        StockQuoteFactory.create(source="test/bulk-1"),
        StockQuoteFactory.create(source="test/bulk-2", adj_close_price=None),
    ]

    repo.bulk_add(entities)

    session.add_all.assert_called_once_with(entities)


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.unit
def test_update() -> None:
    """update() calls session.merge with the entity."""

    repo, session = _repo()
    entity = StockQuoteFactory.create(source="test/update-old")
    entity.source = "test/update-new"

    repo.update(entity)

    session.merge.assert_called_once_with(entity)


# =========================================================
# DELETE
# =========================================================

@pytest.mark.unit
def test_delete() -> None:
    """delete() calls session.delete with the entity."""

    repo, session = _repo()
    entity = StockQuoteFactory.create(source="test/to-delete")

    repo.delete(entity)

    session.delete.assert_called_once_with(entity)


# =========================================================
# DELETE BY ID
# =========================================================

@pytest.mark.unit
def test_delete_by_id_found() -> None:
    """delete_by_id returns True and calls session.delete when entity exists."""

    repo, session = _repo()
    entity = StockQuoteFactory.create(source="test/del-by-id")
    session.get.return_value = entity

    result = repo.delete_by_id(1)

    assert result is True
    session.delete.assert_called_once_with(entity)


@pytest.mark.unit
def test_delete_by_id_not_found() -> None:
    """delete_by_id returns False and does not call session.delete when entity is missing."""

    repo, session = _repo()
    session.get.return_value = None

    result = repo.delete_by_id(999)

    assert result is False
    session.delete.assert_not_called()


# =========================================================
# GET BY ID
# =========================================================

@pytest.mark.unit
def test_get_by_id() -> None:
    """get_by_id returns the entity from session.get."""

    repo, session = _repo()
    entity = StockQuoteFactory.create(source="test/by-id")
    session.get.return_value = entity

    found = repo.get_by_id(42)

    assert found is entity


@pytest.mark.unit
def test_get_by_id_missing() -> None:
    """get_by_id returns None when session.get returns None."""

    repo, session = _repo()
    session.get.return_value = None

    assert repo.get_by_id(999) is None


# =========================================================
# GET ALL
# =========================================================

@pytest.mark.unit
def test_get_all() -> None:
    """get_all returns the list from session.query().all()."""

    repo, session = _repo()
    entities = [
        StockQuoteFactory.create(source="test/all-a"),
        StockQuoteFactory.create(source="test/all-b"),
    ]
    session.query.return_value.all.return_value = entities

    result = repo.get_all()

    assert result == entities
    sources = {e.source for e in result}
    assert "test/all-a" in sources
    assert "test/all-b" in sources


# =========================================================
# GET BY DATE RANGE
# =========================================================

@pytest.mark.unit
def test_get_by_date_range() -> None:
    """get_by_date_range returns only entities whose date falls in range."""

    repo, session = _repo()
    inside = [
        StockQuoteFactory.create(source="test/range-1", trade_date=date(2000, 1, 1)),
        StockQuoteFactory.create(source="test/range-2", trade_date=date(2000, 1, 11)),
    ]
    session.query.return_value.filter.return_value.all.return_value = inside

    result = repo.get_by_date_range(date(2000, 1, 1), date(2000, 1, 15))

    sources = {e.source for e in result}
    assert "test/range-1" in sources
    assert "test/range-2" in sources
    assert "test/range-3" not in sources
