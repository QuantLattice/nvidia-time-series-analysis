"""
Forecasting model configuration layer.

This package defines strongly-typed configuration objects
for different forecasting models used in the pipeline.

It provides standardized parameter containers for:
- naive baselines;
- moving average models;
- ARIMA family models;
- SARIMAX models.

These configurations are used to ensure:
- type-safe model specification;
- reproducible forecasting setups;
- consistent model initialization across pipelines.
"""


from .model_configs import (
    NaiveConfig,
    MovingAverageConfig,
    ARIMAConfig,
    SARIMAXConfig,
    ForecastModelConfig
)


__all__ = [
    "NaiveConfig",
    "MovingAverageConfig",
    "ARIMAConfig",
    "SARIMAXConfig",
    "ForecastModelConfig"
]
