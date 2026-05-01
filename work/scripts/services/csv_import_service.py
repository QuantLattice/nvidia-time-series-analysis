"""CSV import pipeline for StockQuote data.

This module implements an ETL (Extract–Transform–Load) pipeline for
ingesting stock market data from CSV files into the database.

Pipeline Stages
---------------
1. Extract   : Load raw CSV data into a pandas DataFrame
2. Transform : Normalize and clean data (types, formatting, ordering)
3. Validate  : Enforce schema constraints and business rules
4. Map       : Convert DataFrame rows into DTO objects
5. Load      : Persist data via service layer
"""


from work.library.io.csv_loader import CSVLoader
from work.scripts.contracts.validation import (
    StockQuoteNormalizer,
    StockQuoteValidator,
)
from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.services import StockQuoteService
from work.scripts.dto import StockQuoteCreateDTO


class CSVImportService:
    """Service for importing stock quote data from CSV files.

    This service orchestrates a full ETL pipeline that converts raw CSV
    input into validated database records using DTO-based data transfer.

    Parameters
    ----------
    stock_service : StockQuoteService
        Service responsible for persisting stock quote data.

    Notes
    -----
    - Input CSV must conform to StockQuoteSchema.
    - Validation errors will interrupt the pipeline.
    - Designed for batch processing of large datasets.
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

        This method executes the full ETL pipeline:
        extract → transform → validate → map → load

        Parameters
        ----------
        path : str
            Path to the CSV file containing stock quote data.

        Raises
        ------
        FileNotFoundError
            If the CSV file does not exist.
        ValueError
            If normalization or validation fails.
        """

        # ---------------------------
        # EXTRACT
        # ---------------------------
        df = CSVLoader.load(path)

        # ---------------------------
        # TRANSFORM
        # ---------------------------
        df = StockQuoteNormalizer.normalize(df)

        # ---------------------------
        # VALIDATE
        # ---------------------------
        StockQuoteValidator.validate(df)

        # ---------------------------
        # MAP (DataFrame → DTO)
        # ---------------------------
        quotes = [
            StockQuoteCreateDTO(
                trade_date=row[S.TRADE_DATE],
                source=row[S.SOURCE],
                open_price=row[S.OPEN_PRICE],
                high_price=row[S.HIGH_PRICE],
                low_price=row[S.LOW_PRICE],
                close_price=row[S.CLOSE_PRICE],
                adj_close_price=row.get(S.ADJ_CLOSE_PRICE),
                volume=row[S.VOLUME]
            )
            for _, row in df.iterrows()
        ]

        # ---------------------------
        # LOAD (DTO → DB)
        # ---------------------------
        self.stock_service.create_quote_bulk(quotes)
