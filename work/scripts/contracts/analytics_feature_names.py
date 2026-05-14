"""
Standardized feature name registry for analytical pipeline.

This module defines centralized naming conventions for all derived
features used throughout the analytics system, including:

- return-based metrics;
- categorical analytical labels;
- moving averages;
- momentum indicators;
- volatility measures;
- technical analysis indicators.
"""


class AnalyticsFeatureNames:
    """
    Central registry of analytical feature names.

    This class provides:
    - static feature identifiers;
    - grouped feature namespaces;
    - base names for parameterized indicators;
    - helper methods for generating standardized feature names.

    Notes
    -----
    Dynamic analytical features should always be generated using
    the provided builder methods instead of manually formatting
    strings inside feature generators.
    """

    # ==========================================
    # STATIC FEATURES
    # ==========================================

    DAILY_RETURN = "daily_return"
    LOG_RETURN = "log_return"
    CUMULATIVE_RETURN = "cumulative_return"
    ROLLING_RETURN_BASE = "rolling_return"

    # ==========================================
    # CATEGORICAL FEATURES
    # ==========================================

    PRICE_TREND = "price_trend"
    RETURN_SIGN = "return_sign"
    VOLATILITY_REGIME = "volatility_regime"
    VOLUME_REGIME = "volume_regime"

    # ==========================================
    # MOVING AVERAGES
    # ==========================================

    SMA_BASE = "sma"
    EMA_BASE = "ema"
    VWMA_BASE = "vwma"

    # ==========================================
    # MOMENTUM / OSCILLATORS
    # ==========================================

    RSI_BASE = "rsi"
    MOMENTUM_BASE = "momentum"

    # ==========================================
    # VOLATILITY
    # ==========================================

    VOLATILITY_BASE = "volatility"

    # ==========================================
    # MACD
    # ==========================================

    MACD = "macd"
    MACD_SIGNAL = "macd_signal"
    MACD_HISTOGRAM = "macd_histogram"

    # ==========================================
    # BOLLINGER BANDS
    # ==========================================

    BOLLINGER_MIDDLE_BASE = "bollinger_middle"
    BOLLINGER_UPPER_BASE = "bollinger_upper"
    BOLLINGER_LOWER_BASE = "bollinger_lower"
    BOLLINGER_BANDWIDTH_BASE = "bollinger_bandwidth"
    BOLLINGER_PERCENT_B_BASE = "bollinger_percent_b"

    # ==========================================
    # FEATURE BUILDERS
    # ==========================================

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

    @classmethod
    def rsi(cls, window: int, method: str) -> str:
        """
        Construct Relative Strength Index feature name.

        Parameters
        ----------
        window : int
            RSI window size.

        method : str
            Calculation method identifier (e.g. "wilder").

        Returns
        -------
        str
            Feature name in format:
            ``rsi_{method}_{window}``.
        """

        return f"{cls.RSI_BASE}_{method}_{window}"

    @classmethod
    def volatility(cls, window: int) -> str:
        """
        Construct volatility feature name.

        Parameters
        ----------
        window : int
            Rolling window size.

        Returns
        -------
        str
            Feature name in format: ``volatility_{window}``.
        """

        return f"{cls.VOLATILITY_BASE}_{window}"

    @classmethod
    def momentum(cls, window: int) -> str:
        """
        Construct momentum feature name.

        Parameters
        ----------
        window : int
            Window size.

        Returns
        -------
        str
            Feature name in format: ``momentum_{window}``.
        """

        return f"{cls.MOMENTUM_BASE}_{window}"

    @classmethod
    def bollinger_middle(cls, window: int) -> str:
        """
        Construct Bollinger Bands middle line feature name.

        Parameters
        ----------
        window : int
            Rolling window size used for the SMA baseline.

        Returns
        -------
        str
            Feature name in format:
            ``bollinger_middle_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.bollinger_middle(20)
        'bollinger_middle_20'
        """

        return f"{cls.BOLLINGER_MIDDLE_BASE}_{window}"

    @classmethod
    def bollinger_upper(cls, window: int) -> str:
        """
        Construct Bollinger Bands upper band feature name.

        Parameters
        ----------
        window : int
            Rolling window size used for band calculation.

        Returns
        -------
        str
            Feature name in format:
            ``bollinger_upper_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.bollinger_upper(20)
        'bollinger_upper_20'
        """

        return f"{cls.BOLLINGER_UPPER_BASE}_{window}"

    @classmethod
    def bollinger_lower(cls, window: int) -> str:
        """
        Construct Bollinger Bands lower band feature name.

        Parameters
        ----------
        window : int
            Rolling window size used for band calculation.

        Returns
        -------
        str
            Feature name in format:
            ``bollinger_lower_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.bollinger_lower(20)
        'bollinger_lower_20'
        """

        return f"{cls.BOLLINGER_LOWER_BASE}_{window}"

    @classmethod
    def bollinger_bandwidth(cls, window: int) -> str:
        """
        Construct Bollinger Bands bandwidth feature name.

        Parameters
        ----------
        window : int
            Rolling window size used for band calculation.

        Returns
        -------
        str
            Feature name in format:
            ``bollinger_bandwidth_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.bollinger_bandwidth(20)
        'bollinger_bandwidth_20'
        """

        return f"{cls.BOLLINGER_BANDWIDTH_BASE}_{window}"

    @classmethod
    def bollinger_percent_b(cls, window: int) -> str:
        """
        Construct Bollinger Bands %B feature name.

        Parameters
        ----------
        window : int
            Rolling window size used for band calculation.

        Returns
        -------
        str
            Feature name in format:
            ``bollinger_percent_b_{window}``.

        Examples
        --------
        >>> AnalyticsFeatureNames.bollinger_percent_b(20)
        'bollinger_percent_b_20'
        """

        return f"{cls.BOLLINGER_PERCENT_B_BASE}_{window}"
