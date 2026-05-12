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
    - static feature identifiers;
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

    VWMA_BASE = "vwma"

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
            Feature name in format:
            ``rolling_return_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.rolling_return(5)
        'rolling_return_5'
        """

        return f"{cls.ROLLING_RETURN_BASE}_{window}"

    @classmethod
    def sma(cls, window: int) -> str:
        """
        Construct simple moving average feature name.

        Parameters
        ----------
        window : int
            Moving average window size.

        Returns
        -------
        str
            Feature name in format:
            ``sma_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.sma(20)
        'sma_20'
        """

        return f"{cls.SMA_BASE}_{window}"

    @classmethod
    def ema(cls, window: int) -> str:
        """
        Construct exponential moving average feature name.

        Parameters
        ----------
        window : int
            Moving average window size.

        Returns
        -------
        str
            Feature name in format:
            ``ema_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.ema(10)
        'ema_10'
        """

        return f"{cls.EMA_BASE}_{window}"

    @classmethod
    def vwma(cls, window: int) -> str:
        """
        Construct volume-weighted moving average feature name.

        Parameters
        ----------
        window : int
            Moving average window size.

        Returns
        -------
        str
            Feature name in format: ``vwma_{window}``.
        """

        return f"{cls.VWMA_BASE}_{window}"
