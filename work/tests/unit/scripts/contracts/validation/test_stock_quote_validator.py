"""Unit tests for StockQuoteValidator.

This module verifies schema, type, nullability, and business-rule checks
performed by the StockQuoteValidator.

Test coverage includes:
- required column presence
- datetime, string, numeric, and integer type validation
- null value detection
- OHLC consistency rules
- non-negative volume constraint
"""


import pytest

from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.contracts.validation import StockQuoteValidator
from work.tests.factories import DataFrameFactory


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.unit
def test_validator_valid_data() -> None:
    """Validate a clean dataset that satisfies all schema rules."""

    df = DataFrameFactory.valid()
    StockQuoteValidator.validate(df)


# =========================================================
# COLUMN VALIDATION
# =========================================================

@pytest.mark.unit
def test_missing_column() -> None:
    """Reject a dataset with a missing required column."""

    df = DataFrameFactory.valid()
    df = df.drop(columns=[S.OPEN_PRICE])

    with pytest.raises(ValueError, match="Missing columns"):
        StockQuoteValidator.validate(df)


# =========================================================
# TYPE VALIDATION
# =========================================================

@pytest.mark.unit
def test_invalid_trade_date_type() -> None:
    """Reject a dataset where trade_date cannot be interpreted as datetime."""

    df = DataFrameFactory.with_invalid_datetime()

    with pytest.raises(ValueError, match="must be datetime"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_invalid_string_type() -> None:
    """Reject a dataset where the source column does not contain strings."""

    df = DataFrameFactory.valid()

    df[S.SOURCE] = [15]

    with pytest.raises(ValueError, match="must be string"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_invalid_numeric_type() -> None:
    """Reject a dataset where a numeric price column contains text values."""

    df = DataFrameFactory.valid(rows=2)

    df[S.OPEN_PRICE] = ["bad", "data"]

    with pytest.raises(ValueError, match="must be numeric"):
        StockQuoteValidator.validate(df)


@pytest.mark.unit
def test_invalid_integer_type() -> None:
    """Reject a dataset where volume is not stored as an integer type."""

    df = DataFrameFactory.valid(rows=2)

    df[S.VOLUME] = [1000.5, 2000.5]

    with pytest.raises(ValueError, match="must be integer"):
        StockQuoteValidator.validate(df)


# =========================================================
# NULL VALIDATION
# =========================================================

@pytest.mark.unit
def test_null_values() -> None:
    """Reject a dataset containing null values in required columns."""

    df = DataFrameFactory.valid()

    df.loc[0, S.CLOSE_PRICE] = None

    with pytest.raises(ValueError, match="Null values"):
        StockQuoteValidator.validate(df)


# =========================================================
# BUSINESS RULES
# =========================================================

@pytest.mark.unit
def test_invalid_ohlc() -> None:
    """Reject a dataset with an invalid OHLC relationship."""

    df = DataFrameFactory.valid(rows=2)
    df[S.HIGH_PRICE] = [80.0, 70.0]
    df[S.LOW_PRICE] = [90, 80]

    with pytest.raises(ValueError, match="Invalid OHLC"):
        StockQuoteValidator.validate(df)


# =========================================================
# VOLUME VALIDATION
# =========================================================

@pytest.mark.unit
def test_negative_volume() -> None:
    """Reject a dataset that contains negative trading volume."""

    df = DataFrameFactory.valid(rows=2)

    df[S.VOLUME] = [-1, 1000]

    with pytest.raises(ValueError, match="Negative volume"):
        StockQuoteValidator.validate(df)
