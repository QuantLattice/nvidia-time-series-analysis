"""
Autocorrelation and partial autocorrelation utilities.

This module provides statistical helpers for analyzing temporal
dependencies in time-series data using:

- autocorrelation function (ACF);
- partial autocorrelation function (PACF).

These diagnostics are commonly used in:

- exploratory time-series analysis;
- autoregressive model identification;
- lag structure detection;
- seasonality analysis;
- forecasting pipeline preparation.

The implementation is built on top of
``statsmodels.tsa.stattools`` and returns pandas-native result
structures suitable for downstream analysis and visualization.
"""


from dataclasses import dataclass
from typing import Optional, cast
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf  # type: ignore
from numpy.typing import NDArray
import numpy as np

from work.scripts.analytics.constants import (
    AUTOCORRELATION_ACF_SERIES_NAME,
    AUTOCORRELATION_CI_LOWER_COLUMN,
    AUTOCORRELATION_CI_UPPER_COLUMN,
    AUTOCORRELATION_DEFAULT_ALPHA,
    AUTOCORRELATION_DEFAULT_FFT,
    AUTOCORRELATION_DEFAULT_MAX_LAG,
    AUTOCORRELATION_DEFAULT_MIN_LENGTH,
    AUTOCORRELATION_DEFAULT_PACF_METHOD,
    AUTOCORRELATION_LAG_INDEX_NAME,
    AUTOCORRELATION_PACF_SERIES_NAME,
    PACFMethod,
)
from work.scripts.analytics.utils import prepare_series_for_statistical_testing


@dataclass(frozen=True)
class AutocorrelationConfig:
    """
    Configuration parameters for autocorrelation analysis.

    Parameters
    ----------
    max_lag : int, default=AUTOCORRELATION_DEFAULT_MAX_LAG
        Maximum lag included in ACF and PACF computation.

    alpha : float, default=AUTOCORRELATION_DEFAULT_ALPHA
        Significance level used for confidence interval estimation.

    fft : bool, default=AUTOCORRELATION_DEFAULT_FFT
        Whether to use FFT acceleration during ACF computation.

    pacf_method : PACFMethod, default=AUTOCORRELATION_DEFAULT_PACF_METHOD
        Estimation method used for PACF computation.

    min_length : int, default=AUTOCORRELATION_DEFAULT_MIN_LENGTH
        Minimum required number of valid observations.
    """

    max_lag: int = AUTOCORRELATION_DEFAULT_MAX_LAG
    alpha: float = AUTOCORRELATION_DEFAULT_ALPHA
    fft: bool = AUTOCORRELATION_DEFAULT_FFT
    pacf_method: PACFMethod = AUTOCORRELATION_DEFAULT_PACF_METHOD
    min_length: int = AUTOCORRELATION_DEFAULT_MIN_LENGTH


@dataclass(frozen=True)
class AutocorrelationResult:
    """
    Result container for autocorrelation analysis.

    Attributes
    ----------
    values : pd.Series
        Autocorrelation coefficients indexed by lag.

    confidence_intervals : pd.DataFrame
        Confidence intervals associated with each lag.

    alpha : float
        Significance level used for confidence interval estimation.
    """

    values: pd.Series
    confidence_intervals: pd.DataFrame
    alpha: float


@dataclass(frozen=True)
class PartialAutocorrelationResult:
    """
    Result container for partial autocorrelation analysis.

    Attributes
    ----------
    values : pd.Series
        Partial autocorrelation coefficients indexed by lag.

    confidence_intervals : pd.DataFrame
        Confidence intervals associated with each lag.

    alpha : float
        Significance level used for confidence interval estimation.
    """

    values: pd.Series
    confidence_intervals: pd.DataFrame
    alpha: float


def autocorrelation_series(
    series: pd.Series,
    config: Optional[AutocorrelationConfig] = None
) -> AutocorrelationResult:
    """
    Compute autocorrelation coefficients for a time series.

    The autocorrelation function (ACF) measures the linear dependency
    between observations and their lagged values.

    Parameters
    ----------
    series : pd.Series
        Input time series.

    config : Optional[AutocorrelationConfig], optional
        Configuration controlling lag selection, confidence interval
        estimation, and computation settings.

    Returns
    -------
    AutocorrelationResult
        Object containing autocorrelation coefficients and confidence
        intervals.

    Raises
    ------
    ValueError
        If the cleaned series contains fewer observations than required.

    Notes
    -----
    Missing and infinite values are removed before computation.

    Examples
    --------
    >>> result = autocorrelation_series(series)
    >>> result.values.head()
    """

    config = config or AutocorrelationConfig()
    cleaned = prepare_series_for_statistical_testing(series=series)

    if len(cleaned) < config.min_length:
        raise ValueError(
            f"Autocorrelation analysis requires at \
            least {config.min_length} observations."
        )

    acf_values, confidence_intervals = cast(
        tuple[NDArray[np.float64], NDArray[np.float64]],
        acf(
            cleaned,
            nlags=config.max_lag,
            alpha=config.alpha,
            fft=config.fft,
        ),
    )

    lag_index = pd.Index(
        range(len(acf_values)),
        name=AUTOCORRELATION_LAG_INDEX_NAME,
    )

    return AutocorrelationResult(
        values=pd.Series(
            data=acf_values,
            index=lag_index,
            name=AUTOCORRELATION_ACF_SERIES_NAME,
        ),
        confidence_intervals=pd.DataFrame(
            data=confidence_intervals,
            index=lag_index,
            columns=[
                AUTOCORRELATION_CI_LOWER_COLUMN,
                AUTOCORRELATION_CI_UPPER_COLUMN,
            ],
        ),
        alpha=config.alpha,
    )


def partial_autocorrelation_series(
    series: pd.Series,
    config: Optional[AutocorrelationConfig] = None
) -> PartialAutocorrelationResult:
    """
    Compute partial autocorrelation coefficients for a time series.

    The partial autocorrelation function (PACF) measures the direct
    relationship between observations separated by a given lag while
    controlling for intermediate lags.

    Parameters
    ----------
    series : pd.Series
        Input time series.

    config : Optional[AutocorrelationConfig], optional
        Configuration controlling lag selection, estimation method,
        and confidence interval settings.

    Returns
    -------
    PartialAutocorrelationResult
        Object containing partial autocorrelation coefficients and
        confidence intervals.

    Raises
    ------
    ValueError
        If the cleaned series contains fewer observations than required.

    Notes
    -----
    Missing and infinite values are removed before computation.

    Examples
    --------
    >>> result = partial_autocorrelation_series(series)
    >>> result.values.head()
    """

    config = config or AutocorrelationConfig()
    cleaned = prepare_series_for_statistical_testing(series=series)

    if len(cleaned) < config.min_length:
        raise ValueError(
            f"Partial autocorrelation analysis requires at \
            least {config.min_length} observations."
        )

    pacf_values, confidence_intervals = cast(
        tuple[NDArray[np.float64], NDArray[np.float64]],
        pacf(
            cleaned,
            nlags=config.max_lag,
            alpha=config.alpha,
            method=config.pacf_method,
        ),
    )

    lag_index = pd.Index(
        range(len(pacf_values)),
        name=AUTOCORRELATION_LAG_INDEX_NAME,
    )

    return PartialAutocorrelationResult(
        values=pd.Series(
            data=pacf_values,
            index=lag_index,
            name=AUTOCORRELATION_PACF_SERIES_NAME,
        ),
        confidence_intervals=pd.DataFrame(
            data=confidence_intervals,
            index=lag_index,
            columns=[
                AUTOCORRELATION_CI_LOWER_COLUMN,
                AUTOCORRELATION_CI_UPPER_COLUMN,
            ],
        ),
        alpha=config.alpha,
    )


def strongest_autocorrelation_lag(
    result: AutocorrelationResult,
    exclude_zero_lag: bool = True
) -> int:
    """
    Identify the lag with the strongest autocorrelation magnitude.

    Parameters
    ----------
    result : AutocorrelationResult
        Autocorrelation analysis result.

    exclude_zero_lag : bool, default=True
        Whether to exclude lag zero from the search.

    Returns
    -------
    int
        Lag index with the largest absolute autocorrelation value.

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
    Identify the lag with the strongest partial autocorrelation magnitude.

    Parameters
    ----------
    result : PartialAutocorrelationResult
        Partial autocorrelation analysis result.

    exclude_zero_lag : bool, default=True
        Whether to exclude lag zero from the search.

    Returns
    -------
    int
        Lag index with the largest absolute partial autocorrelation value.
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

    A lag is considered significant when its confidence interval does
    not include zero.

    Parameters
    ----------
    result : AutocorrelationResult
        Autocorrelation analysis result.

    Returns
    -------
    pd.Series
        Boolean mask indexed by lag indicating statistical significance.
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

    A lag is considered significant when its confidence interval does
    not include zero.

    Parameters
    ----------
    result : PartialAutocorrelationResult
        Partial autocorrelation analysis result.

    Returns
    -------
    pd.Series
        Boolean mask indexed by lag indicating statistical significance.
    """

    ci = result.confidence_intervals

    return (
        (ci[AUTOCORRELATION_CI_LOWER_COLUMN] > 0) |
        (ci[AUTOCORRELATION_CI_UPPER_COLUMN] < 0)
    )
