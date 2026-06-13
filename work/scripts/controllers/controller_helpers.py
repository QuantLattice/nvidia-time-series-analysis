"""Helper utilities for controller layer.

This module provides module-level helper functions shared across
controllers: serialization, ID parsing, and unified error handling.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""

from typing import Any, Callable, Dict, Union

from work.scripts.dto import StockQuoteDTO


def to_stock_quote_dict(dto: StockQuoteDTO) -> Dict[str, Any]:
    """Convert a StockQuoteDTO to a serializable dictionary.

    Parameters
    ----------
    dto : StockQuoteDTO
        Data transfer object to convert.

    Returns
    -------
    dict[str, Any]
        Serializable dictionary for API/GUI usage.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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


def parse_quote_id(value: Union[int, str]) -> int:
    """Parse and validate a stock quote identifier.

    Parameters
    ----------
    value : int | str
        Raw identifier value to parse.

    Returns
    -------
    int
        Parsed positive integer ID.

    Raises
    ------
    TypeError
        If value cannot be converted to integer.
    ValueError
        If the parsed ID is not positive.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
    """

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise TypeError("quote_id must be an integer")

    if parsed <= 0:
        raise ValueError("quote_id must be positive")

    return parsed


def handle_controller_call(
    func: Callable[[], Any]
) -> Dict[str, Any]:
    """Execute a controller operation with unified error handling.

    Wraps controller logic to ensure a consistent response format
    for both successful and failed operations.

    Parameters
    ----------
    func : Callable[[], Any]
        Zero-argument callable containing the operation to execute.

    Returns
    -------
    dict[str, Any]
        Response dictionary with keys:

        - success : bool
        - data : Any | None
        - error : str | None

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
            "error": f"{e.__class__.__name__}: {e}",
        }
