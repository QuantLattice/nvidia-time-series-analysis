"""
Contracts package for standardized analytical data structures.

This package defines unified interfaces for working with financial
time-series data used throughout the application.

It provides:
- typed DataFrame wrappers;
- standardized feature naming conventions for analytics;
- shared schema definitions for stock market datasets.
"""


from .stock_quote_frame import StockQuoteFrame
from .analytics_feature_names import AnalyticsFeatureNames


__all__ = [
    "StockQuoteFrame",
    "AnalyticsFeatureNames"
]
