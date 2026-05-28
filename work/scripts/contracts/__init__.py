"""
Core contracts package for analytics and forecasting systems.

This module defines shared data structures, naming conventions,
and schema contracts used across the entire analytical pipeline.

It ensures:
- consistent feature naming;
- unified dataset representations;
- type-safe model identification;
- interoperability between analytics and forecasting modules.
"""


from .stock_quote_frame import StockQuoteFrame
from .analytics_feature_names import AnalyticsFeatureNames
from .forecasting_model_names import ForecastModelName


__all__ = [
    "StockQuoteFrame",
    "AnalyticsFeatureNames",
    "ForecastModelName"
]
