"""
Contracts for categorical feature engineering.

This module defines the enumeration of standard categorical
labels and the configuration dataclass used by the categorical
feature generator.

Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.
"""


from dataclasses import dataclass
from enum import StrEnum

from work.scripts.analytics.constants import (
    CATEGORY_HIGH_QUANTILE,
    CATEGORY_LOW_QUANTILE,
    PRICE_TREND_EPSILON,
    RETURN_STRONG_THRESHOLD,
)


class CategoricalLabels(StrEnum):
    """
    Standard categorical labels used in analytics pipelines.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Categories are grouped by analytical domain:
    - price trend direction;
    - return strength/sign;
    - volatility and volume regimes.
    """

    # =========================
    # PRICE TREND
    # =========================

    TREND_UP = "up"
    TREND_DOWN = "down"
    TREND_FLAT = "flat"

    # =========================
    # RETURN SIGN
    # =========================

    STRONG_UP = "strong_up"
    UP = "up"
    FLAT = "flat"
    DOWN = "down"
    STRONG_DOWN = "strong_down"
    UNKNOWN = "unknown"

    # =========================
    # VOLATILITY / VOLUME
    # =========================

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class CategoricalFeatureConfig:
    """
    Configuration for categorical feature generation.

    Авторы: Черкащенко Д.Д., Ловчиков С.О., Андреева М.А.

    Parameters
    ----------
    price_trend_epsilon : float, default=PRICE_TREND_EPSILON
        Threshold used to classify price trend direction.

    strong_return_threshold : float,
        default=RETURN_STRONG_THRESHOLD
        Absolute return threshold used to classify strong
        returns.

    low_quantile : float, default=CATEGORY_LOW_QUANTILE
        Lower quantile boundary for regime classification.

    high_quantile : float, default=CATEGORY_HIGH_QUANTILE
        Upper quantile boundary for regime classification.
    """

    price_trend_epsilon: float = PRICE_TREND_EPSILON
    strong_return_threshold: float = RETURN_STRONG_THRESHOLD
    low_quantile: float = CATEGORY_LOW_QUANTILE
    high_quantile: float = CATEGORY_HIGH_QUANTILE
