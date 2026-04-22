"""Unit tests for StockQuoteValidator.

This module verifies that normalized stock quote data satisfies schema,
type, nullability, and business-rule constraints before being accepted
by the application.
"""


import pandas as pd
import pytest

from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.contracts.validation import StockQuoteValidator


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.unit
def test_validator_valid_data(valid_df: pd.DataFrame) -> None:
    """Accept a valid, fully normalized DataFrame."""
    StockQuoteValidator.validate(valid_df)


# =========================================================
# COLUMN VALIDATION
# =========================================================

@pytest.mark.unit
def test_missing_column(valid_df: pd.DataFrame) -> None:
    """Reject a DataFrame with a missing required column."""
    df = valid_df.drop(columns=[S.OPEN_PRICE])

    with pytest.raises(ValueError, match="Missing columns"):
        StockQuoteValidator.validate(df)


# =========================================================
# TYPE VALIDATION
# =========================================================

@pytest.mark.unit
def test_invalid_trade_date_type(valid_df: pd.DataFrame) -> None:
    """Reject a non-datetime trade_date column."""
    df = valid_df.copy()
    # string values instead of datetime
    df[S.TRADE_DATE] = ["2024-01-01", "2024-01-02"]

    with pytest.raises(ValueError, match="must be datetime"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_invalid_numeric_type(valid_df: pd.DataFrame) -> None:
    """Reject non-numeric price values."""
    df = valid_df.copy()
    df[S.OPEN_PRICE] = ["bad", "data"]

    with pytest.raises(ValueError, match="must be numeric"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_invalid_integer_type(valid_df: pd.DataFrame) -> None:
    """Reject floating-point values in integer columns."""
    df = valid_df.copy()
    df[S.VOLUME] = [1000.5, 2000.5]  # float values instead of integers

    with pytest.raises(ValueError, match="must be integer"):
        StockQuoteValidator.validate(df)


# =========================================================
# NULL VALIDATION
# =========================================================

@pytest.mark.unit
def test_null_values(valid_df: pd.DataFrame) -> None:
    """Reject required columns containing null values."""
    df = valid_df.copy()
    df.loc[0, S.CLOSE_PRICE] = None

    with pytest.raises(ValueError, match="Null values"):
        StockQuoteValidator.validate(df)


# =========================================================
# BUSINESS RULES
# =========================================================

@pytest.mark.unit
def test_invalid_ohlc(valid_df: pd.DataFrame) -> None:
    """
    Reject invalid OHLC relationships where high price is below low price.
    """
    df = valid_df.copy()
    df[S.HIGH_PRICE] = [80.0, 70.0]  # intentionally lower than low price

    with pytest.raises(ValueError, match="Invalid OHLC"):
        StockQuoteValidator.validate(df)


# =========================================================
# VOLUME VALIDATION
# =========================================================

@pytest.mark.unit
def test_negative_volume(valid_df: pd.DataFrame) -> None:
    """Reject negative trading volume values."""
    df = valid_df.copy()
    df[S.VOLUME] = [-1, 1000]

    with pytest.raises(ValueError, match="Negative volume"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_duplicate_source(valid_df: pd.DataFrame) -> None:
    """Reject duplicate source values."""
    df = valid_df.copy()
    df[S.SOURCE] = ["https://example.com/duplicate"] * len(df)

    with pytest.raises(ValueError, match="Duplicate values"):
        StockQuoteValidator.validate(df)
