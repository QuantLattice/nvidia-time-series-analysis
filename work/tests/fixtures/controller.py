"""Reusable controller fixtures for database-backed tests."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any
from uuid import uuid4

import pytest

from work.scripts.controllers.stock_quote_controller import (
    StockQuoteController,
)
from work.scripts.db.session import Database
from work.scripts.services import StockQuoteService


TEST_DATE_YEAR = 9000 + uuid4().int % 900
TEST_DATE_PREFIX = f"{TEST_DATE_YEAR}-12"


@pytest.fixture(scope="module")
def controller() -> StockQuoteController:
    """Return a controller wired to the real application database."""

    db = Database()
    service = StockQuoteService(db)
    return StockQuoteController(service)


@pytest.fixture
def created_quote_ids(controller: StockQuoteController) -> Iterator[list[int]]:
    """Track created database rows and delete them after each test."""

    quote_ids: list[int] = []
    yield quote_ids

    for quote_id in reversed(quote_ids):
        controller.delete_quote_by_id(quote_id)


def quote_payload(day: int = 1) -> dict[str, Any]:
    """Build a unique valid create payload for the real database."""

    trade_date = f"{TEST_DATE_PREFIX}-{day:02d}"
    unique_token = uuid4().hex
    return {
        "trade_date": trade_date,
        "source": f"https://example.com/tests/nvda/{trade_date}/{unique_token}",
        "open_price": 850.5,
        "high_price": 875.0,
        "low_price": 842.1,
        "close_price": 870.25,
        "adj_close_price": 870.25,
        "volume": 35000000,
    }


def create_quote(
    controller: StockQuoteController,
    created_quote_ids: list[int],
    *,
    day: int = 1,
) -> dict[str, Any]:
    """Create a quote through the controller and schedule cleanup."""

    result = controller.create_quote(quote_payload(day))
    assert result["success"] is True, result

    quote = result["data"]
    created_quote_ids.append(quote["id"])
    return quote
