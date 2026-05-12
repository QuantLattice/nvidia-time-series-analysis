"""
Analytical indicator functions.

This package exposes reusable helpers for return-based feature
engineering and time-series calculations.
"""


from .returns import (
    daily_return,
    log_return,
    rolling_return,
    cumulative_return
)


__all__ = [
    "daily_return",
    "log_return",
    "rolling_return",
    "cumulative_return"
]
