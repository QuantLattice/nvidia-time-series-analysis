"""CSV import pipeline for StockQuote data.

This module implements a complete ETL-style pipeline for importing stock
market data from CSV files into the database.

Pipeline stages:
1. Load raw CSV data
2. Normalize dataset (data cleaning + type conversion)
3. Validate dataset (schema + business rules)
4. Convert DataFrame into ORM objects
5. Persist data into database via StockQuoteService
"""


from work.library.io.csv_loader import CSVLoader
from work.scripts.contracts.validation import (
    StockQuoteNormalizer,
    StockQuoteValidator,
)
from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.services import StockQuoteService
from work.scripts.db.models import StockQuote


class CSVImportService:
    """Service for importing stock quote data from CSV files.

    This service encapsulates a full ETL pipeline that transforms raw CSV
    input into validated database records.

    Notes
    -----
    The service assumes that input CSV structure is compatible with
    StockQuoteSchema and will raise errors if validation fails.
    """

    def __init__(self, stock_service: StockQuoteService) -> None:
        """Initialize CSV import service.

        Parameters
        ----------
        stock_service : StockQuoteService
            Service responsible for persisting StockQuote entities.
        """
        self.stock_service = stock_service

    def import_csv(self, path: str) -> None:
        """Import stock quotes from a CSV file into the database.

        This method performs full ETL processing:
        - Extract: load CSV into DataFrame
        - Transform: normalize and validate data
        - Load: convert to ORM objects and persist

        Parameters
        ----------
        path : str
            Path to the CSV file containing stock quote data.

        Raises
        ------
        ValueError
            If normalization or validation fails.
        FileNotFoundError
            If CSV file does not exist.
        """

        # ---------------------------
        # EXTRACT
        # ---------------------------
        df = CSVLoader.load(path)

        # ---------------------------
        # TRANSFORM
        # ---------------------------
        df = StockQuoteNormalizer.normalize(df)
        StockQuoteValidator.validate(df)

        # ---------------------------
        # LOAD (ORM mapping)
        # ---------------------------
        quotes = [
            StockQuote(
                trade_date=row[S.TRADE_DATE],
                source=row[S.SOURCE],
                open_price=row[S.OPEN_PRICE],
                high_price=row[S.HIGH_PRICE],
                low_price=row[S.LOW_PRICE],
                close_price=row[S.CLOSE_PRICE],
                adj_close_price=row.get(S.ADJ_CLOSE_PRICE),
                volume=row[S.VOLUME],
            )
            for _, row in df.iterrows()
        ]

        # Persist to database using batch insert
        self.stock_service.add_quote_bulk(quotes)
