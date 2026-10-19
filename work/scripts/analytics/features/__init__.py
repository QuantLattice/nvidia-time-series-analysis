"""
Feature engineering components for analytics pipeline.

This package provides reusable generators for transforming raw
financial time-series data into structured analytical datasets.

Included feature groups
-----------------------
Returns features
    Daily, logarithmic, cumulative, and rolling returns.

Moving average features
    Simple, exponential, and volume-weighted moving averages.

Technical indicator features
    Momentum, volatility, RSI, MACD, Bollinger Bands,
    and other statistical indicators.

Categorical features
    Regime classification, trend labeling, and discretized
    analytical categories for machine learning workflows.

Exports
-------
ReturnsFeatureGenerator
    Generator for return-based analytical features.

MovingAverageFeatureGenerator
    Generator for moving average indicators.

TechnicalIndicatorConfig
    Configuration model for technical indicator generation.

TechnicalIndicatorsFeatureGenerator
    Generator for technical analysis indicators.

CategoricalFeatureConfig
    Configuration model for categorical feature generation.

CategoricalFeatureGenerator
    Generator for categorical analytical features.

CategoricalLabels
    Standard categorical labels used across the analytics pipeline.
"""


from .returns_feature_generator import ReturnsFeatureGenerator
from .moving_average_feature_generator import MovingAverageFeatureGenerator
from .technical_indicator_feature_generator import (
    TechnicalIndicatorConfig,
    TechnicalIndicatorsFeatureGenerator
)
from .categorical_contracts import (
    CategoricalFeatureConfig,
    CategoricalLabels,
)
from .categorical_features import (
    CategoricalFeatureGenerator,
)


__all__ = [
    "ReturnsFeatureGenerator",
    "MovingAverageFeatureGenerator",
    "TechnicalIndicatorConfig",
    "TechnicalIndicatorsFeatureGenerator",
    "CategoricalFeatureConfig",
    "CategoricalFeatureGenerator",
    "CategoricalLabels"
]
