"""
Feature generators for analytics pipeline.

This package exposes reusable feature engineering components that
transform raw market data into analytical datasets.
"""


from .returns_feature_generator import ReturnsFeatureGenerator


__all__ = [
    "ReturnsFeatureGenerator"
]
