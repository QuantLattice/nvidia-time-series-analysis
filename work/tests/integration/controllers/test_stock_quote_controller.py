"""Database-backed tests for StockQuoteController."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest

from work.scripts.controllers.stock_quote_controller import (
    StockQuoteController,
)
from work.tests.fixtures.controller import (
    TEST_DATE_PREFIX,
    create_quote,
    quote_payload,
)


@pytest.mark.integration
def test_create_quote_success(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Create a quote in the real database through the controller."""

    payload = quote_payload(day=1)

    result = controller.create_quote(payload)

    assert result["success"] is True
    assert result["error"] is None
    assert result["data"]["id"] > 0
    assert result["data"]["trade_date"] == payload["trade_date"]
    assert result["data"]["source"] == payload["source"]
    assert result["data"]["close_price"] == payload["close_price"]

    created_quote_ids.append(result["data"]["id"])


@pytest.mark.integration
def test_create_quote_duplicate_source_error(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Reject a second real database row with the same source."""

    payload = quote_payload(day=2)
    first_result = controller.create_quote(payload)
    assert first_result["success"] is True, first_result
    created_quote_ids.append(first_result["data"]["id"])

    duplicate_payload = {
        **quote_payload(day=3),
        "source": payload["source"],
    }

    result = controller.create_quote(duplicate_payload)

    assert result == {
        "success": False,
        "data": None,
        "error": "source already exists",
    }


@pytest.mark.integration
def test_create_quote_allows_duplicate_trade_date_with_unique_source(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Create two real rows for one date when sources are unique."""

    payload = quote_payload(day=4)
    first_result = controller.create_quote(payload)
    assert first_result["success"] is True, first_result
    created_quote_ids.append(first_result["data"]["id"])

    duplicate_payload = {
        **quote_payload(day=4),
        "source": f"https://example.com/tests/nvda/duplicate/{uuid4().hex}",
    }

    result = controller.create_quote(duplicate_payload)

    assert result["success"] is True
    assert result["error"] is None
    assert result["data"]["trade_date"] == payload["trade_date"]
    assert result["data"]["source"] == duplicate_payload["source"]
    created_quote_ids.append(result["data"]["id"])


@pytest.mark.integration
def test_update_quote_by_id_success(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Update a real database row through the controller."""

    quote = create_quote(controller, created_quote_ids, day=5)
    new_source = f"https://example.com/tests/nvda/updated/{uuid4().hex}"

    result = controller.update_quote_by_id(
        str(quote["id"]),
        {
            "source": new_source,
            "close_price": 901.25,
        },
    )

    assert result["success"] is True
    assert result["error"] is None
    assert result["data"]["id"] == quote["id"]
    assert result["data"]["source"] == new_source
    assert result["data"]["close_price"] == 901.25


@pytest.mark.integration
def test_update_quote_by_id_duplicate_source_error(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Reject updating a real row to another row's source."""

    first_quote = create_quote(controller, created_quote_ids, day=6)
    second_quote = create_quote(controller, created_quote_ids, day=7)

    result = controller.update_quote_by_id(
        second_quote["id"],
        {"source": first_quote["source"]},
    )

    assert result == {
        "success": False,
        "data": None,
        "error": "source already exists",
    }


@pytest.mark.integration
def test_update_quote_by_id_not_found(
    controller: StockQuoteController,
) -> None:
    """Return a failed result when update target is missing."""

    result = controller.update_quote_by_id(999999999, {"close_price": 900.0})

    assert result == {
        "success": False,
        "data": None,
        "error": "Stock quote was not found",
    }


@pytest.mark.integration
@pytest.mark.parametrize("quote_id", ["abc", True, None])
def test_update_quote_by_id_invalid_id_type(
    controller: StockQuoteController,
    quote_id: Any,
) -> None:
    """Reject ids that cannot be parsed as integers."""

    result = controller.update_quote_by_id(quote_id, {"close_price": 900.0})

    assert result == {
        "success": False,
        "data": None,
        "error": "quote_id must be an integer",
    }


@pytest.mark.integration
@pytest.mark.parametrize("quote_id", [0, "-1"])
def test_update_quote_by_id_non_positive_id(
    controller: StockQuoteController,
    quote_id: int | str,
) -> None:
    """Reject non-positive ids."""

    result = controller.update_quote_by_id(quote_id, {"close_price": 900.0})

    assert result == {
        "success": False,
        "data": None,
        "error": "quote_id must be positive",
    }


@pytest.mark.integration
def test_delete_quote_by_id_success(
    controller: StockQuoteController,
) -> None:
    """Delete a real database row through the controller."""

    created_ids: list[int] = []
    quote = create_quote(controller, created_ids, day=8)

    result = controller.delete_quote_by_id(str(quote["id"]))

    assert result == {
        "success": True,
        "data": {"deleted": True},
        "error": None,
    }
    assert controller.get_quote_by_id(quote["id"]) == {
        "success": False,
        "data": None,
        "error": "Stock quote was not found",
    }


@pytest.mark.integration
def test_delete_quote_by_id_not_found(
    controller: StockQuoteController,
) -> None:
    """Return a failed result when delete target is missing."""

    result = controller.delete_quote_by_id(999999999)

    assert result == {
        "success": False,
        "data": None,
        "error": "Stock quote was not found",
    }


@pytest.mark.integration
def test_get_quote_by_id_success(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Read a real database row through the controller."""

    quote = create_quote(controller, created_quote_ids, day=9)

    result = controller.get_quote_by_id(str(quote["id"]))

    assert result == {
        "success": True,
        "data": quote,
        "error": None,
    }


@pytest.mark.integration
def test_get_quote_by_id_not_found(
    controller: StockQuoteController,
) -> None:
    """Return a failed result when lookup target is missing."""

    result = controller.get_quote_by_id(999999999)

    assert result == {
        "success": False,
        "data": None,
        "error": "Stock quote was not found",
    }


@pytest.mark.integration
def test_get_all_quotes_includes_created_quote(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Return real database rows from get_all_quotes."""

    quote = create_quote(controller, created_quote_ids, day=10)

    result = controller.get_all_quotes()

    assert result["success"] is True
    assert result["error"] is None
    assert quote in result["data"]


@pytest.mark.integration
def test_get_quotes_by_date_range_includes_created_quote(
    controller: StockQuoteController,
    created_quote_ids: list[int],
) -> None:
    """Return real database rows for an inclusive date range."""

    quote = create_quote(controller, created_quote_ids, day=11)

    result = controller.get_quotes_by_date_range(
        f"{TEST_DATE_PREFIX}-01",
        f"{TEST_DATE_PREFIX}-31",
    )

    assert result["success"] is True
    assert result["error"] is None
    assert quote in result["data"]
