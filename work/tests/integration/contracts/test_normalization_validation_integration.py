"""Integration tests for StockQuote ETL pipeline.

This module validates the full data processing pipeline consisting of:

    raw input → normalization → validation → clean dataset

It ensures that:
- Dirty real-world data can be correctly normalized
- Schema and business rules are strictly enforced
- Edge cases and invalid inputs are properly rejected
- The system behaves consistently under integration conditions

Test Coverage
-------------
- Positive case: valid raw CSV-like data
- Schema violations (missing columns)
- Type conversion failures
- Business rule violations (OHLC logic)
- Negative values (volume constraints)
- Real-world dirty datasets
- Null value handling
"""


import pandas as pd
import pytest

from work.tests.helpers import run_pipeline
from work.scripts.contracts import StockQuoteSchema as S


# =========================================================
# POSITIVE CASE
# =========================================================

@pytest.mark.integration
def test_pipeline_valid_raw_data():
    """Pipeline should successfully process valid raw CSV-like dataset."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-02", "2024-01-01"],
        "open_price": ["100", "101"],
        "high_price": ["110", "111"],
        "low_price": ["90", "91"],
        "close_price": ["105", "106"],
        "adj_close_price": ["105", "106"],
        "volume": ["1000", "2000"],
    })

    result = run_pipeline(raw_df)

    # ---------------------------
    # FINAL DATASET GUARANTEES
    # ---------------------------
    assert pd.api.types.is_datetime64_any_dtype(result[S.TRADE_DATE])
    assert result[S.TRADE_DATE].is_monotonic_increasing
    assert result[S.VOLUME].dtype.kind in "iu"  # integer type
    assert len(result) == 2


# =========================================================
# SCHEMA VALIDATION
# =========================================================

@pytest.mark.integration
def test_pipeline_missing_column():
    """Pipeline must fail if required column is missing."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-01"],
        "open_price": ["100"],
        # missing HIGH_PRICE
        "low_price": ["90"],
        "close_price": ["105"],
        "adj_close_price": ["105"],
        "volume": ["1000"],
    })

    with pytest.raises(ValueError, match="Missing columns"):
        run_pipeline(raw_df)


# =========================================================
# TYPE VALIDATION
# =========================================================

@pytest.mark.integration
def test_pipeline_invalid_numeric():
    """Pipeline must fail if numeric conversion is not possible."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-01"],
        "open_price": ["not_a_number"],
        "high_price": ["110"],
        "low_price": ["90"],
        "close_price": ["105"],
        "adj_close_price": ["105"],
        "volume": ["1000"],
    })

    with pytest.raises(Exception):
        run_pipeline(raw_df)


# =========================================================
# BUSINESS RULES (OHLC LOGIC)
# =========================================================

@pytest.mark.integration
def test_pipeline_invalid_ohlc_logic():
    """Pipeline must reject invalid OHLC relationships."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-01"],
        "open_price": ["100"],
        "high_price": ["80"],   # invalid
        "low_price": ["90"],    # invalid: high < low
        "close_price": ["105"],
        "adj_close_price": ["105"],
        "volume": ["1000"],
    })

    with pytest.raises(ValueError, match="Invalid OHLC"):
        run_pipeline(raw_df)


# =========================================================
# BUSINESS RULES (VOLUME)
# =========================================================

@pytest.mark.integration
def test_pipeline_negative_volume():
    """Pipeline must reject negative trading volume values."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-01"],
        "open_price": ["100"],
        "high_price": ["110"],
        "low_price": ["90"],
        "close_price": ["105"],
        "adj_close_price": ["105"],
        "volume": ["-100"],
    })

    with pytest.raises(ValueError, match="Negative volume"):
        run_pipeline(raw_df)


# =========================================================
# REAL-WORLD DIRTY DATA
# =========================================================

@pytest.mark.integration
def test_pipeline_real_world_dirty_csv():
    """Pipeline should handle messy real-world CSV datasets."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-03", "2024-01-01", "2024-01-02"],
        " open_price ": ["100", "101", "102"],
        " high_price ": ["110", "111", "112"],
        " low_price ": ["90", "91", "92"],
        " close_price ": ["105", "106", "107"],
        " adj_close_price ": ["105", "106", "107"],
        " volume ": ["1000", "2000", "3000"],
    })

    result = run_pipeline(raw_df)

    assert len(result) == 3
    assert result[S.TRADE_DATE].is_monotonic_increasing


# =========================================================
# NULL HANDLING
# =========================================================

@pytest.mark.integration
def test_pipeline_null_values():
    """Pipeline must correctly handle missing values in input data."""

    raw_df = pd.DataFrame({
        " trade_date ": ["2024-01-01", None],
        "open_price": ["100", "101"],
        "high_price": ["110", "111"],
        "low_price": ["90", "91"],
        "close_price": ["105", "106"],
        "adj_close_price": ["105", "106"],
        "volume": ["1000", "2000"],
    })

    result = run_pipeline(raw_df)

    # row with null date should be dropped
    assert len(result) == 1
    assert result[S.TRADE_DATE].isna().sum() == 0
