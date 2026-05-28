"""
Categorical feature engineering utilities.

This module provides tools for generating categorical analytical
features from continuous market data such as returns, volatility,
and trading volume.

The generated categories can be used for:
- exploratory data analysis;
- regime detection;
- visualization and reporting;
- machine learning classification targets;
- feature discretization pipelines.
"""


from dataclasses import dataclass
from typing import Optional
from enum import StrEnum
import numpy as np
import pandas as pd

from work.scripts.analytics.constants import (
    CATEGORY_HIGH_QUANTILE,
    CATEGORY_LOW_QUANTILE,
    PRICE_TREND_EPSILON,
    RETURN_STRONG_THRESHOLD,
)
from work.scripts.contracts import AnalyticsFeatureNames as FN


class CategoricalLabels(StrEnum):
    """
    Standard categorical labels used in analytics pipelines.

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

    Parameters
    ----------
    price_trend_epsilon : float, default=PRICE_TREND_EPSILON
        Threshold used to classify price trend direction.

    strong_return_threshold : float, default=RETURN_STRONG_THRESHOLD
        Absolute return threshold used to classify strong returns.

    low_quantile : float, default=CATEGORY_LOW_QUANTILE
        Lower quantile boundary for regime classification.

    high_quantile : float, default=CATEGORY_HIGH_QUANTILE
        Upper quantile boundary for regime classification.
    """

    price_trend_epsilon: float = PRICE_TREND_EPSILON
    strong_return_threshold: float = RETURN_STRONG_THRESHOLD
    low_quantile: float = CATEGORY_LOW_QUANTILE
    high_quantile: float = CATEGORY_HIGH_QUANTILE


class CategoricalFeatureGenerator:
    """
    Generate categorical analytical features from continuous data.

    The generator converts numerical analytical metrics into discrete
    categorical labels suitable for downstream analysis, dashboards,
    and machine learning workflows.

    Generated features include:
    - price trend direction;
    - return sign and strength;
    - volatility regimes;
    - volume regimes.

    Parameters
    ----------
    config : Optional[CategoricalFeatureConfig], optional
        Configuration object controlling classification thresholds
        and quantile boundaries.
    """

    def __init__(
        self,
        config: Optional[CategoricalFeatureConfig] = None
    ) -> None:
        """
        Initialize categorical feature generator.

        Parameters
        ----------
        config : Optional[CategoricalFeatureConfig], optional
            Configuration object for categorical thresholds
            and quantile boundaries.
        """

        self.config = config or CategoricalFeatureConfig()

    def apply(
        self,
        df: pd.DataFrame,
        daily_return_column: str,
        volatility_column: str,
        volume_column: str
    ) -> pd.DataFrame:
        """
        Generate categorical analytical features.

        Parameters
        ----------
        df : pd.DataFrame
            Source analytical dataset.

        daily_return_column : str
            Name of the daily return feature column.

        volatility_column : str
            Name of the volatility feature column.

        volume_column : str
            Name of the trading volume column.

        Returns
        -------
        pd.DataFrame
            Copy of the input DataFrame enriched with categorical
            analytical features.
        """

        result = df.copy()

        result[FN.PRICE_TREND] = self.price_trend(
            series=result[daily_return_column]
        )

        result[FN.RETURN_SIGN] = self.return_sign(
            series=result[daily_return_column]
        )

        result[FN.VOLATILITY_REGIME] = self.volatility_regime(
            series=result[volatility_column]
        )

        result[FN.VOLUME_REGIME] = self.volume_regime(
            series=result[volume_column]
        )

        return result

    def price_trend(
        self,
        series: pd.Series,
    ) -> pd.Series:
        """
        Classify price trend direction.

        Parameters
        ----------
        series : pd.Series
            Series containing return values.

        Returns
        -------
        pd.Series
            Series containing:
            - ``up``
            - ``down``
            - ``flat``
        """

        trend = np.select(
            condlist=[
                series > self.config.price_trend_epsilon,
                series < -self.config.price_trend_epsilon
            ],
            choicelist=[
                CategoricalLabels.TREND_UP,
                CategoricalLabels.TREND_DOWN
            ],
            default=CategoricalLabels.TREND_FLAT,
        )

        return pd.Series(
            data=trend,
            index=series.index,
            name=FN.PRICE_TREND
        )

    def return_sign(
        self,
        series: pd.Series
    ) -> pd.Series:
        """
        Categorize returns by direction and strength.

        Parameters
        ----------
        series : pd.Series
            Series containing return values.

        Returns
        -------
        pd.Series
            Series containing:
            - ``strong_up``
            - ``up``
            - ``flat``
            - ``down``
            - ``strong_down``
            - ``unknown``
        """

        strong = self.config.strong_return_threshold

        sign = np.select(
            condlist=[
                series >= strong,
                (series > 0) & (series < strong),
                series == 0,
                (series < 0) & (series > -strong),
                series <= -strong,
            ],
            choicelist=[
                CategoricalLabels.STRONG_UP,
                CategoricalLabels.UP,
                CategoricalLabels.FLAT,
                CategoricalLabels.DOWN,
                CategoricalLabels.STRONG_DOWN
            ],
            default=CategoricalLabels.UNKNOWN
        )

        return pd.Series(
            data=sign,
            index=series.index,
            name=FN.RETURN_SIGN
        )

    def volatility_regime(
        self,
        series: pd.Series
    ) -> pd.Series:
        """
        Classify volatility regimes using quantile bucketing.

        Parameters
        ----------
        series : pd.Series
            Volatility feature series.

        Returns
        -------
        pd.Series
            Volatility regime labels:
            - ``low``
            - ``medium``
            - ``high``
        """

        regime = self._bucket_by_quantiles(
            series=series,
            low_label=CategoricalLabels.LOW,
            mid_label=CategoricalLabels.MEDIUM,
            high_label=CategoricalLabels.HIGH
        )

        return pd.Series(
            data=regime,
            index=series.index,
            name=FN.VOLATILITY_REGIME
        )

    def volume_regime(
        self,
        series: pd.Series
    ) -> pd.Series:
        """
        Classify volume regimes using quantile bucketing.

        Parameters
        ----------
        series : pd.Series
            Volume feature series.

        Returns
        -------
        pd.Series
            Volume regime labels:
            - ``low``
            - ``medium``
            - ``high``
        """

        regime = self._bucket_by_quantiles(
            series=series,
            low_label=CategoricalLabels.LOW,
            mid_label=CategoricalLabels.MEDIUM,
            high_label=CategoricalLabels.HIGH
        )

        return pd.Series(
            data=regime,
            index=series.index,
            name=FN.VOLUME_REGIME
        )

    def _bucket_by_quantiles(
        self,
        series: pd.Series,
        low_label: str,
        mid_label: str,
        high_label: str
    ) -> pd.Series:
        """
        Split a numerical series into quantile-based categories.

        Parameters
        ----------
        series : pd.Series
            Numerical series to classify.

        low_label : str
            Label assigned to values below or equal to the lower quantile.

        mid_label : str
            Label assigned to middle-range values.

        high_label : str
            Label assigned to values above the upper quantile.

        Returns
        -------
        pd.Series
            Categorized series based on quantile ranges.

        Notes
        -----
        If quantile computation is invalid (NaN or overlapping
        boundaries), the entire series is assigned the middle label.
        """

        low_q = series.quantile(q=self.config.low_quantile)
        high_q = series.quantile(q=self.config.high_quantile)

        if pd.isna(obj=low_q) or pd.isna(obj=high_q) or low_q >= high_q:
            return pd.Series(
                data=mid_label,
                index=series.index,
                dtype=object
            )

        return pd.Series(
            np.select(
                condlist=[
                    series <= low_q,
                    (series > low_q) & (series <= high_q),
                    series > high_q,
                ],
                choicelist=[
                    low_label,
                    mid_label,
                    high_label,
                ],
                default=CategoricalLabels.UNKNOWN,
            ),
            index=series.index,
            dtype=object,
        )
