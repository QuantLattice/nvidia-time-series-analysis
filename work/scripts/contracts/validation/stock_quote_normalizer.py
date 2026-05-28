"""Normalization utilities for stock quote DataFrames.

This module provides preprocessing logic for tabular stock market data.
It converts mapped raw datasets into a normalized structure suitable for
validation and analytical processing.

The normalization pipeline includes:
- safe datetime parsing;
- string cleanup and normalization;
- numeric type conversion;
- nullable integer conversion for volume;
- removal of incomplete records;
- chronological sorting of time series data.
"""


import pandas as pd

from work.scripts.contracts.schemas import StockQuoteSchema as S


class StockQuoteNormalizer:
    """Normalize mapped stock quote data.

    The normalizer prepares a DataFrame for downstream validation and
    analytics by converting values to consistent types, cleaning string
    data, removing invalid rows, and sorting records by trade date.

    Notes
    -----
    This class expects column names to already be mapped to the internal
    StockQuoteSchema format by StockQuoteMapper.
    """

    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize a mapped stock quote DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input DataFrame with internal schema column names.

        Returns
        -------
        pd.DataFrame
            Normalized DataFrame with converted types, cleaned values,
            removed invalid rows, and sorted chronological records.

        Notes
        -----
        The normalization process performs:
        - safe datetime parsing using pandas;
        - string cleanup for textual columns;
        - numeric conversion with invalid values coerced to NaN;
        - nullable integer conversion for volume;
        - removal of rows missing required values;
        - sorting by trade date.
        """

        df = df.copy()

        # ============================================================
        # DATE PARSING
        # ============================================================

        if S.TRADE_DATE in df.columns:
            df[S.TRADE_DATE] = pd.to_datetime(
                arg=df[S.TRADE_DATE],
                errors="coerce",
                dayfirst=True,
                format="mixed"
            )

        # ============================================================
        # STRING NORMALIZATION
        # ============================================================

        for col in S.STRING_COLUMNS:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(dtype="string")
                    .str.strip()
                    .replace(to_replace="", value=pd.NA)
                )

        # ============================================================
        # NUMERIC CONVERSION
        # ============================================================

        for col in S.NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(arg=df[col], errors="coerce")

        # ============================================================
        # VOLUME CONVERSION
        # ============================================================

        if S.VOLUME in df.columns:
            df[S.VOLUME] = pd.to_numeric(
                arg=df[S.VOLUME],
                errors="coerce"
            ).astype(dtype="Int64")

        # ============================================================
        # REMOVE INVALID ROWS
        # ============================================================

        df = df.dropna(subset=S.REQUIRED_COLUMNS)

        # ============================================================
        # SORT TIME SERIES
        # ============================================================

        df = df.sort_values(S.TRADE_DATE).reset_index(drop=True)

        return df
