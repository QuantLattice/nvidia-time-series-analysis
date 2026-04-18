"""Validation utilities for StockQuote DataFrames.

This module checks whether a stock quote dataset satisfies structural,
type-related, and business-rule constraints before it is stored in the
database or used in analytics.
"""


import pandas as pd

from work.scripts.contracts import StockQuoteSchema as S


class StockQuoteValidator:
    """Validate stock quote tabular data.

    The validator checks the presence of required columns, column data types,
    null values, and domain-specific financial rules such as OHLC consistency
    and non-negative trading volume.
    """

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        """Validate a stock quote DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing stock quote data.

        Raises
        ------
        ValueError
            If the DataFrame violates schema, type, nullability, or business
            rule constraints.
        """

        cls._validate_columns(df)
        cls._validate_types(df)
        cls._validate_nulls(df)
        cls._validate_business_rules(df)
        cls._validate_volume(df)

    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> None:
        """Check that all expected columns are present.

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
        """Check that columns have expected data types.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If trade date is not datetime, numeric columns are not numeric,
            or integer columns are not integer typed.
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
        """Validate financial business rules.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If high price is lower than low price in any row.
        """

        if (df[S.HIGH_PRICE] < df[S.LOW_PRICE]).any():
            raise ValueError("Invalid OHLC: high < low")

    @staticmethod
    def _validate_volume(df: pd.DataFrame) -> None:
        """Check that trading volume is non-negative.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Raises
        ------
        ValueError
            If negative volume values are detected.
        """

        if (df[S.VOLUME] < 0).any():
            raise ValueError("Negative volume detected")
