"""Validation utilities for stock quote DataFrames.

This module provides validation logic for normalized stock market datasets.
It verifies that a DataFrame satisfies structural, type-related, and
business-rule constraints before being used in analytics or persisted
to storage.

Rather than failing on the first problem, the validator inspects every
column and collects all issues. The resulting error lists which columns
need to be fixed and how to fix each one, so a malformed CSV can be
corrected in a single pass.
"""


from typing import List

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

    All per-column issues are accumulated and reported together, each with
    a short instruction describing how to fix the offending column.

    Notes
    -----
    This validator is intended to run after StockQuoteMapper and
    StockQuoteNormalizer have processed the raw dataset.
    """

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        """Validate a stock quote DataFrame.

        Every column is inspected; all detected problems are collected and
        raised together as a single, actionable error.

        Parameters
        ----------
        df : pd.DataFrame
            Normalized DataFrame containing stock quote data.

        Raises
        ------
        ValueError
            If the DataFrame is empty, or if any column violates schema,
            type, nullability, or business-rule constraints. The message
            lists each offending column and how to fix it.
        """

        cls._is_empty(df)

        issues: List[str] = []
        issues += cls._check_columns(df)
        issues += cls._check_types(df)
        issues += cls._check_nulls(df)
        issues += cls._check_business_rules(df)
        issues += cls._check_volume(df)

        if issues:
            raise ValueError(cls._format_issues(issues))

    # ============================================================
    # REPORTING
    # ============================================================

    @staticmethod
    def _format_issues(issues: List[str]) -> str:
        """Build a single error message from collected column issues.

        Parameters
        ----------
        issues : list[str]
            One entry per problematic column.

        Returns
        -------
        str
            Human-readable, multi-line error message.
        """

        body = "\n".join(f"  - {issue}" for issue in issues)
        return (
            "Invalid stock quote data. "
            "Fix the following column(s):\n"
            f"{body}"
        )

    # ============================================================
    # CHECKS
    # ============================================================

    @staticmethod
    def _is_empty(df: pd.DataFrame) -> None:
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
                "Dataframe is empty. "
                "Fix: provide a CSV with at least one data row."
            )

    @staticmethod
    def _check_columns(df: pd.DataFrame) -> List[str]:
        """Report any expected schema columns that are absent.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Returns
        -------
        list[str]
            One issue per missing column.
        """

        issues: List[str] = []
        for col in S.ALL_COLUMNS:
            if col not in df.columns:
                issues.append(
                    f"'{col}': required column is missing. "
                    f"Fix: add a '{col}' column to the dataset."
                )
        return issues

    @staticmethod
    def _check_types(df: pd.DataFrame) -> List[str]:
        """Report columns whose values use an unexpected data type.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Returns
        -------
        list[str]
            One issue per column with an invalid type.
        """

        issues: List[str] = []

        if (S.TRADE_DATE in df.columns and
                not pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])):
            issues.append(
                f"'{S.TRADE_DATE}': values are not valid dates. "
                f"Fix: use a parseable date format such as YYYY-MM-DD."
            )

        for col in S.NUMERIC_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_numeric_dtype(df[col])):
                issues.append(
                    f"'{col}': contains non-numeric values. "
                    f"Fix: use plain numbers (e.g. 105.5), no text or symbols."
                )

        for col in S.INTEGER_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_integer_dtype(df[col])):
                issues.append(
                    f"'{col}': contains non-integer values. "
                    f"Fix: use whole numbers (e.g. 1000 instead of 1000.5)."
                )

        for col in S.STRING_COLUMNS:
            if (col in df.columns and
                    not pd.api.types.is_string_dtype(df[col])):
                issues.append(
                    f"'{col}': values are not text. "
                    f"Fix: provide text values (e.g. a source name)."
                )

        return issues

    @staticmethod
    def _check_nulls(df: pd.DataFrame) -> List[str]:
        """Report required columns that contain missing values.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Returns
        -------
        list[str]
            One issue per required column that is absent or contains nulls.
        """

        issues: List[str] = []
        for col in S.REQUIRED_COLUMNS:
            if col not in df.columns:
                # Absence is already reported by _check_columns.
                continue

            null_count = int(df[col].isnull().sum())
            if null_count:
                issues.append(
                    f"'{col}': has {null_count} missing value(s). "
                    f"Fix: provide a value in every row."
                )
        return issues

    @staticmethod
    def _check_business_rules(df: pd.DataFrame) -> List[str]:
        """Report rows that violate financial business constraints.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Returns
        -------
        list[str]
            One issue if high price is lower than low price in any record.
        """

        issues: List[str] = []

        if (S.HIGH_PRICE in df.columns and S.LOW_PRICE in df.columns and
                pd.api.types.is_numeric_dtype(df[S.HIGH_PRICE]) and
                pd.api.types.is_numeric_dtype(df[S.LOW_PRICE])):
            invalid = int((df[S.HIGH_PRICE] < df[S.LOW_PRICE]).sum())
            if invalid:
                issues.append(
                    f"'{S.HIGH_PRICE}': {invalid} row(s) have high < low. "
                    f"Fix: ensure {S.HIGH_PRICE} >= {S.LOW_PRICE} in each row."
                )

        return issues

    @staticmethod
    def _check_volume(df: pd.DataFrame) -> List[str]:
        """Report negative trading volume values.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to validate.

        Returns
        -------
        list[str]
            One issue if any negative volume value is present.
        """

        issues: List[str] = []

        if (S.VOLUME in df.columns and
                pd.api.types.is_numeric_dtype(df[S.VOLUME])):
            negative = int((df[S.VOLUME] < 0).sum())
            if negative:
                issues.append(
                    f"'{S.VOLUME}': {negative} row(s) have negative volume. "
                    f"Fix: use a volume of 0 or greater."
                )

        return issues
