"""
Standardized feature name registry for analytical pipeline.

This module defines consistent naming conventions for all derived
features used in time-series analysis, including returns, rolling
metrics, and technical indicators.

Using centralized feature names ensures consistency between:
- feature engineering pipelines;
- model training datasets;
- visualization and reporting modules.
"""


class AnalyticsFeatureNames:
    """
    Central registry of feature names used in analytics.

    This class provides:
    - static feature identifiers (returns, cumulative metrics);
    - base names for dynamically generated feature families;
    - helper methods for constructing parameterized feature names.
    """

    # ==========================================
    # STATIC FEATURES
    # ==========================================

    DAILY_RETURN = "daily_return"
    LOG_RETURN = "log_return"
    CUMULATIVE_RETURN = "cumulative_return"

    # ==========================================
    # DYNAMIC FEATURE FAMILIES
    # ==========================================

    ROLLING_RETURN_BASE = "rolling_return"

    SMA_BASE = "sma"

    EMA_BASE = "ema"

    # ==============================
    # FEATURE BUILDERS
    # ==============================

    @classmethod
    def rolling_return(cls, window: int) -> str:
        """
        Construct rolling return feature name.

        Parameters
        ----------
        window : int
            Size of the rolling window.

        Returns
        -------
        str
            Feature name in format: ``rolling_return_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.rolling_return(5)
        'rolling_return_5'
        """

        return f"{cls.ROLLING_RETURN_BASE}_{window}"
