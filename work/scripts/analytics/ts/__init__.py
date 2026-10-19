"""
Time-series statistical testing and diagnostics utilities.

The module includes:

Stationarity analysis
    Augmented Dickey-Fuller (ADF) testing utilities for detecting
    non-stationary behavior in time-series data.

Autocorrelation analysis
    Auto-correlation (ACF) and partial auto-correlation (PACF)
    utilities for identifying temporal dependencies, lag structure,
    and autoregressive behavior.

The provided functions and result objects are intended to support:

- exploratory time-series analysis;
- statistical diagnostics;
- forecasting model preparation;
- autoregressive model identification;
- feature engineering for sequential data.
"""


from .stationarity import (
    ADFTestConfig,
    ADFTestResult,
    adf_test
)
from .autocorrelation_contracts import (
    AutocorrelationConfig,
    AutocorrelationResult,
    PartialAutocorrelationResult,
)
from .autocorrelation_utils import (
    strongest_autocorrelation_lag,
    strongest_partial_autocorrelation_lag,
    significant_autocorrelation_lags,
    significant_partial_autocorrelation_lags,
)
from .autocorrelation import (
    autocorrelation_series,
    partial_autocorrelation_series,
)


__all__ = [
    "ADFTestConfig",
    "ADFTestResult",
    "adf_test",

    "AutocorrelationConfig",
    "AutocorrelationResult",
    "PartialAutocorrelationResult",
    "autocorrelation_series",
    "partial_autocorrelation_series",
    "strongest_autocorrelation_lag",
    "strongest_partial_autocorrelation_lag",
    "significant_autocorrelation_lags",
    "significant_partial_autocorrelation_lags"
]
