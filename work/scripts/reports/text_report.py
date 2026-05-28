"""
Simple human-readable text report for stock quote datasets.

Generates a formatted multi-section summary including shape,
date range, data sources, column overview, missing value counts,
and basic descriptive statistics.
"""

from dataclasses import dataclass
from typing import Optional
import pandas as pd

from work.scripts.contracts.schemas.stock_quote_schema import StockQuoteSchema as S


@dataclass(frozen=True)
class TextReportResult:
    """
    Plain-text summary of a stock dataset.

    Attributes
    ----------
    content : str
        Formatted multi-line report string.
    """

    content: str


class TextReport:
    """
    Generates a plain-text summary for a stock quotes DataFrame.

    Sections
    --------
    - Dataset shape.
    - Date range (when trade_date column is present).
    - Unique data sources.
    - Column overview with dtype and non-null counts.
    - Missing value summary.
    - Numeric descriptives (mean, std, min, median, max).
    """

    _SEP = "=" * 48

    def generate(self, df: pd.DataFrame) -> TextReportResult:
        """
        Generate a plain-text summary report.

        Parameters
        ----------
        df : pd.DataFrame
            Input stock dataset.

        Returns
        -------
        TextReportResult
            Formatted text report.
        """

        blocks = [
            self._header(),
            self._shape_block(df),
            self._date_range_block(df),
            self._sources_block(df),
            self._columns_block(df),
            self._missing_block(df),
            self._numeric_summary_block(df),
        ]

        content = "\n\n".join(b for b in blocks if b is not None)
        return TextReportResult(content=content)

    # --------------------------------
    # PRIVATE BLOCKS
    # --------------------------------

    def _header(self) -> str:
        return f"{self._SEP}\n  DATASET SUMMARY\n{self._SEP}"

    def _shape_block(self, df: pd.DataFrame) -> str:
        rows, cols = df.shape
        return f"Shape:    {rows:,} rows × {cols} columns"

    def _date_range_block(self, df: pd.DataFrame) -> Optional[str]:
        if S.TRADE_DATE not in df.columns:
            return None
        dates = pd.to_datetime(df[S.TRADE_DATE], errors="coerce").dropna()
        if dates.empty:
            return None
        start = dates.min().date()
        end = dates.max().date()
        span = (dates.max() - dates.min()).days
        return f"Dates:    {start} → {end}  ({span:,} calendar days)"

    def _sources_block(self, df: pd.DataFrame) -> Optional[str]:
        if S.SOURCE not in df.columns:
            return None
        sources = sorted(str(s) for s in df[S.SOURCE].dropna().unique())
        label = ", ".join(sources)
        return f"Sources:  {label}  ({len(sources)} total)"

    def _columns_block(self, df: pd.DataFrame) -> str:
        lines = [self._SEP, "  COLUMNS", self._SEP]
        for col in df.columns:
            non_null = int(df[col].notna().sum())
            dtype = str(df[col].dtype)
            lines.append(f"  {col:<26} {non_null:>8,} non-null   {dtype}")
        return "\n".join(lines)

    def _missing_block(self, df: pd.DataFrame) -> str:
        total_missing = int(df.isna().sum().sum())
        if total_missing == 0:
            return "Missing:  none"
        ratio = total_missing / df.size * 100
        return f"Missing:  {total_missing:,} cells ({ratio:.2f}% of total)"

    def _numeric_summary_block(self, df: pd.DataFrame) -> Optional[str]:
        numeric = df.select_dtypes(include="number")
        if numeric.empty:
            return None

        desc = numeric.describe().T[["mean", "std", "min", "50%", "max"]]
        desc.columns = ["mean", "std", "min", "median", "max"]
        desc = desc.round(4)

        header = f"  {'column':<26} {'mean':>12} {'std':>12} {'min':>12} {'median':>12} {'max':>12}"
        divider = "  " + "-" * 86

        lines = [self._SEP, "  NUMERIC SUMMARY", self._SEP, header, divider]

        for col, row in desc.iterrows():
            lines.append(
                f"  {col:<26} {row['mean']:>12.4f} {row['std']:>12.4f}"
                f" {row['min']:>12.4f} {row['median']:>12.4f} {row['max']:>12.4f}"
            )

        return "\n".join(lines)
