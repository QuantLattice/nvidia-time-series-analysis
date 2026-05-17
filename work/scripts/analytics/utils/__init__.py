"""
Shared utility helpers for the analytics pipeline.

This package contains lightweight reusable utilities used across
statistical analysis, feature engineering, and time-series diagnostics.

Included utilities
------------------
Series helpers
    Functions for resolving Series metadata, validation,
    preprocessing, and statistical test preparation.
"""


from .series import (
    resolve_series_name,
    prepare_series_for_statistical_testing
)


__all__ = [
    "resolve_series_name",
    "prepare_series_for_statistical_testing"
]
