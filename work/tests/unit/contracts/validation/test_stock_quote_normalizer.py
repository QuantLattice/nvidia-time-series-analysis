"""Unit tests for StockQuoteNormalizer.

This module verifies that raw stock quote data is correctly normalized
before validation and persistence. The tests cover:

- column name cleanup
- type conversion
- sorting by trade date
- dropping incomplete rows
- handling of invalid input values
"""


import numpy as np
import pandas as pd
import pytest

from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.contracts.validation import StockQuoteNormalizer


# =========================================================
# POSITIVE CASES
# =========================================================

@pytest.mark.unit
def test_normalization_basic(raw_df: pd.DataFrame) -> None:
    """Normalize dirty raw input into schema-compliant data."""
    df = StockQuoteNormalizer.normalize(raw_df)

    assert list(df.columns) == [
        S.TRADE_DATE,
        S.SOURCE,
        S.OPEN_PRICE,
        S.HIGH_PRICE,
        S.LOW_PRICE,
        S.CLOSE_PRICE,
        S.ADJ_CLOSE_PRICE,
        S.VOLUME,
    ]

    assert pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])
    assert pd.api.types.is_numeric_dtype(df[S.OPEN_PRICE])
    assert pd.api.types.is_integer_dtype(df[S.VOLUME])


@pytest.mark.unit
def test_sorting_by_date(raw_df: pd.DataFrame) -> None:
    """Normalized data must be sorted by trade date."""
    df = StockQuoteNormalizer.normalize(raw_df)

    assert df[S.TRADE_DATE].is_monotonic_increasing


# =========================================================
# TYPE CONVERSIONS
# =========================================================

@pytest.mark.unit
def test_numeric_conversion() -> None:
    """Convert string-encoded numeric values to numeric dtypes."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["2024-01-01"],
        S.SOURCE: ["https://example.com/nvda/2024-01-01"],
        S.OPEN_PRICE: ["100.5"],
        S.HIGH_PRICE: ["110.5"],
        S.LOW_PRICE: ["90.5"],
        S.CLOSE_PRICE: ["105.5"],
        S.ADJ_CLOSE_PRICE: ["105.5"],
        S.VOLUME: ["1000"],
    })

    result = StockQuoteNormalizer.normalize(df)

    assert isinstance(result[S.OPEN_PRICE].iloc[0], float)
    assert isinstance(result[S.VOLUME].iloc[0], (int, np.integer))


# =========================================================
# MISSING VALUES
# =========================================================

@pytest.mark.unit
def test_drop_na_rows() -> None:
    """Drop rows containing missing values in required columns."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["2024-01-01", None],
        S.SOURCE: [
            "https://example.com/nvda/2024-01-01",
            "https://example.com/nvda/missing-date",
        ],
        S.OPEN_PRICE: ["100", "101"],
        S.HIGH_PRICE: ["110", "111"],
        S.LOW_PRICE: ["90", "91"],
        S.CLOSE_PRICE: ["105", "106"],
        S.ADJ_CLOSE_PRICE: ["105", "106"],
        S.VOLUME: ["1000", "2000"],
    })

    result = StockQuoteNormalizer.normalize(df)

    assert len(result) == 1


# =========================================================
# COLUMN CLEANING
# =========================================================

@pytest.mark.unit
def test_column_stripping() -> None:
    """Strip leading and trailing whitespace from column names."""
    df = pd.DataFrame({
        " trade_date ": ["2024-01-01"],
        " source ": ["https://example.com/nvda/2024-01-01"],
        " open_price ": ["100"],
        " high_price ": ["110"],
        " low_price ": ["90"],
        " close_price ": ["105"],
        " adj_close_price ": ["105"],
        " volume ": ["1000"],
    })

    result = StockQuoteNormalizer.normalize(df)

    assert S.TRADE_DATE in result.columns
    assert " trade_date " not in result.columns


# =========================================================
# ERROR HANDLING
# =========================================================

@pytest.mark.unit
def test_invalid_date() -> None:
    """Raise an exception when the trade date cannot be parsed."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["invalid-date"],
        S.SOURCE: ["https://example.com/nvda/invalid-date"],
        S.OPEN_PRICE: ["100"],
        S.HIGH_PRICE: ["110"],
        S.LOW_PRICE: ["90"],
        S.CLOSE_PRICE: ["105"],
        S.ADJ_CLOSE_PRICE: ["105"],
        S.VOLUME: ["1000"],
    })

    with pytest.raises(Exception):
        StockQuoteNormalizer.normalize(df)


@pytest.mark.unit
def test_invalid_numeric() -> None:
    """Raise an exception when numeric conversion fails."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["2024-01-01"],
        S.SOURCE: ["https://example.com/nvda/2024-01-01"],
        S.OPEN_PRICE: ["bad"],
        S.HIGH_PRICE: ["110"],
        S.LOW_PRICE: ["90"],
        S.CLOSE_PRICE: ["105"],
        S.ADJ_CLOSE_PRICE: ["105"],
        S.VOLUME: ["1000"],
    })

    with pytest.raises(Exception):
        StockQuoteNormalizer.normalize(df)


@pytest.mark.unit
def test_invalid_volume() -> None:
    """Raise an exception when volume cannot be converted to integer."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["2024-01-01"],
        S.SOURCE: ["https://example.com/nvda/2024-01-01"],
        S.OPEN_PRICE: ["100"],
        S.HIGH_PRICE: ["110"],
        S.LOW_PRICE: ["90"],
        S.CLOSE_PRICE: ["105"],
        S.ADJ_CLOSE_PRICE: ["105"],
        S.VOLUME: ["not_int"],
    })

    with pytest.raises(Exception):
        StockQuoteNormalizer.normalize(df)


# =========================================================
# OPTIONAL COLUMNS
# =========================================================

@pytest.mark.unit
def test_optional_adj_close_missing() -> None:
    """Allow normalized data to omit optional adjusted close values."""
    df = pd.DataFrame({
        S.TRADE_DATE: ["2024-01-01"],
        S.SOURCE: ["https://example.com/nvda/2024-01-01"],
        S.OPEN_PRICE: ["100"],
        S.HIGH_PRICE: ["110"],
        S.LOW_PRICE: ["90"],
        S.CLOSE_PRICE: ["105"],
        S.VOLUME: ["1000"],
    })

    result = StockQuoteNormalizer.normalize(df)

    assert (S.ADJ_CLOSE_PRICE not in result.columns or
            result[S.ADJ_CLOSE_PRICE].isnull().all())
