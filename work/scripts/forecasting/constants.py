"""
Default configuration constants for forecasting pipeline.

This module defines global defaults used across forecasting models,
evaluation utilities, and reporting layers.

The constants provide standardized hyperparameters for:
- forecast generation;
- backtesting configuration;
- output formatting and naming conventions.

Design goals
------------
Centralized configuration ensures:
- consistent forecasting behavior across models;
- reproducible evaluation results;
- simplified experimentation and tuning;
- clear separation between logic and configuration.
"""


"""
Default name assigned to forecast output series.

Used when model predictions do not inherit a meaningful name
from the input time series.
"""
DEFAULT_FORECAST_SERIES_NAME = "forecast"

"""
Default number of future time steps for forecasting.

Used in ForecastReport when no explicit horizon is provided.
Represents a medium-term forecasting window.
"""
DEFAULT_FORECAST_HORIZON = 30

"""
Default proportion of data reserved for backtesting.

Used in chronological train/test split when no explicit ratio
is specified.

Represents a standard holdout configuration for time-series
evaluation.
"""
DEFAULT_TEST_RATIO = 0.2
