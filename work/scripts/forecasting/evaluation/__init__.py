"""
Forecasting evaluation utilities.

This package provides core utilities for evaluating time-series
forecasting models, including:

- chronological train/test splitting;
- standard regression error metrics.

The module is designed for:
- backtesting pipelines;
- model benchmarking;
- forecasting validation workflows.
"""


from .splitting import (
    chronological_split,
    TrainTestSplitResult
)
from .metrics import (
    mae,
    mse,
    rmse,
    mape
)


__all__ = [
    "chronological_split",
    "TrainTestSplitResult",
    "mae",
    "mse",
    "rmse",
    "mape"
]
