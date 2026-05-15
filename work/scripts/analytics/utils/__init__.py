"""
Utility helpers for analytics pipeline.

This package contains small reusable helpers used across the analytics
stack, including series metadata resolution and related convenience
functions.
"""


from .series import resolve_series_name


__all__ = [
    "resolve_series_name"
]
