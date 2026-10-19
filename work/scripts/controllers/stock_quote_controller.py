"""Controller layer for StockQuote operations.

Acts as interface between the GUI and service layers: parses input,
maps to DTOs, converts results to dicts, and handles exceptions.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from datetime import date

from work.scripts.services import StockQuoteService
from work.scripts.dto import (
    StockQuoteCreateDTO,
    StockQuoteUpdateDTO,
)
from work.scripts.controllers.controller_helpers import (
    to_stock_quote_dict,
    parse_quote_id,
    handle_controller_call,
)

from typing import Dict, Any, Union, List


class StockQuoteController:
    """Intermediary between the GUI and service layers.

    Parameters
    ----------
    service : StockQuoteService
        Service instance for business logic and persistence.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    def __init__(self, service: StockQuoteService) -> None:
        """Store service dependency.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        self.service = service

    # ============================================================
    # CREATE
    # ============================================================

    def create_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new stock quote from raw input data.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(lambda: self._create(data))

    def _create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert data to DTO and call service.create_quote.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        dto = StockQuoteCreateDTO(**data)
        result = self.service.create_quote(dto)
        return to_stock_quote_dict(result)

    # ============================================================
    # UPDATE
    # ============================================================

    def update_quote_by_id(
        self,
        quote_id: Union[int, str],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a stock quote by ID.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            lambda: self._update(parse_quote_id(quote_id), data)
        )

    def _update(
        self,
        quote_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply update DTO and return serialized result.

        Raises ValueError if quote not found.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        dto = StockQuoteUpdateDTO(**data)
        result = self.service.update_quote_by_id(quote_id, dto)
        if result is None:
            raise ValueError("Stock quote not found")
        return to_stock_quote_dict(result)

    # ============================================================
    # DELETE
    # ============================================================

    def delete_quote_by_id(
        self, quote_id: Union[int, str]
    ) -> Dict[str, Any]:
        """Delete a stock quote by ID.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            lambda: self._delete(parse_quote_id(quote_id))
        )

    def _delete(self, quote_id: int) -> dict[str, Any]:
        """Call service delete; raise ValueError if not found.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        success = self.service.delete_quote_by_id(quote_id)
        if not success:
            raise ValueError("Stock quote not found")
        return {"deleted": True}

    # ============================================================
    # READ
    # ============================================================

    def get_quotes_page(
        self,
        page: int,
        page_size: int = 100,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> Dict[str, Any]:
        """Retrieve a paginated page of stock quotes.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            func=lambda: self._get_page(
                page=page,
                page_size=page_size,
                sort_col=sort_col,
                sort_desc=sort_desc,
            )
        )

    def get_quote_by_id(
        self, quote_id: Union[int, str]
    ) -> Dict[str, Any]:
        """Retrieve a single stock quote by ID.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            lambda: self._get_one(parse_quote_id(quote_id))
        )

    def _get_page(
        self,
        page: int,
        page_size: int,
        sort_col: str = 'trade_date',
        sort_desc: bool = False,
    ) -> Dict[str, Any]:
        """Validate, fetch page, return pagination metadata + items.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        if page <= 0:
            raise ValueError('page must be positive')
        if page_size <= 0:
            raise ValueError('page_size must be positive')

        quotes, total = self.service.get_quotes_page(
            page=page,
            page_size=page_size,
            sort_col=sort_col,
            sort_desc=sort_desc,
        )

        return {
            'items': [to_stock_quote_dict(q) for q in quotes],
            'page': page,
            'page_size': page_size,
            'total_rows': total,
            'total_pages': max(
                1, (total + page_size - 1) // page_size
            ),
        }

    def _get_one(self, quote_id: int) -> Dict[str, Any]:
        """Fetch single quote by ID; raise ValueError if absent.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        result = self.service.get_quote_by_id(quote_id)
        if result is None:
            raise ValueError("Stock quote not found")
        return to_stock_quote_dict(result)

    def get_quotes_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> Dict[str, Any]:
        """Retrieve all stock quotes within the given date range.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            lambda: self._get_by_date_range(start_date, end_date)
        )

    def _get_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> List[Dict[str, Any]]:
        """Fetch and serialize quotes between start_date and end_date.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return [
            to_stock_quote_dict(q)
            for q in self.service.get_quotes_by_date_range(
                start_date, end_date
            )
        ]

    def delete_all_quotes(self) -> Dict[str, Any]:
        """Delete all stock quotes from the database.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(
            lambda: {"deleted": self.service.delete_all_quotes()}
        )

    def get_date_range(self) -> Dict[str, Any]:
        """Return min/max trade_date across all stored quotes.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        def _inner():
            """Fetch and return min/max date dict.

            Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
            """
            min_date, max_date = self.service.get_date_range()
            return {"min_date": min_date, "max_date": max_date}

        return handle_controller_call(_inner)

    def get_all_quotes(self) -> Dict[str, Any]:
        """Retrieve all stock quotes.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return handle_controller_call(self._get_all)

    def _get_all(self) -> List[Dict[str, Any]]:
        """Fetch and serialize all stock quotes.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """
        return [
            to_stock_quote_dict(dto)
            for dto in self.service.get_all_quotes()
        ]
