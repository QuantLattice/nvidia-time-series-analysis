"""DTO package for stock quote data transfer.

This package provides structured data transfer objects used for
communication between different layers of the application.

Exports
-------
- StockQuoteCreateDTO : for creating new records
- StockQuoteUpdateDTO : for partial updates
- StockQuoteDTO       : for read operations

Notes
-----
DTOs act as explicit contracts and isolate the domain model (ORM)
from external interfaces such as GUI and import pipelines.
"""


from .stock_quote import (
    StockQuoteCreateDTO,
    StockQuoteUpdateDTO,
    StockQuoteDTO
)


__all__ = [
    "StockQuoteCreateDTO",
    "StockQuoteUpdateDTO",
    "StockQuoteDTO"
]
