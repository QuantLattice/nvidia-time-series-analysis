"""Controller API for manual stock quote editing from the GUI."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from work.scripts.services import StockQuoteService


class StockQuoteController:
    """UI-facing controller for stock quote CRUD operations."""

    def __init__(self, service: StockQuoteService) -> None:
        """Store the stock quote service used by this controller."""

        self.service = service

    def create_quote(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a stock quote from GUI form data."""

        return self._handle(lambda: self.service.create_quote(data))

    def update_quote_by_id(
            self,
            quote_id: int | str,
            data: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a stock quote by id from GUI form data."""

        return self._handle(
            lambda: self._require_found(
                self.service.update_quote_by_id(
                    self._parse_quote_id(quote_id),
                    data
                )
            )
        )

    def delete_quote_by_id(self, quote_id: int | str) -> dict[str, Any]:
        """Delete a stock quote by id."""

        return self._handle(
            lambda: self._delete_or_raise(self._parse_quote_id(quote_id))
        )

    def get_quote_by_id(self, quote_id: int | str) -> dict[str, Any]:
        """Return one stock quote by id."""

        return self._handle(
            lambda: self._require_found(
                self.service.get_quote_by_id(self._parse_quote_id(quote_id))
            )
        )

    def get_all_quotes(self) -> dict[str, Any]:
        """Return all stock quotes."""

        return self._handle(self.service.get_all_quotes)

    def get_quotes_by_date_range(
            self,
            start_date: Any,
            end_date: Any
    ) -> dict[str, Any]:
        """Return stock quotes for an inclusive date range."""

        return self._handle(
            lambda: self.service.get_quotes_by_date_range(
                start_date,
                end_date
            )
        )

    def _handle(self, operation: Callable[[], Any]) -> dict[str, Any]:
        """Return a structured UI result for a service operation."""

        try:
            return self._success(operation())
        except (TypeError, ValueError) as exc:
            return self._failure(str(exc))
        except Exception as exc:
            return self._failure(f"{exc.__class__.__name__}: {exc}")

    def _delete_or_raise(self, quote_id: int) -> dict[str, bool]:
        """Delete a record or raise a UI-friendly not-found error."""

        deleted = self.service.delete_quote_by_id(quote_id)
        if not deleted:
            raise ValueError("Stock quote was not found")

        return {"deleted": True}

    def _require_found(self, quote: dict[str, Any] | None) -> dict[str, Any]:
        """Return a quote or raise a UI-friendly not-found error."""

        if quote is None:
            raise ValueError("Stock quote was not found")

        return quote

    def _parse_quote_id(self, quote_id: int | str) -> int:
        """Parse a GUI id value into a positive integer primary key."""

        if isinstance(quote_id, bool):
            raise TypeError("quote_id must be an integer")
        try:
            parsed_quote_id = int(quote_id)
        except (TypeError, ValueError) as exc:
            raise TypeError("quote_id must be an integer") from exc

        if parsed_quote_id <= 0:
            raise ValueError("quote_id must be positive")

        return parsed_quote_id

    def _success(self, data: Any) -> dict[str, Any]:
        """Build a successful UI result."""

        return {
            "success": True,
            "data": data,
            "error": None,
        }

    def _failure(self, error: str) -> dict[str, Any]:
        """Build a failed UI result."""

        return {
            "success": False,
            "data": None,
            "error": error,
        }
