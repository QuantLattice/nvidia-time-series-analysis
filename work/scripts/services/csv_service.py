"""CSV import pipeline for stock quote data.

This module implements an ETL (Extract–Transform–Load) pipeline for
importing stock market CSV datasets into the application database.

Pipeline Stages
---------------
1. Extract
    Load raw CSV data into a pandas DataFrame.

2. Map
    Resolve external column names into the internal schema format.

3. Transform
    Normalize values, convert data types, and clean records.

4. Validate
    Enforce schema consistency and business rules.

5. DTO Mapping
    Convert normalized rows into DTO objects.

6. Load
    Persist validated data through the service layer.
"""


from dataclasses import dataclass
from pandas import Series
import pandas as pd
from typing import (
    Any,
    Optional
)
from pathlib import Path

from work.library.io.csv_loader import CSVLoader
from work.scripts.contracts.validation import (
    StockQuoteNormalizer,
    StockQuoteValidator,
)
from work.scripts.contracts.schemas import StockQuoteSchema as S
from work.scripts.contracts.mappers import StockQuoteMapper
from work.scripts.services import StockQuoteService
from work.scripts.dto import StockQuoteCreateDTO


@dataclass(frozen=True, slots=True)
class CSVImportResult:
    source_file: str
    rows_total: int
    rows_imported: int
    first_trade_date: Optional[str] = None
    last_trade_date: Optional[str] = None


@dataclass(frozen=True, slots=True)
class CSVExportResult:
    output_file: str
    rows_exported: int


class CSVService:
    """Import stock quote data from CSV files.

    This service orchestrates a complete ETL workflow that converts
    raw CSV datasets into validated database records using DTO-based
    transfer objects.

    Parameters
    ----------
    stock_service : StockQuoteService
        Service responsible for persisting stock quote records.

    Notes
    -----
    The import pipeline performs:
    - CSV extraction;
    - schema mapping;
    - data normalization;
    - validation;
    - DTO conversion;
    - bulk database persistence.

    Validation or normalization failures interrupt the import process.
    """

    def __init__(
        self,
        stock_service: StockQuoteService
    ) -> None:
        """Initialize CSV import service.

        Parameters
        ----------
        stock_service : StockQuoteService
            Service responsible for persisting stock quote entities.
        """

        self.stock_service = stock_service

    def import_csv(
        self,
        path: str
    ) -> CSVImportResult:
        """Import stock quotes from a CSV file.

        This method executes the complete ETL pipeline:

        extract → map → transform → validate → DTO mapping → load

        Parameters
        ----------
        path : str
            Path to the CSV file containing stock market data.

        Raises
        ------
        FileNotFoundError
            If the CSV file does not exist.

        ValueError
            If mapping, normalization, or validation fails.
        """

        filename = Path(path).name

        # ---------------------------
        # EXTRACT
        # ---------------------------
        df = CSVLoader.load(path)

        # ---------------------------
        # MAP EXTERNAL SCHEMA
        # ---------------------------
        df = StockQuoteMapper.map(
            df=df,
            source=filename
        )

        # ---------------------------
        # NORMALIZE DATA
        # ---------------------------
        df = StockQuoteNormalizer.normalize(df)

        # ---------------------------
        # VALIDATE DATA
        # ---------------------------
        StockQuoteValidator.validate(df)

        # ---------------------------
        # MAP DATAFRAME TO DTO
        # ---------------------------

        quotes = [
            self._to_dto(row)
            for _, row in df.iterrows()
        ]

        # ---------------------------
        # LOAD INTO DATABASE
        # ---------------------------
        self.stock_service.create_quote_bulk(quotes)

        rows_total = len(df)
        first_trade_date = None
        last_trade_date = None
        if not df.empty and S.TRADE_DATE in df.columns:
            first_trade_date = self._to_iso_date(df[S.TRADE_DATE].min())
            last_trade_date = self._to_iso_date(df[S.TRADE_DATE].max())

        return CSVImportResult(
            source_file=filename,
            rows_total=rows_total,
            rows_imported=len(quotes),
            first_trade_date=first_trade_date,
            last_trade_date=last_trade_date,
        )

    def export_csv(
        self,
        path: str
    ) -> CSVExportResult:
        df = self.stock_service.get_all_quotes_df()
        df.loc
        df.to_csv(path_or_buf=path, index=False)

        return CSVExportResult(
            output_file=Path(path).name,
            rows_exported=len(df),
        )

    def _to_dto(
        self,
        row: Series
    ) -> StockQuoteCreateDTO:
        return StockQuoteCreateDTO(
            trade_date=row[S.TRADE_DATE],
            source=row[S.SOURCE],
            open_price=row[S.OPEN_PRICE],
            high_price=row[S.HIGH_PRICE],
            low_price=row[S.LOW_PRICE],
            close_price=row[S.CLOSE_PRICE],
            adj_close_price=self._nullable(
                row.get(S.ADJ_CLOSE_PRICE)
            ),
            volume=row[S.VOLUME],
        )

    def _nullable(
        self,
        value: Optional[Any]
    ) -> Optional[Any]:
        return None if pd.isna(value) else value

    def _to_iso_date(
        self,
        value: Any
    ) -> Optional[str]:
        if value is None or pd.isna(value):
            return None
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)
