"""Service layer for business logic operations.

This package contains application-level services that orchestrate
database access, data transformation, validation, and external data
imports.

Services act as a bridge between:
- Database layer (repositories / ORM)
- Data processing layer (contracts / validation)
- External I/O sources (CSV, files, etc.)

Components
----------
StockQuoteService
    Core service for CRUD operations on stock quotes.

CSVService
    Service responsible for importing, validating and exporting
    stock quote data from CSV files into the database.
"""


from .stock_quote_service import StockQuoteService
from .csv_service import CSVService
from .report_formatter import ReportFormatter


__all__ = [
    "StockQuoteService",
    "CSVService",
    "ReportFormatter",
]
