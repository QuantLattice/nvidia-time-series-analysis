"""Unit tests for StockQuoteController.

The service layer is mocked so these tests exercise controller logic
(input parsing, error wrapping, result formatting) without a database.
"""
import pytest
from datetime import date
from unittest.mock import MagicMock

from work.scripts.controllers import StockQuoteController
from work.scripts.dto import StockQuoteDTO


def _dto(id_=1, trade_date=date(2024, 1, 1)) -> StockQuoteDTO:
    return StockQuoteDTO(
        id=id_,
        trade_date=trade_date,
        source="src",
        open_price=100.0,
        high_price=110.0,
        low_price=90.0,
        close_price=105.0,
        adj_close_price=105.0,
        volume=1000,
    )


def make_controller(**service_attrs) -> StockQuoteController:
    service = MagicMock()
    for k, v in service_attrs.items():
        setattr(service, k, v)
    return StockQuoteController(service=service)


# =========================================================
# get_quote_by_id
# =========================================================

@pytest.mark.unit
def test_get_quote_by_id_success() -> None:
    """Returns success dict with quote data when found."""
    svc = MagicMock()
    svc.get_quote_by_id.return_value = _dto()
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_quote_by_id(1)

    assert result['success'] is True
    assert result['data']['id'] == 1


@pytest.mark.unit
def test_get_quote_by_id_not_found() -> None:
    """Returns success=False when service raises ValueError."""
    svc = MagicMock()
    svc.get_quote_by_id.return_value = None
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_quote_by_id(99999)
    assert result['success'] is False


@pytest.mark.unit
def test_get_quote_by_id_string_id() -> None:
    """Accepts string id and converts it to int."""
    svc = MagicMock()
    svc.get_quote_by_id.return_value = _dto(id_=7)
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_quote_by_id("7")
    assert result['success'] is True


@pytest.mark.unit
def test_get_quote_by_id_invalid_id() -> None:
    """Returns success=False for non-numeric string id."""
    ctrl = make_controller()
    result = ctrl.get_quote_by_id("not-a-number")
    assert result['success'] is False


# =========================================================
# get_quotes_page
# =========================================================

@pytest.mark.unit
def test_get_quotes_page_success() -> None:
    """Returns paginated data with correct metadata."""
    svc = MagicMock()
    svc.get_quotes_page.return_value = ([_dto(), _dto(id_=2)], 10)
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_quotes_page(page=1, page_size=2)

    assert result['success'] is True
    data = result['data']
    assert data['page'] == 1
    assert data['page_size'] == 2
    assert data['total_rows'] == 10
    assert data['total_pages'] == 5
    assert len(data['items']) == 2


@pytest.mark.unit
def test_get_quotes_page_invalid_page() -> None:
    """Returns failure for page=0."""
    ctrl = make_controller()
    result = ctrl.get_quotes_page(page=0, page_size=10)
    assert result['success'] is False


@pytest.mark.unit
def test_get_quotes_page_invalid_size() -> None:
    """Returns failure for page_size=0."""
    ctrl = make_controller()
    result = ctrl.get_quotes_page(page=1, page_size=0)
    assert result['success'] is False


# =========================================================
# get_date_range
# =========================================================

@pytest.mark.unit
def test_get_date_range_success() -> None:
    """Returns min and max dates when data exists."""
    svc = MagicMock()
    svc.get_date_range.return_value = (date(2022, 1, 1), date(2023, 12, 31))
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_date_range()

    assert result['success'] is True
    assert result['data']['min_date'] == date(2022, 1, 1)
    assert result['data']['max_date'] == date(2023, 12, 31)


# =========================================================
# delete_quote_by_id
# =========================================================

@pytest.mark.unit
def test_delete_quote_success() -> None:
    """Returns success=True when service confirms deletion."""
    svc = MagicMock()
    svc.delete_quote_by_id.return_value = True
    ctrl = StockQuoteController(service=svc)

    result = ctrl.delete_quote_by_id(1)
    assert result['success'] is True


@pytest.mark.unit
def test_delete_quote_not_found() -> None:
    """Returns success=False when service reports not found."""
    svc = MagicMock()
    svc.delete_quote_by_id.return_value = False
    ctrl = StockQuoteController(service=svc)

    result = ctrl.delete_quote_by_id(999)
    assert result['success'] is False


# =========================================================
# delete_all_quotes
# =========================================================

@pytest.mark.unit
def test_delete_all_quotes() -> None:
    """Returns success=True with deleted count."""
    svc = MagicMock()
    svc.delete_all_quotes.return_value = 42
    ctrl = StockQuoteController(service=svc)

    result = ctrl.delete_all_quotes()
    assert result['success'] is True
    assert result['data']['deleted'] == 42


# =========================================================
# get_quotes_by_date_range
# =========================================================

@pytest.mark.unit
def test_get_quotes_by_date_range() -> None:
    """Returns a list of quote dicts filtered by date range."""
    svc = MagicMock()
    svc.get_quotes_by_date_range.return_value = [_dto(), _dto(id_=2)]
    ctrl = StockQuoteController(service=svc)

    result = ctrl.get_quotes_by_date_range(date(2024, 1, 1), date(2024, 6, 1))
    assert result['success'] is True
    assert len(result['data']) == 2
