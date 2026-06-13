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

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


class AnalyticsFeatureNames:
    """
    Central registry of analytical feature names.

    This class provides:
    - static feature identifiers;
    - grouped feature namespaces;
    - base names for parameterized indicators;
    - helper methods for generating standardized feature names.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
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
        """Return column name for rolling return with given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.ROLLING_RETURN_BASE}_{window}"

    @classmethod
    def sma(cls, window: int) -> str:
        """Return column name for SMA with the given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.SMA_BASE}_{window}"

    @classmethod
    def ema(cls, window: int) -> str:
        """Return column name for EMA with the given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.EMA_BASE}_{window}"

    @classmethod
    def vwma(cls, window: int) -> str:
        """Return column name for VWMA with the given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.VWMA_BASE}_{window}"

    @classmethod
    def rsi(cls, window: int, method: str) -> str:
        """Return column name for RSI with given window and method.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.RSI_BASE}_{method}_{window}"

    @classmethod
    def volatility(cls, window: int) -> str:
        """Return column name for volatility with the given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.VOLATILITY_BASE}_{window}"

    @classmethod
    def momentum(cls, window: int) -> str:
        """Return column name for momentum with the given window.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.MOMENTUM_BASE}_{window}"

    @classmethod
    def bollinger_middle(cls, window: int) -> str:
        """Return column name for Bollinger middle band.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.BOLLINGER_MIDDLE_BASE}_{window}"

    @classmethod
    def bollinger_upper(cls, window: int) -> str:
        """Return column name for Bollinger upper band.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.BOLLINGER_UPPER_BASE}_{window}"

    @classmethod
    def bollinger_lower(cls, window: int) -> str:
        """Return column name for Bollinger lower band.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.BOLLINGER_LOWER_BASE}_{window}"

    @classmethod
    def bollinger_bandwidth(cls, window: int) -> str:
        """Return column name for Bollinger bandwidth.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.BOLLINGER_BANDWIDTH_BASE}_{window}"

    @classmethod
    def bollinger_percent_b(cls, window: int) -> str:
        """Return column name for Bollinger percent B.

        Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
        """

        return f"{cls.BOLLINGER_PERCENT_B_BASE}_{window}"
