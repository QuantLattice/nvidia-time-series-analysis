"""Validation utilities for stock quote DataFrames.

This module provides validation logic for normalized stock market datasets.
It verifies that a DataFrame satisfies structural, type-related, and
business-rule constraints before being used in analytics or persisted
to storage.
"""


import pandas as pd

from work.scripts.contracts.schemas import StockQuoteSchema as S


class StockQuoteValidator:
    """Validate normalized stock quote data.

    The validator checks:
    - dataset emptiness;
    - required schema columns;
    - column data types;
    - missing values;
    - financial business rules;
    - trading volume consistency.

    Notes
    -----
    This validator is intended to run after StockQuoteMapper and
    StockQuoteNormalizer have processed the raw dataset.
    """

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        """Validate a stock quote DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Normalized DataFrame containing stock quote data.

        Raises
        ------
        ValueError
            If the DataFrame violates schema, type, nullability,
            emptiness, or business-rule constraints.
        """

        cls._is_emty(df)
        cls._validate_columns(df)
        cls._validate_types(df)
        cls._validate_nulls(df)
        cls._validate_business_rules(df)
        cls._validate_volume(df)

    @staticmethod
    def _is_emty(df: pd.DataFrame) -> None:
        """Check that the DataFrame is not empty.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If the DataFrame contains no rows.
        """

        if df.empty:
            raise ValueError(
                "Dataframe is emty."
            )

    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> None:
        """Check that all expected schema columns are present.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If one or more expected columns are missing.
        """

        missing = set(S.ALL_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")

    @staticmethod
    def _validate_types(df: pd.DataFrame) -> None:
        """Check that columns use expected data types.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If:
            - trade_date is not datetime;
            - numeric columns are not numeric;
            - integer columns are not integer typed;
            - string columns are not string typed.
        """

        if not pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE]):
            raise ValueError(f"{S.TRADE_DATE} must be datetime")

        for col in S.NUMERIC_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_numeric_dtype(df[col])):
                raise ValueError(f"{col} must be numeric")

        for col in S.INTEGER_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_integer_dtype(df[col])):
                raise ValueError(f"{col} must be integer")

        for col in S.STRING_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_string_dtype(df[col])):
                raise ValueError(f"{col} must be string")

    @staticmethod
    def _validate_nulls(df: pd.DataFrame) -> None:
        """Check that required columns contain no missing values.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If a required column is missing or contains null values.
        """

        for col in S.REQUIRED_COLUMNS:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

            if df[col].isnull().any():
                raise ValueError(f"Null values in {col}")

    @staticmethod
    def _validate_business_rules(df: pd.DataFrame) -> None:
        """Validate financial business constraints.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If high price is lower than low price in any record.
        """

        if (df[S.HIGH_PRICE] < df[S.LOW_PRICE]).any():
            raise ValueError("Invalid OHLC: high < low")

    @staticmethod
    def _validate_volume(df: pd.DataFrame) -> None:
        """Check that trading volume values are non-negative.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If negative trading volume values are detected.
        """

        if (df[S.VOLUME] < 0).any():
            raise ValueError("Negative volume detected")
