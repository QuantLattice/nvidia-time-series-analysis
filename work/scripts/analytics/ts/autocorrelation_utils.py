"""
Utility functions for autocorrelation analysis.

This module provides helpers for interpreting and summarizing
the results of ACF and PACF computations, including:

- strongest lag identification;
- significant lag detection.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


import pandas as pd

from work.scripts.analytics.constants import (
    AUTOCORRELATION_CI_LOWER_COLUMN,
    AUTOCORRELATION_CI_UPPER_COLUMN,
)
from work.scripts.analytics.ts.autocorrelation_contracts import (
    AutocorrelationResult,
    PartialAutocorrelationResult,
)


def strongest_autocorrelation_lag(
    result: AutocorrelationResult,
    exclude_zero_lag: bool = True
) -> int:
    """
    Identify the lag with the strongest autocorrelation magnitude.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    result : AutocorrelationResult
        Autocorrelation analysis result.

    exclude_zero_lag : bool, default=True
        Whether to exclude lag zero from the search.

    Returns
    -------
    int
        Lag index with the largest absolute autocorrelation
        value.

    Notes
    -----
    Lag zero is typically excluded because it always has perfect
    autocorrelation.
    """

    values = result.values.copy()

    if exclude_zero_lag and 0 in values.index:
        values = values.drop(index=0)

    return int(values.abs().idxmax())


def strongest_partial_autocorrelation_lag(
    result: PartialAutocorrelationResult,
    exclude_zero_lag: bool = True
) -> int:
    """
    Identify the lag with the strongest partial autocorrelation.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    result : PartialAutocorrelationResult
        Partial autocorrelation analysis result.

    exclude_zero_lag : bool, default=True
        Whether to exclude lag zero from the search.

    Returns
    -------
    int
        Lag index with the largest absolute partial
        autocorrelation value.
    """

    values = result.values.copy()

    if exclude_zero_lag and 0 in values.index:
        values = values.drop(index=0)

    return int(values.abs().idxmax())


def significant_autocorrelation_lags(
    result: AutocorrelationResult
) -> pd.Series:
    """
    Detect statistically significant autocorrelation lags.

    A lag is considered significant when its confidence interval
    does not include zero.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    result : AutocorrelationResult
        Autocorrelation analysis result.

    Returns
    -------
    pd.Series
        Boolean mask indexed by lag indicating statistical
        significance.
    """

    ci = result.confidence_intervals

    return (
        (ci[AUTOCORRELATION_CI_LOWER_COLUMN] > 0) |
        (ci[AUTOCORRELATION_CI_UPPER_COLUMN] < 0)
    )


def significant_partial_autocorrelation_lags(
    result: PartialAutocorrelationResult
) -> pd.Series:
    """
    Detect statistically significant partial autocorrelation lags.

    A lag is considered significant when its confidence interval
    does not include zero.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    result : PartialAutocorrelationResult
        Partial autocorrelation analysis result.

    Returns
    -------
    pd.Series
        Boolean mask indexed by lag indicating statistical
        significance.
    """

    ci = result.confidence_intervals

    return (
        (ci[AUTOCORRELATION_CI_LOWER_COLUMN] > 0) |
        (ci[AUTOCORRELATION_CI_UPPER_COLUMN] < 0)
    )
