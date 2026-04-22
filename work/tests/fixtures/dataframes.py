"""Pandas DataFrame fixtures for testing StockQuote pipeline.

This module defines synthetic datasets used to test:
- Data normalization logic
- Validation rules
- ETL pipeline correctness
- Schema consistency

Two datasets are provided:
- valid_df: clean, correctly formatted dataset
- raw_df: intentionally dirty dataset simulating real-world CSV input
"""


import pandas as pd
import pytest
from work.scripts.contracts import StockQuoteSchema as S


@pytest.fixture
def valid_df():
    """Return a clean, schema-compliant StockQuote DataFrame.

    This dataset represents correctly formatted and ordered stock data
    that should pass all validation rules without errors.
    """

    return pd.DataFrame({
        S.TRADE_DATE: pd.to_datetime(["2024-01-01", "2024-01-02"]),
        S.SOURCE: [
            "https://example.com/nvda/2024-01-01",
            "https://example.com/nvda/2024-01-02",
        ],
        S.OPEN_PRICE: [100.0, 101.0],
        S.HIGH_PRICE: [110.0, 111.0],
        S.LOW_PRICE: [90.0, 91.0],
        S.CLOSE_PRICE: [105.0, 106.0],
        S.ADJ_CLOSE_PRICE: [105.0, 106.0],
        S.VOLUME: [1000, 2000],
    })


@pytest.fixture
def raw_df():
    """Return a dirty, unprocessed CSV-like DataFrame.

    This dataset simulates real-world input conditions:
    - inconsistent column formatting
    - string-encoded numeric values
    - unsorted rows
    - leading/trailing whitespace in column names

    It is used to test normalization and validation pipeline robustness.
    """

    return pd.DataFrame({
        " trade_date ": ["2024-01-02", "2024-01-01"],  # spaces + unsorted
        " source ": [
            "https://example.com/nvda/2024-01-02",
            "https://example.com/nvda/2024-01-01",
        ],
        "open_price": ["100", "101"],
        "high_price": ["110", "111"],
        "low_price": ["90", "91"],
        "close_price": ["105", "106"],
        "adj_close_price": ["105", "106"],
        "volume": ["1000", "2000"],
    })
