"""
Dataclass contracts for autocorrelation analysis.

This module defines the configuration and result dataclasses
used by the autocorrelation and partial autocorrelation
analysis functions.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
import pandas as pd

from work.scripts.analytics.constants import (
    AUTOCORRELATION_DEFAULT_ALPHA,
    AUTOCORRELATION_DEFAULT_FFT,
    AUTOCORRELATION_DEFAULT_MAX_LAG,
    AUTOCORRELATION_DEFAULT_MIN_LENGTH,
    AUTOCORRELATION_DEFAULT_PACF_METHOD,
    PACFMethod,
)


@dataclass(frozen=True)
class AutocorrelationConfig:
    """
    Configuration parameters for autocorrelation analysis.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    max_lag : int, default=AUTOCORRELATION_DEFAULT_MAX_LAG
        Maximum lag included in ACF and PACF computation.

    alpha : float, default=AUTOCORRELATION_DEFAULT_ALPHA
        Significance level used for confidence interval
        estimation.

    fft : bool, default=AUTOCORRELATION_DEFAULT_FFT
        Whether to use FFT acceleration during ACF computation.

    pacf_method : PACFMethod,
        default=AUTOCORRELATION_DEFAULT_PACF_METHOD
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

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    values : pd.Series
        Autocorrelation coefficients indexed by lag.

    confidence_intervals : pd.DataFrame
        Confidence intervals associated with each lag.

    alpha : float
        Significance level used for confidence interval
        estimation.
    """

    values: pd.Series
    confidence_intervals: pd.DataFrame
    alpha: float


@dataclass(frozen=True)
class PartialAutocorrelationResult:
    """
    Result container for partial autocorrelation analysis.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Attributes
    ----------
    values : pd.Series
        Partial autocorrelation coefficients indexed by lag.

    confidence_intervals : pd.DataFrame
        Confidence intervals associated with each lag.

    alpha : float
        Significance level used for confidence interval
        estimation.
    """

    values: pd.Series
    confidence_intervals: pd.DataFrame
    alpha: float
