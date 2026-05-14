"""
Feature generators for analytics pipeline.

This package exposes a unified set of feature engineering components
used to transform raw market data into structured analytical datasets.

Modules include:
- return-based features;
- moving average features;
- technical indicator features.
"""


from .returns_feature_generator import ReturnsFeatureGenerator
from .moving_average_feature_generator import MovingAverageFeatureGenerator
from .technical_indicator_feature_generator import (
    TechnicalIndicatorConfig,
    TechnicalIndicatorsFeatureGenerator
)


__all__ = [
    "ReturnsFeatureGenerator",
    "MovingAverageFeatureGenerator",
    "TechnicalIndicatorConfig",
    "TechnicalIndicatorsFeatureGenerator"
]
