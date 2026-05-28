"""
Feature generator for technical indicators.

This module provides a configurable pipeline that enriches a price
DataFrame with classical technical analysis indicators, including:

- Relative Strength Index (RSI)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volatility (log-return based)
- Momentum

The generator is designed to be:
- reproducible (via TechnicalIndicatorConfig),
- deterministic,
- compatible with ML pipelines.
"""


from dataclasses import dataclass
from typing import Optional
import pandas as pd

from work.scripts.analytics.constants import (
    RSI_WINDOW,
    MACD_FAST_WINDOW,
    MACD_SLOW_WINDOW,
    MACD_SIGNAL_WINDOW,
    BOLLINGER_WINDOW,
    BOLLINGER_NUM_STD,
    VOLATILITY_WINDOW,
    MOMENTUM_WINDOW
)
from work.scripts.analytics.indicators import (
    RSIMethod,
    rsi,
    macd,
    bollinger_bands,
    volatility,
    momentum
)
from work.scripts.contracts import AnalyticsFeatureNames as FN


@dataclass(frozen=True)
class TechnicalIndicatorConfig:
    """
    Configuration for technical indicator feature generation.

    Attributes
    ----------
    rsi_window : int
        Lookback period for RSI calculation.

    rsi_method : RSIMethod
        RSI smoothing method.

    macd_fast_window : int
        Fast EMA period for MACD.

    macd_slow_window : int
        Slow EMA period for MACD.

    macd_signal_window : int
        Signal line EMA period.

    bollinger_window : int
        Rolling window for Bollinger Bands.

    bollinger_num_std : float
        Number of standard deviations for bands.

    volatility_window : int
        Window for volatility estimation.

    momentum_window : int
        Window for momentum calculation.
    """

    rsi_window: int = RSI_WINDOW
    rsi_method: RSIMethod = RSIMethod.WILDER
    macd_fast_window: int = MACD_FAST_WINDOW
    macd_slow_window: int = MACD_SLOW_WINDOW
    macd_signal_window: int = MACD_SIGNAL_WINDOW
    bollinger_window: int = BOLLINGER_WINDOW
    bollinger_num_std: float = BOLLINGER_NUM_STD
    volatility_window: int = VOLATILITY_WINDOW
    momentum_window: int = MOMENTUM_WINDOW


class TechnicalIndicatorsFeatureGenerator:
    """
    Pipeline for generating technical indicator features.

    The generator takes a price series and enriches it with
    multiple derived financial indicators.

    Notes
    -----
    This class is stateless; configuration is provided via
    TechnicalIndicatorConfig.
    """

    def __init__(
        self,
        config: Optional[TechnicalIndicatorConfig] = None
    ) -> None:
        """
        Initialize feature generator.

        Parameters
        ----------
        config : TechnicalIndicatorConfig, optional
            Indicator configuration. If None, defaults are used.
        """

        self.config = config or TechnicalIndicatorConfig()

    def apply(
        self,
        df: pd.DataFrame,
        price_column: str
    ) -> pd.DataFrame:
        """
        Apply technical indicators to input DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing price series.

        price_column : str
            Name of column containing price values.

        Returns
        -------
        pd.DataFrame
            Copy of input DataFrame with added indicator features.
        """

        result = df.copy()
        price_series = result[price_column]

        result[
            FN.rsi(
                window=self.config.rsi_window,
                method=self.config.rsi_method
            )
        ] = rsi(
            series=price_series,
            window=self.config.rsi_window,
            method=self.config.rsi_method
        )

        macd_df = macd(
            series=price_series,
            fast_window=self.config.macd_fast_window,
            slow_window=self.config.macd_slow_window,
            signal_window=self.config.macd_signal_window
        )
        result[FN.MACD] = macd_df[FN.MACD]
        result[FN.MACD_SIGNAL] = macd_df[FN.MACD_SIGNAL]
        result[FN.MACD_HISTOGRAM] = macd_df[FN.MACD_HISTOGRAM]

        bb_df = bollinger_bands(
            series=price_series,
            window=self.config.bollinger_window,
            num_std=self.config.bollinger_num_std
        )
        result[
            FN.bollinger_middle(window=self.config.bollinger_window)
        ] = bb_df[
            FN.BOLLINGER_MIDDLE_BASE
        ]
        result[
            FN.bollinger_upper(window=self.config.bollinger_window)
        ] = bb_df[
            FN.BOLLINGER_UPPER_BASE
        ]
        result[
            FN.bollinger_lower(window=self.config.bollinger_window)
        ] = bb_df[
            FN.BOLLINGER_LOWER_BASE
        ]
        result[
            FN.bollinger_bandwidth(window=self.config.bollinger_window)
        ] = bb_df[
            FN.BOLLINGER_BANDWIDTH_BASE
        ]
        result[
            FN.bollinger_percent_b(window=self.config.bollinger_window)
        ] = bb_df[
            FN.BOLLINGER_PERCENT_B_BASE
        ]

        result[
            FN.volatility(window=self.config.volatility_window)
        ] = volatility(
            series=price_series,
            window=self.config.volatility_window
        )

        result[FN.momentum(window=self.config.momentum_window)] = momentum(
            series=price_series,
            window=self.config.momentum_window
        )

        return result
