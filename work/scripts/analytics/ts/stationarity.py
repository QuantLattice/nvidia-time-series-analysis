"""
Augmented Dickey-Fuller (ADF) stationarity test utilities.

This module provides a thin, safe wrapper around
``statsmodels.tsa.stattools.adfuller`` with:

- input validation;
- preprocessing of time series;
- structured result representation;
- explicit stationarity decision logic.

The ADF test is used to determine whether a time series is stationary,
i.e. whether it has a unit root.

Mathematical intuition
----------------------
The null hypothesis (H0) of the ADF test is that the series has a unit root
(non-stationary process). Rejection of H0 implies stationarity.
"""


from dataclasses import dataclass
from typing import Mapping, Optional, Any, Tuple, cast
import pandas as pd
from statsmodels.tsa.stattools import adfuller  # type: ignore

from work.scripts.analytics.constants import (
    ADF_DEFAULT_ALPHA,
    ADF_DEFAULT_AUTOLAG,
    ADF_DEFAULT_MAXLAG,
    ADF_DEFAULT_MIN_LENGTH,
    ADF_DEFAULT_REGRESSION,
)
from work.scripts.analytics.utils import prepare_series_for_statistical_testing


@dataclass(frozen=True)
class ADFTestConfig:
    """
    Configuration parameters for Augmented Dickey-Fuller test.

    Attributes
    ----------
    alpha : float
        Significance level for stationarity decision.

    regression : str
        Type of regression used in ADF test
        (e.g., 'c', 'ct', 'ctt', 'n').

    autolag : str
        Method used to select optimal lag length.

    maxlag : Optional[int]
        Maximum lag considered in test.

    min_length : int
        Minimum required length of cleaned time series.
    """

    alpha: float = ADF_DEFAULT_ALPHA
    regression: str = ADF_DEFAULT_REGRESSION
    autolag: str = ADF_DEFAULT_AUTOLAG
    maxlag: Optional[int] = ADF_DEFAULT_MAXLAG
    min_length: int = ADF_DEFAULT_MIN_LENGTH


@dataclass(frozen=True)
class ADFTestResult:
    """
    Result of Augmented Dickey-Fuller test.

    Attributes
    ----------
    statistic : float
        ADF test statistic.

    pvalue : float
        P-value of the test.

    used_lags : int
        Number of lags used in regression.

    nobs : int
        Number of observations used.

    critical_values : Mapping[str, float]
        Critical values for different confidence levels.

    icbest : Optional[float]
        Information criterion value (if available).

    alpha : float
        Significance level used for decision.

    is_stationary : bool
        Whether the null hypothesis was rejected.
    """

    statistic: float
    pvalue: float
    used_lags: int
    nobs: int
    critical_values: Mapping[str, float]
    icbest: Optional[float]
    alpha: float
    is_stationary: bool


def adf_test(
    series: pd.Series,
    config: Optional[ADFTestConfig] = None
) -> ADFTestResult:
    """
    Perform Augmented Dickey-Fuller stationarity test.

    Parameters
    ----------
    series : pd.Series
        Input time series.

    config : Optional[ADFTestConfig]
        Configuration object controlling test behavior.

    Returns
    -------
    ADFTestResult
        Structured ADF test result with stationarity decision.

    Raises
    ------
    ValueError
        If series is too short, constant, or invalid for testing.
    """

    config = config or ADFTestConfig()
    cleaned = prepare_series_for_statistical_testing(series)

    if len(cleaned) < config.min_length:
        raise ValueError(
            f"ADF test requires at least {config.min_length} observations; "
            f"got {len(cleaned)}."
        )

    if cleaned.nunique(dropna=True) <= 1:
        raise ValueError("ADF test cannot be applied to a constant series.")

    try:
        raw_result = adfuller(  # type: ignore
            cleaned,
            maxlag=config.maxlag,
            regression=config.regression,
            autolag=config.autolag,
            store=False,
            regresults=False,
        )
        adf_result = cast(Tuple[Any, ...], raw_result)
    except Exception as exc:
        raise ValueError(f"ADF test failed: {exc}") from exc

    if len(adf_result) == 6:
        (
            statistic,
            pvalue,
            used_lags,
            nobs,
            critical_values,
            icbest
        ) = adf_result
    elif len(adf_result) == 5:
        (
            statistic,
            pvalue,
            used_lags,
            nobs,
            critical_values
        ) = adf_result
        icbest = None
    else:
        raise ValueError(
            f"Unexpected ADF result shape: {len(adf_result)} elements."
        )

    is_stationary_result = float(pvalue) < config.alpha

    return ADFTestResult(
        statistic=float(statistic),
        pvalue=float(pvalue),
        used_lags=int(used_lags),
        nobs=int(nobs),
        critical_values=dict(critical_values),
        icbest=None if icbest is None else float(icbest),
        alpha=config.alpha,
        is_stationary=is_stationary_result,
    )
