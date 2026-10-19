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


from typing import Optional, cast
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf  # type: ignore
from numpy.typing import NDArray
import numpy as np

from work.scripts.analytics.constants import (
    AUTOCORRELATION_ACF_SERIES_NAME,
    AUTOCORRELATION_CI_LOWER_COLUMN,
    AUTOCORRELATION_CI_UPPER_COLUMN,
    AUTOCORRELATION_LAG_INDEX_NAME,
    AUTOCORRELATION_PACF_SERIES_NAME,
)
from work.scripts.analytics.utils import (
    prepare_series_for_statistical_testing,
)
from work.scripts.analytics.ts.autocorrelation_contracts import (
    AutocorrelationConfig,
    AutocorrelationResult,
    PartialAutocorrelationResult,
)


def autocorrelation_series(
    series: pd.Series,
    config: Optional[AutocorrelationConfig] = None
) -> AutocorrelationResult:
    """
    Compute autocorrelation coefficients for a time series.

    The autocorrelation function (ACF) measures the linear
    dependency between observations and their lagged values.

    Parameters
    ----------
    series : pd.Series
        Input time series.

    config : Optional[AutocorrelationConfig], optional
        Configuration controlling lag selection, confidence
        interval estimation, and computation settings.

    Returns
    -------
    AutocorrelationResult
        Object containing autocorrelation coefficients and
        confidence intervals.

    Raises
    ------
    ValueError
        If the cleaned series contains fewer observations than
        required.

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

    The partial autocorrelation function (PACF) measures the
    direct relationship between observations separated by a given
    lag while controlling for intermediate lags.

    Parameters
    ----------
    series : pd.Series
        Input time series.

    config : Optional[AutocorrelationConfig], optional
        Configuration controlling lag selection, estimation
        method, and confidence interval settings.

    Returns
    -------
    PartialAutocorrelationResult
        Object containing partial autocorrelation coefficients
        and confidence intervals.

    Raises
    ------
    ValueError
        If the cleaned series contains fewer observations than
        required.

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
