"""Controller layer for StockQuote operations.

This module provides a controller that acts as an interface between the
GUI layer and the service layer. It is responsible for:

- Input validation and parsing (e.g., converting IDs)
- Mapping raw input data to DTOs
- Converting service results into serializable dictionaries
- Handling exceptions and returning unified response structures

The controller ensures that the GUI layer interacts with a stable and
predictable API.
"""


from datetime import date

from work.scripts.services import StockQuoteService
from work.scripts.dto import (
    StockQuoteCreateDTO,
    StockQuoteUpdateDTO,
    StockQuoteDTO
)

from typing import (
    Dict,
    Any,
    Callable,
    Union,
    List
)


class StockQuoteController:
    """Controller for managing stock quote operations.

    This class acts as an intermediary between the presentation layer (GUI)
    and the business logic layer (services). It transforms raw input into
    DTOs, invokes service methods, and formats responses.

    Parameters
    ----------
    service : StockQuoteService
        Service instance responsible for business logic and persistence.
    """

    def __init__(self, service: StockQuoteService) -> None:
        """Initialize controller with service dependency.

        Parameters
        ----------
        service : StockQuoteService
            Service layer instance used to perform operations.
        """

        self.service = service

    # ============================================================
    # CREATE
    # ============================================================

    def create_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new stock quote.

        Parameters
        ----------
        data : dict[str, Any]
            Raw input data (e.g., from GUI form).

        Returns
        -------
        dict[str, Any]
            Standardized response containing operation result.
        """

        return self._handle(lambda: self._create(data))

    def _create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Internal create implementation.

        Converts raw input into DTO and delegates creation to service.

        Parameters
        ----------
        data : dict[str, Any]

        Returns
        -------
        dict[str, Any]
            Serialized created object.
        """

        dto = StockQuoteCreateDTO(**data)

        result = self.service.create_quote(dto)

        return self._to_dict(result)

    # ============================================================
    # UPDATE
    # ============================================================

    def update_quote_by_id(
        self,
        quote_id: Union[int, str],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a stock quote by ID.

        Parameters
        ----------
        quote_id : int | str
            Identifier of the stock quote.
        data : dict[str, Any]
            Fields to update.

        Returns
        -------
        dict[str, Any]
            Standardized response.
        """

        return self._handle(
            lambda: self._update(self._parse_id(quote_id), data)
        )

    def _update(
        self,
        quote_id: int,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Internal update implementation.

        Parameters
        ----------
        quote_id : int
        data : dict[str, Any]

        Returns
        -------
        dict[str, Any]
            Serialized updated object.

        Raises
        ------
        ValueError
            If the stock quote is not found.
        """

        dto = StockQuoteUpdateDTO(**data)

        result = self.service.update_quote_by_id(quote_id, dto)
        if result is None:
            raise ValueError("Stock quote not found")

        return self._to_dict(result)

    # ============================================================
    # DELETE
    # ============================================================

    def delete_quote_by_id(self, quote_id: Union[int, str]) -> Dict[str, Any]:
        """Delete a stock quote by ID.

        Parameters
        ----------
        quote_id : int | str

        Returns
        -------
        dict[str, Any]
            Standardized response indicating deletion result.
        """

        return self._handle(
            lambda: self._delete(self._parse_id(quote_id))
        )

    def _delete(self, quote_id: int) -> dict[str, Any]:
        """Internal delete implementation.

        Parameters
        ----------
        quote_id : int

        Returns
        -------
        dict[str, Any]

        Raises
        ------
        ValueError
            If the stock quote is not found.
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
        page_size: int = 100
    ) -> Dict[str, Any]:
        return self._handle(
            func=lambda: self._get_page(
                page=page,
                page_size=page_size
            )
        )

    def get_quote_by_id(self, quote_id: Union[int, str]) -> Dict[str, Any]:
        """Retrieve a single stock quote by ID.

        Parameters
        ----------
        quote_id : int | str

        Returns
        -------
        dict[str, Any]
            Standardized response with quote data.
        """

        return self._handle(
            lambda: self._get_one(self._parse_id(quote_id))
        )

    def _get_page(
        self,
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        if page <= 0:
            raise ValueError('page must be positive')
        if page_size <= 0:
            raise ValueError('page_size must be positive')

        quotes, total = self.service.get_quotes_page(
            page=page,
            page_size=page_size
        )

        return {
            'items': [self._to_dict(q) for q in quotes],
            'page': page,
            'page_size': page_size,
            'total_rows': total,
            'total_pages': max(1, (total + page_size - 1) // page_size),
        }

    def _get_one(self, quote_id: int) -> Dict[str, Any]:
        """Internal retrieval of a single stock quote.

        Parameters
        ----------
        quote_id : int

        Returns
        -------
        dict[str, Any]

        Raises
        ------
        ValueError
            If the stock quote is not found.
        """

        result = self.service.get_quote_by_id(quote_id)

        if result is None:
            raise ValueError("Stock quote not found")

        return self._to_dict(result)

    def get_quotes_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> Dict[str, Any]:
        """Retrieve stock quotes within a date range.

        Parameters
        ----------
        start_date : date
            Start of the range (inclusive).
        end_date : date
            End of the range (inclusive).

        Returns
        -------
        dict[str, Any]
            Standardized response containing a list of quote dicts.
        """

        return self._handle(
            lambda: self._get_by_date_range(start_date, end_date)
        )

    def _get_by_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> List[Dict[str, Any]]:
        return [
            self._to_dict(q)
            for q in self.service.get_quotes_by_date_range(start_date, end_date)
        ]

    def get_all_quotes(self) -> Dict[str, Any]:
        """Retrieve all stock quotes.

        Returns
        -------
        dict[str, Any]
            Standardized response containing list of quotes.
        """

        return self._handle(self._get_all)

    def _get_all(self) -> List[Dict[str, Any]]:
        """Internal retrieval of all stock quotes.

        Returns
        -------
        list[dict[str, Any]]
            List of serialized stock quotes.
        """

        return [
            self._to_dict(dto)
            for dto in self.service.get_all_quotes()
        ]

    # ============================================================
    # HELPERS
    # ============================================================

    def _to_dict(self, dto: StockQuoteDTO) -> Dict[str, Any]:
        """Convert DTO to dictionary representation.

        Parameters
        ----------
        dto : StockQuoteDTO

        Returns
        -------
        dict[str, Any]
            Serializable dictionary for API/GUI usage.
        """

        return {
            "id": dto.id,
            "trade_date": dto.trade_date.isoformat(),
            "source": dto.source,
            "open_price": dto.open_price,
            "high_price": dto.high_price,
            "low_price": dto.low_price,
            "close_price": dto.close_price,
            "adj_close_price": dto.adj_close_price,
            "volume": dto.volume,
        }

    def _parse_id(self, value: Union[int, str]) -> int:
        """Parse and validate quote identifier.

        Parameters
        ----------
        value : int | str

        Returns
        -------
        int
            Parsed integer ID.

        Raises
        ------
        TypeError
            If value cannot be converted to integer.
        ValueError
            If ID is not positive.
        """

        try:
            parsed = int(value)
        except (TypeError, ValueError):
            raise TypeError("quote_id must be an integer")

        if parsed <= 0:
            raise ValueError("quote_id must be positive")

        return parsed

    # ============================================================
    # RESPONSE WRAPPER
    # ============================================================

    def _handle(self, func: Callable[[], Any]) -> Dict[str, Any]:
        """Execute operation with unified error handling.

        This method wraps controller logic to ensure consistent response
        format for both successful and failed operations.

        Parameters
        ----------
        func : Callable[[], Any]
            Function to execute.

        Returns
        -------
        dict[str, Any]
            Response dictionary with keys:
            - success : bool
            - data : Any | None
            - error : str | None
        """

        try:
            return {
                "success": True,
                "data": func(),
                "error": None,
            }
        except (ValueError, TypeError) as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": f"{e.__class__.__name__}: {e}"
            }
