"""
Series utility helpers for analytics workflows.

This module provides reusable helper functions for working with
``pandas.Series`` objects throughout the analytics pipeline.

The utilities focus on:
- stable series metadata handling;
- preprocessing for statistical testing;
- numeric validation and cleanup.
"""


import pandas as pd
import numpy as np

from work.scripts.analytics.constants import (
    DEFAULT_SERIES_NAME
)


def resolve_series_name(
    series: pd.Series
) -> str:
    """
    Resolve a stable display name for a pandas Series.

    This helper guarantees that analytical reports and diagnostic
    outputs always contain a valid human-readable series identifier.

    Parameters
    ----------
    series : pd.Series
        Input pandas Series.

    Returns
    -------
    str
        Series name if available; otherwise a predefined fallback name.

    Notes
    -----
    If ``series.name`` is ``None``, the function returns
    ``DEFAULT_SERIES_NAME``.
    """

    if series.name is None:
        return DEFAULT_SERIES_NAME

    return str(series.name)


def prepare_series_for_statistical_testing(series: pd.Series) -> pd.Series:
    """
    Prepare a series for statistical testing procedures.

    The function performs a standardized preprocessing pipeline used
    by statistical diagnostics and time-series testing utilities.

    Processing steps
    ----------------
    1. Convert values to numeric representation.
    2. Replace infinite values with ``NaN``.
    3. Remove missing observations.
    4. Cast the resulting series to ``float``.

    Parameters
    ----------
    series : pd.Series
        Input series to preprocess.

    Returns
    -------
    pd.Series
        Clean numeric series suitable for statistical testing.

    Raises
    ------
    ValueError
        If the resulting cleaned series contains no valid observations.

    Notes
    -----
    This helper is primarily intended for:
    - stationarity testing;
    - autocorrelation analysis;
    - statistical inference utilities.
    """

    cleaned = (
        pd.to_numeric(series, errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )

    if cleaned.empty:
        raise ValueError(
            "ADF test requires at least one valid numeric observation."
        )

    return cleaned.astype(float)
