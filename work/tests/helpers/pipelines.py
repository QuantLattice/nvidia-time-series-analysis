"""Test pipeline utilities for ETL validation.

This module provides a simplified execution wrapper for the full
data processing pipeline used in the application:

    normalization → validation → output

It is intended for testing purposes only and should not be used
in production code.
"""


import pandas as pd

from work.scripts.contracts.validation import (
    StockQuoteNormalizer,
    StockQuoteValidator,
)


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Execute full ETL pipeline on input DataFrame.

    This function performs the complete transformation pipeline used in
    the application logic:

    1. Normalize raw input data (cleaning, type conversion, sorting)
    2. Validate schema and business rules
    3. Return cleaned DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        Raw input DataFrame (typically fixture or CSV-like data).

    Returns
    -------
    pd.DataFrame
        Clean and validated DataFrame ready for analytical use.

    Raises
    ------
    ValueError
        If normalization or validation fails.

    Notes
    -----
    This helper is primarily intended for integration testing of the ETL
    pipeline and should not be used in production services.
    """

    cleaned = StockQuoteNormalizer.normalize(df)
    StockQuoteValidator.validate(cleaned)
    return cleaned
