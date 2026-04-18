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

        # Convert trade date to pandas datetime type if present.
        if S.TRADE_DATE in df.columns:
            df[S.TRADE_DATE] = pd.to_datetime(df[S.TRADE_DATE], errors="raise")

        # Convert all numeric price columns to numeric dtype.
        for col in S.NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="raise")

        # Convert volume to integer type for consistency with the database.
        if S.VOLUME in df.columns:
            df[S.VOLUME] = pd.to_numeric(
                df[S.VOLUME],
                errors="raise"
            ).astype("int64")

        # Drop rows with missing values in columns that are already present
        # and considered required for the current dataset structure.
        existing_required = [c for c in S.REQUIRED_COLUMNS if c in df.columns]
        df = df.dropna(subset=existing_required)

        # Sort records chronologically to preserve time-series order.
        if S.TRADE_DATE in df.columns:
            df = df.sort_values(S.TRADE_DATE)

        if df.empty:
            raise ValueError("DataFrame is empty after normalization")

        return df
