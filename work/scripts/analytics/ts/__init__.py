"""
Time-series statistical testing utilities.

This module provides statistical tests and utilities specifically
designed for time-series analysis.

Currently includes:
- Augmented Dickey-Fuller (ADF) test for stationarity detection.
"""


from .stationarity import (
    ADFTestConfig,
    ADFTestResult,
    adf_test
)


__all__ = [
    "ADFTestConfig",
    "ADFTestResult",
    "adf_test"
]
