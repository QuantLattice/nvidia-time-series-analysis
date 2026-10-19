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


from typing import Optional
import numpy as np
import pandas as pd

from work.scripts.contracts import AnalyticsFeatureNames as FN
from work.scripts.analytics.features.categorical_contracts import (
    CategoricalFeatureConfig,
    CategoricalLabels,
)


class CategoricalFeatureGenerator:
    """
    Generate categorical analytical features from continuous data.

    Converts numerical analytical metrics into discrete categorical
    labels suitable for downstream analysis, dashboards, and
    machine learning workflows.

    Generated features include:
    - price trend direction;
    - return sign and strength;
    - volatility regimes;
    - volume regimes.
    """

    def __init__(
        self,
        config: Optional[CategoricalFeatureConfig] = None
    ) -> None:
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
            Series with labels ``up``, ``down``, or ``flat``.
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
            Series with labels ``strong_up``, ``up``, ``flat``,
            ``down``, ``strong_down``, or ``unknown``.
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
            Series with labels ``low``, ``medium``, or ``high``.
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
            Series with labels ``low``, ``medium``, or ``high``.
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
            Label for values at or below the lower quantile.

        mid_label : str
            Label for middle-range values.

        high_label : str
            Label for values above the upper quantile.

        Returns
        -------
        pd.Series
            Categorized series based on quantile ranges.

        Notes
        -----
        If quantile computation is invalid (NaN or overlapping
        boundaries), the entire series is assigned mid_label.
        """

        low_q = series.quantile(q=self.config.low_quantile)
        high_q = series.quantile(q=self.config.high_quantile)

        if (
            pd.isna(obj=low_q)
            or pd.isna(obj=high_q)
            or low_q >= high_q
        ):
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
