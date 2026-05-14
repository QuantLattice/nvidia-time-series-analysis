"""
Analytical indicator functions.

This package exposes reusable building blocks for:
- return-based features;
- moving averages;
- technical indicators (momentum, volatility, oscillators).
"""


from .returns import (
    daily_return,
    log_return,
    rolling_return,
    cumulative_return
)
from .moving_averages import (
    sma,
    ema,
    vwma
)
from .technical_indicators import (
    RSIMethod,
    rsi,
    macd,
    bollinger_bands,
    volatility,
    momentum
)


__all__ = [
    "daily_return",
    "log_return",
    "rolling_return",
    "cumulative_return",
    "sma",
    "ema",
    "vwma",
    "RSIMethod",
    "rsi",
    "macd",
    "bollinger_bands",
    "volatility",
    "momentum"
]
