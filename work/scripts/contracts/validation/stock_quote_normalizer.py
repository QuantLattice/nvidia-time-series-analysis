"""Normalization utilities for StockQuote DataFrames.

This module contains preprocessing logic for raw stock quote data. It
standardizes column names and data types, removes invalid rows, and sorts
the dataset by trade date to make it ready for validation and analysis.
"""


import pandas as pd

from work.scripts.contracts import StockQuoteSchema as S


class StockQuoteNormalizer:
    """Normalize raw stock quote tabular data.

    The normalizer prepares a DataFrame for downstream validation and
    analytical processing by cleaning column names, converting data types,
    removing incomplete rows, and sorting records by trade date.
    """

    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize a raw stock quote DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Raw input DataFrame containing stock quote data.

        Returns
        -------
        pd.DataFrame
            Normalized DataFrame with cleaned column names, converted data
            types, removed incomplete rows, and sorted records.

        Raises
        ------
        ValueError
            If any required conversion fails or the resulting DataFrame is
            empty after normalization.
        """

        df = df.copy()

        # Remove leading and trailing whitespace from column names.
        df.columns = df.columns.str.strip()

        for col in S.ALL_COLUMNS:
            if col not in df.columns:
                df[col] = pd.NA

        # Convert trade date to pandas datetime type if present.
        if S.TRADE_DATE in df.columns:
            df[S.TRADE_DATE] = pd.to_datetime(
                df[S.TRADE_DATE],
                format="%Y-%m-%d",
                errors="coerce"
            )

        # Normalize string columns (e.g., source).
        for col in S.STRING_COLUMNS:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(dtype="string")
                    .str.strip()
                    .replace(to_replace="", value=pd.NA)
                )

        # Convert all numeric price columns to numeric dtype.
        for col in S.NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Convert volume to integer type for consistency with the database.
        if S.VOLUME in df.columns:
            df[S.VOLUME] = pd.to_numeric(
                df[S.VOLUME],
                errors="coerce"
            ).astype("Int64")

        df = df.dropna(subset=S.REQUIRED_COLUMNS)

        # Sort records chronologically to preserve time-series order.
        df = df.sort_values(S.TRADE_DATE)

        return df
