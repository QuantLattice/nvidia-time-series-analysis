"""
Series-related utility helpers for analytics.

This module provides small convenience functions for working with
pandas Series objects in the analytics pipeline.
"""


import pandas as pd

from work.scripts.analytics.constants import (
    DEFAULT_SERIES_NAME
)


def resolve_series_name(
    series: pd.Series
) -> str:
    """
    Resolve a stable name for a pandas Series.

    Parameters
    ----------
    series : pd.Series
        Input series.

    Returns
    -------
    str
        Existing series name, or a default fallback name when the
        series is unnamed.
    """

    if series.name is None:
        return DEFAULT_SERIES_NAME

    return str(series.name)
