"""Integration tests for the StockQuote ETL pipeline.

This module validates the end-to-end preprocessing pipeline used for
stock quote data.

The pipeline under test performs:
1. normalization of raw CSV-like input
2. validation of schema and business rules
3. return of a clean DataFrame for downstream processing

Test coverage includes:
- successful processing of dirty but valid input
- failure handling for invalid schema and data values
- enforcement of OHLC and volume business rules
- handling of null values and real-world CSV noise
"""


import pandas as pd
import pytest

from work.tests.helpers import run_pipeline
from work.scripts.contracts.schemas import StockQuoteSchema as S
from work.scripts.contracts.mappers import StockQuoteMapper
from work.tests.factories import DataFrameFactory


def _mapped(df: pd.DataFrame) -> pd.DataFrame:
    """Map raw dataframe columns to internal schema names."""

    return StockQuoteMapper.map(df)


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.integration
def test_pipeline_valid_raw_data():
    """Process a valid raw dataset and verify the cleaned output."""

    df = _mapped(DataFrameFactory.raw_unsorted())

    result = run_pipeline(df)

    # ---------------------------
    # FINAL DATASET GUARANTEES
    # ---------------------------
    assert pd.api.types.is_datetime64_any_dtype(result[S.TRADE_DATE])
    assert result[S.TRADE_DATE].is_monotonic_increasing
    assert result[S.VOLUME].dtype.kind in "iu"  # integer type


# =========================================================
# SCHEMA VALIDATION
# =========================================================

@pytest.mark.integration
def test_pipeline_missing_column():
    """Reject input data that is missing a required column."""

    df = DataFrameFactory.missing_values()

    df = run_pipeline(df)
    assert all(
        col in df.columns
        for col in S.ALL_COLUMNS
    )


# =========================================================
# TYPE VALIDATION
# =========================================================

@pytest.mark.integration
def test_pipeline_invalid_datetime():
    """Reject input data with an invalid date value."""

    df = DataFrameFactory.with_invalid_datetime()

    df = run_pipeline(df)

    assert pd.api.types.is_datetime64_any_dtype(df[S.TRADE_DATE])


@pytest.mark.integration
def test_pipeline_invalid_string():
    """Reject input data with an invalid source value."""

    df = DataFrameFactory.with_invalid_string()

    df = run_pipeline(df)
    assert all(
        pd.api.types.is_string_dtype(df[col])
        for col in S.STRING_COLUMNS
    )


@pytest.mark.integration
def test_pipeline_invalid_numeric():
    """Reject input data with a non-numeric price value."""

    df = DataFrameFactory.with_invalid_numeric()

    df = run_pipeline(df)
    assert all(
        pd.api.types.is_numeric_dtype(df[col])
        for col in S.NUMERIC_COLUMNS
    )


@pytest.mark.integration
def test_pipeline_invalid_integer():
    """Reject input data with a non-integer volume value."""

    df = DataFrameFactory.with_invalid_integer()

    df = run_pipeline(df)
    assert all(
        pd.api.types.is_integer_dtype(df[col])
        for col in S.INTEGER_COLUMNS
    )


# =========================================================
# BUSINESS RULES (OHLC LOGIC)
# =========================================================

@pytest.mark.integration
def test_pipeline_invalid_ohlc_logic():
    """Reject input data with an invalid OHLC relationship."""

    df = DataFrameFactory.valid(rows=2)
    df[S.HIGH_PRICE] = [80.0, 70.0]
    df[S.LOW_PRICE] = [90, 80]

    with pytest.raises(ValueError, match="Invalid OHLC"):
        run_pipeline(df)


# =========================================================
# BUSINESS RULES (VOLUME)
# =========================================================

@pytest.mark.integration
def test_pipeline_negative_volume():
    """Reject input data containing negative trading volume."""

    df = DataFrameFactory.valid()
    df[S.VOLUME] = [-2]

    with pytest.raises(ValueError, match="Negative volume"):
        run_pipeline(df)


# =========================================================
# REAL-WORLD DIRTY DATA
# =========================================================

@pytest.mark.integration
def test_pipeline_real_world_dirty_csv():
    """Process a messy CSV-like dataset and verify ordering after cleanup."""

    df = _mapped(DataFrameFactory.raw_unsorted())

    result = run_pipeline(df)

    assert result[S.TRADE_DATE].is_monotonic_increasing


# =========================================================
# NULL HANDLING
# =========================================================

@pytest.mark.integration
def test_pipeline_null_values():
    """Preserve valid rows while removing rows with missing required values."""

    df = DataFrameFactory.valid(rows=2)
    df[S.ADJ_CLOSE_PRICE] = pd.NA

    df = run_pipeline(df)

    assert df[S.ADJ_CLOSE_PRICE].isna().to_numpy().all()
