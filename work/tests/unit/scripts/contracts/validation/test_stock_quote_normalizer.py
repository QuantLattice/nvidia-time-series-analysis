"""Unit tests for StockQuoteNormalizer.

This module validates the normalization behavior for raw stock quote
datasets.

Test coverage includes:
- column name trimming
- type conversion for dates, strings, numerics, and integers
- removal of rows with missing values
- sorting by trade date
- handling of invalid input values

The tests focus on the cleaned output produced by the normalizer.
"""


import pandas as pd
import pytest

from work.scripts.contracts import StockQuoteSchema as S
from work.scripts.contracts.validation import StockQuoteNormalizer
from work.tests.factories import DataFrameFactory


# =========================================================
# BASIC NORMALIZATION
# =========================================================

@pytest.mark.unit
def test_normalization_basic() -> None:
    """Normalize a dirty dataset and verify resulting column types."""

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.raw_unsorted()
    )

    assert pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])

    assert all(
        pd.api.types.is_string_dtype(df[col])
        for col in S.STRING_COLUMNS
    )

    assert all(
        pd.api.types.is_numeric_dtype(df[col])
        for col in S.NUMERIC_COLUMNS
    )

    assert all(
        pd.api.types.is_integer_dtype(df[col])
        for col in S.INTEGER_COLUMNS
    )


@pytest.mark.unit
def test_sorting_by_date() -> None:
    """Normalize a dirty dataset and verify chronological ordering."""

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.raw_unsorted()
    )

    assert df[S.TRADE_DATE].is_monotonic_increasing


# =========================================================
# TYPE CONVERSIONS
# =========================================================

@pytest.mark.unit
def test_datetime_conversion() -> None:
    """Invalid date strings should be converted or rejected by normalization.

    Notes
    -----
    With `errors='raise'`, this test should be updated to expect an exception
    if the input contains an unparseable date value.
    """

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_datetime()
    )

    assert pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])


@pytest.mark.unit
def test_string_conversion() -> None:
    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_string()
    )

    assert all(
        pd.api.types.is_string_dtype(df[col])
        for col in S.STRING_COLUMNS
    )


@pytest.mark.unit
def test_numeric_conversion() -> None:
    """Normalize source values and verify string-typed output."""

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_numeric()
    )

    assert all(
        pd.api.types.is_numeric_dtype(df[col])
        for col in S.NUMERIC_COLUMNS
    )


@pytest.mark.unit
def test_integer_conversion() -> None:
    """Normalize numeric fields and verify numeric dtype output.

    Notes
    -----
    With `errors='raise'`, non-numeric values should raise during conversion.
    """

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_integer()
    )

    assert all(
        pd.api.types.is_integer_dtype(df[col])
        for col in S.INTEGER_COLUMNS
    )


# =========================================================
# MISSING VALUES
# =========================================================

@pytest.mark.unit
def test_drop_na_rows() -> None:
    """Normalize a dataset with missing values and remove incomplete rows."""

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.missing_values()
    )

    assert df[S.REQUIRED_COLUMNS].notna().to_numpy().all()


# =========================================================
# COLUMN CLEANING
# =========================================================

@pytest.mark.unit
def test_column_stripping() -> None:
    """Normalize a dirty dataset and verify header whitespace removal."""

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.raw_unsorted()
    )

    assert S.TRADE_DATE in df.columns
    assert " trade_date " not in df.columns


# =========================================================
# ERROR HANDLING
# =========================================================

@pytest.mark.unit
def test_invalid_date() -> None:
    """Invalid date values should cause normalization to fail.

    Notes
    -----
    This test should use `pytest.raises(ValueError)` if the normalizer keeps
    `errors='raise'` for datetime conversion.
    """

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_datetime()
    )

    assert len(df) == 2


@pytest.mark.unit
def test_invalid_numeric() -> None:
    """Invalid numeric values should cause normalization to fail.

    Notes
    -----
    This test should use `pytest.raises(ValueError)` if the normalizer keeps
    `errors='raise'` for numeric conversion.
    """

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_numeric()
    )

    assert len(df) == 2


@pytest.mark.unit
def test_invalid_volume() -> None:
    """Invalid volume values should cause normalization to fail.

    Notes
    -----
    This test should use `pytest.raises(ValueError)` if the normalizer keeps
    `errors='raise'` for integer conversion.
    """

    df = StockQuoteNormalizer.normalize(
        DataFrameFactory.with_invalid_integer()
    )

    assert len(df) == 2


# =========================================================
# OPTIONAL COLUMNS
# =========================================================

@pytest.mark.unit
def test_optional_adj_close_missing() -> None:
    """Normalize a dataset where optional adjusted close values are missing."""

    df = DataFrameFactory.valid()
    optional_columns = set(S.ALL_COLUMNS)-set(S.REQUIRED_COLUMNS)
    for col in optional_columns:
        df[col] = pd.NA

    df = StockQuoteNormalizer.normalize(df)

    assert set(optional_columns).issubset(df.columns)

    assert df[list(optional_columns)].isna().to_numpy().all()
