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


import warnings

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
            volume = pd.to_numeric(arg=df[S.VOLUME], errors="coerce")

            # Volume represents a whole number of shares. Cast to a nullable
            # integer only when every present value is whole; otherwise leave
            # the values numeric so the validator can report the column with a
            # clear fix instruction instead of failing here on a cast error.
            if (volume.dropna() % 1 == 0).all():
                volume = volume.astype(dtype="Int64")

            df[S.VOLUME] = volume

        # ============================================================
        # REMOVE INVALID ROWS
        # ============================================================

        df = StockQuoteNormalizer._drop_invalid_rows(df)

        # ============================================================
        # SORT TIME SERIES
        # ============================================================

        df = df.sort_values(S.TRADE_DATE).reset_index(drop=True)

        return df

    @staticmethod
    def _drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
        """Drop rows missing required values and warn about what was removed.

        Rows with a missing value in any required column are removed because
        they cannot be validated downstream. Such values are usually the
        result of failed type conversion (e.g. text in a numeric column is
        coerced to NaN). To avoid losing this information silently, a warning
        is emitted naming the affected columns, the per-column count of
        offending rows, and the original (pre-reset) row positions.

        Parameters
        ----------
        df : pd.DataFrame
            Normalized DataFrame prior to invalid-row removal.

        Returns
        -------
        pd.DataFrame
            DataFrame containing only rows with all required values present.
        """

        required = [col for col in S.REQUIRED_COLUMNS if col in df.columns]
        missing_mask = df[required].isna().any(axis=1)

        if missing_mask.any():
            dropped_positions = df.index[missing_mask].tolist()
            per_column = {
                col: int(df[col].isna().sum())
                for col in required
                if df[col].isna().any()
            }
            details = ", ".join(
                f"'{col}' ({count})" for col, count in per_column.items()
            )
            warnings.warn(
                f"Dropped {int(missing_mask.sum())} row(s) with missing "
                f"required values at row index {dropped_positions}. "
                f"Missing per column: {details}. "
                "Fix: provide valid values in these columns "
                "(non-numeric or unparseable entries are treated as missing) "
                "to keep these rows.",
                UserWarning,
                stacklevel=2,
            )

        return df.dropna(subset=S.REQUIRED_COLUMNS)
