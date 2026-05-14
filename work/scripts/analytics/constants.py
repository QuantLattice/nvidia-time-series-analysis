"""
Default analytical configuration constants.

This module defines standardized default parameters used across
the analytics and feature engineering pipeline.

The constants centralize commonly used hyperparameters for:
- return calculations;
- moving averages;
- momentum and volatility indicators;
- technical analysis indicators;
- categorical feature generation.

Using shared defaults ensures:
- consistency across analytical modules;
- reproducible feature generation;
- easier configuration management;
- simplified experimentation and tuning.
"""


# ==========================================
# RETURN FEATURES
# ==========================================

ROLLING_WINDOWS = [5, 10, 20]


# ==========================================
# MOVING AVERAGES
# ==========================================

SMA_WINDOWS = [5, 10, 20]
EMA_WINDOWS = [5, 10, 20]
VWMA_WINDOWS = [5, 10, 20]


# ==========================================
# TECHNICAL INDICATORS
# ==========================================

# Relative Strength Index (RSI)
RSI_WINDOW = 14

# Moving Average Convergence Divergence (MACD)
MACD_FAST_WINDOW = 12
MACD_SLOW_WINDOW = 26
MACD_SIGNAL_WINDOW = 9

# Bollinger Bands
BOLLINGER_WINDOW = 20
BOLLINGER_NUM_STD = 2.0

# Statistical indicators
VOLATILITY_WINDOW = 20
MOMENTUM_WINDOW = 20

# ==========================================
# CATEGORICAL FEATURES
# ==========================================

# Threshold used to classify flat price movement.
PRICE_TREND_EPSILON = 0.001

# Absolute return threshold used to classify strong returns.
RETURN_STRONG_THRESHOLD = 0.02

# Quantile boundaries used for regime classification.
CATEGORY_LOW_QUANTILE = 0.33
CATEGORY_HIGH_QUANTILE = 0.66
