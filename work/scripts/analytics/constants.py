"""
Default parameter configuration for analytics feature engineering.

This module defines standard window sizes and hyperparameters used
across the analytics pipeline.

These constants act as global defaults for:
- return-based features;
- moving averages;
- volatility and momentum indicators;
- technical indicators (RSI, MACD, Bollinger Bands).
"""


ROLLING_WINDOWS = [5, 10, 20]
SMA_WINDOWS = [5, 10, 20]
EMA_WINDOWS = [5, 10, 20]
VWMA_WINDOWS = [5, 10, 20]

RSI_WINDOW = 14

MACD_FAST_WINDOW = 12
MACD_SLOW_WINDOW = 26
MACD_SIGNAL_WINDOW = 9

BOLLINGER_WINDOW = 20
BOLLINGER_NUM_STD = 2.0

VOLATILITY_WINDOW = 20
MOMENTUM_WINDOW = 20
