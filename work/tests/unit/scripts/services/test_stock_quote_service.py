"""Unit tests for StockQuoteService.

Test coverage includes:
- get_all_quotes_df returns correctly shaped DataFrame
- get_all_quotes returns list of dicts
- get_quote_by_id returns dict or None
- create_quote calls repository and returns dict
- delete_quote_by_id delegates to repository
- repository exception propagates from service
- data transformation: numeric fields are floats, volume is int
"""

import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pandas as pd

from work.scripts.db.models import StockQuote
from work.scripts.services.stock_quote_service import StockQuoteService


def _make_entity(
    *,
    id: int = 1,
    trade_date: date = date(2024, 1, 15),
    source: str = "yahoo/NVDA/2024-01-15",
    open_price: float = 100.0,
    high_price: float = 110.0,
    low_price: float = 90.0,
    close_price: float = 105.0,
    adj_close_price: float | None = 105.0,
    volume: int = 500_000,
) -> StockQuote:
    entity = StockQuote(
        trade_date=trade_date,
        source=source,
        open_price=Decimal(str(open_price)),
        high_price=Decimal(str(high_price)),
        low_price=Decimal(str(low_price)),
        close_price=Decimal(str(close_price)),
        adj_close_price=Decimal(str(adj_close_price)) if adj_close_price is not None else None,
        volume=volume,
    )
    entity.id = id
    return entity


def _make_service(entities: list[StockQuote]) -> StockQuoteService:
    """Build a StockQuoteService with a mocked database session."""

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = entities
    mock_repo.get_by_id.side_effect = lambda eid: next(
        (e for e in entities if e.id == eid), None
    )
    mock_repo.get_by_source.return_value = None

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        service._mock_repo = mock_repo
        service._mock_db = mock_db

    return service


# =========================================================
# get_all_quotes_df
# =========================================================

@pytest.mark.unit
def test_get_all_quotes_df_returns_dataframe() -> None:
    """get_all_quotes_df returns a DataFrame with correct columns."""

    entities = [_make_entity(id=1), _make_entity(id=2, source="yahoo/NVDA/2024-01-16")]

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = entities

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        df = service.get_all_quotes_df()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "close_price" in df.columns
    assert "trade_date" in df.columns


@pytest.mark.unit
def test_get_all_quotes_df_empty_when_no_records() -> None:
    """get_all_quotes_df returns empty DataFrame when repository is empty."""

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = []

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        df = service.get_all_quotes_df()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


# =========================================================
# get_all_quotes
# =========================================================

@pytest.mark.unit
def test_get_all_quotes_returns_list_of_dicts() -> None:
    """get_all_quotes returns list of plain dictionaries."""

    entities = [_make_entity(id=1)]

    mock_repo = MagicMock()
    mock_repo.get_all.return_value = entities

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.get_all_quotes()

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], dict)
    assert result[0]["source"] == "yahoo/NVDA/2024-01-15"


# =========================================================
# get_quote_by_id
# =========================================================

@pytest.mark.unit
def test_get_quote_by_id_returns_dict_when_found() -> None:
    """get_quote_by_id returns a dict for an existing id."""

    entity = _make_entity(id=42)

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = entity

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.get_quote_by_id(42)

    assert result is not None
    assert result["id"] == 42


@pytest.mark.unit
def test_get_quote_by_id_returns_none_when_missing() -> None:
    """get_quote_by_id returns None when id does not exist."""

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.get_quote_by_id(999)

    assert result is None


# =========================================================
# create_quote
# =========================================================

@pytest.mark.unit
def test_create_quote_returns_dict() -> None:
    """create_quote saves entity and returns serialized dict."""

    entity = _make_entity(id=7)

    mock_repo = MagicMock()
    mock_repo.get_by_source.return_value = None
    mock_repo.add.return_value = entity

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    payload = {
        "trade_date": "2024-01-15",
        "source": "yahoo/NVDA/2024-01-15",
        "open_price": 100.0,
        "high_price": 110.0,
        "low_price": 90.0,
        "close_price": 105.0,
        "volume": 500000,
    }

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.create_quote(payload)

    assert isinstance(result, dict)
    assert result["id"] == 7


# =========================================================
# delete_quote_by_id
# =========================================================

@pytest.mark.unit
def test_delete_quote_by_id_returns_true_when_deleted() -> None:
    """delete_quote_by_id returns True when repository reports success."""

    mock_repo = MagicMock()
    mock_repo.delete_by_id.return_value = True

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.delete_quote_by_id(1)

    assert result is True


@pytest.mark.unit
def test_delete_quote_by_id_returns_false_when_not_found() -> None:
    """delete_quote_by_id returns False when record does not exist."""

    mock_repo = MagicMock()
    mock_repo.delete_by_id.return_value = False

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.delete_quote_by_id(999)

    assert result is False


# =========================================================
# DATA TRANSFORMATION
# =========================================================

@pytest.mark.unit
def test_numeric_fields_are_floats_in_dict() -> None:
    """Serialized quote dict returns float prices and int volume."""

    entity = _make_entity(id=1, close_price=495.75, volume=1_234_567)

    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = entity

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        result = service.get_quote_by_id(1)

    assert isinstance(result["close_price"], float)
    assert isinstance(result["volume"], int)
    assert result["close_price"] == 495.75


# =========================================================
# EXCEPTION PROPAGATION
# =========================================================

@pytest.mark.unit
def test_repository_exception_propagates() -> None:
    """Exception raised in repository is not swallowed by service."""

    mock_repo = MagicMock()
    mock_repo.get_all.side_effect = RuntimeError("db down")

    mock_session = MagicMock()
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)

    mock_db = MagicMock()
    mock_db.session.return_value = mock_session

    service = StockQuoteService(mock_db)

    with patch(
        "work.scripts.services.stock_quote_service.StockQuoteRepository",
        return_value=mock_repo,
    ):
        with pytest.raises(RuntimeError, match="db down"):
            service.get_all_quotes()
