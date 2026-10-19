"""Unit tests for low-level statistical functions.

Covers: central tendency, descriptive, shape, distribution,
rolling, and correlation statistics.
"""
import math
import pytest
import pandas as pd
import numpy as np

from work.scripts.analytics.statistics.central_tendency import mean, median
from work.scripts.analytics.statistics.descriptive_statistics import (
    variance,
    std,
    data_range,
    min_value,
    max_value,
    missing_count,
    missing_ratio,
    trimmed_mean,
    mad,
    coefficient_of_variation,
)
from work.scripts.analytics.statistics.shape_statistics import (
    skewness,
    kurtosis,
    positive_ratio,
    negative_ratio,
    zero_ratio,
)
from work.scripts.analytics.statistics.distribution_statistics import (
    quantiles,
    iqr,
    outlier_bounds,
)
from work.scripts.analytics.statistics.rolling_statistics import (
    rolling_mean,
    rolling_std,
    rolling_min,
    rolling_max,
)

# ── fixtures ─────────────────────────────────────────────

S = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])   # simple ascending
S_NEG = pd.Series([-3.0, -1.0, 0.0, 1.0, 3.0])
S_NAN = pd.Series([1.0, float('nan'), 3.0, float('nan'), 5.0])


# =========================================================
# CENTRAL TENDENCY
# =========================================================

@pytest.mark.unit
def test_mean_basic() -> None:
    assert mean(S) == pytest.approx(3.0)


@pytest.mark.unit
def test_mean_single() -> None:
    assert mean(pd.Series([7.0])) == pytest.approx(7.0)


@pytest.mark.unit
def test_median_basic() -> None:
    assert median(S) == pytest.approx(3.0)


@pytest.mark.unit
def test_median_even() -> None:
    assert median(pd.Series([1.0, 2.0, 3.0, 4.0])) == pytest.approx(2.5)


# =========================================================
# DESCRIPTIVE
# =========================================================

@pytest.mark.unit
def test_variance_basic() -> None:
    assert variance(S) > 0


@pytest.mark.unit
def test_std_basic() -> None:
    assert std(S) == pytest.approx(math.sqrt(variance(S)))


@pytest.mark.unit
def test_data_range() -> None:
    assert data_range(S) == pytest.approx(4.0)


@pytest.mark.unit
def test_min_value() -> None:
    assert min_value(S) == pytest.approx(1.0)


@pytest.mark.unit
def test_max_value() -> None:
    assert max_value(S) == pytest.approx(5.0)


@pytest.mark.unit
def test_missing_count_no_nans() -> None:
    assert missing_count(S) == 0


@pytest.mark.unit
def test_missing_count_with_nans() -> None:
    assert missing_count(S_NAN) == 2


@pytest.mark.unit
def test_missing_ratio() -> None:
    assert missing_ratio(S_NAN) == pytest.approx(2 / 5)


@pytest.mark.unit
def test_trimmed_mean_reduces_extremes() -> None:
    outliers = pd.Series([1.0, 2.0, 3.0, 4.0, 100.0])
    assert trimmed_mean(outliers, trim=0.1) < mean(outliers)


@pytest.mark.unit
def test_mad_non_negative() -> None:
    assert mad(S) >= 0


@pytest.mark.unit
def test_coefficient_of_variation_positive() -> None:
    assert coefficient_of_variation(S) > 0


# =========================================================
# SHAPE
# =========================================================

@pytest.mark.unit
def test_skewness_symmetric() -> None:
    sym = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    assert abs(skewness(sym)) < 1.0


@pytest.mark.unit
def test_kurtosis_returns_float() -> None:
    assert isinstance(kurtosis(S), float)


@pytest.mark.unit
def test_positive_ratio_all_positive() -> None:
    assert positive_ratio(S) == pytest.approx(1.0)


@pytest.mark.unit
def test_negative_ratio_all_positive() -> None:
    assert negative_ratio(S) == pytest.approx(0.0)


@pytest.mark.unit
def test_zero_ratio() -> None:
    s = pd.Series([0.0, 1.0, 0.0, 2.0])
    assert zero_ratio(s) == pytest.approx(0.5)


@pytest.mark.unit
def test_positive_ratio_mixed() -> None:
    pos = positive_ratio(S_NEG)
    neg = negative_ratio(S_NEG)
    # zero is not counted in either
    assert pos + neg <= 1.0


# =========================================================
# DISTRIBUTION
# =========================================================

@pytest.mark.unit
def test_quantiles_keys() -> None:
    q = quantiles(S, probs=[0.25, 0.5, 0.75])
    assert 0.25 in q
    assert q[0.5] == pytest.approx(3.0)


@pytest.mark.unit
def test_iqr_non_negative() -> None:
    assert iqr(S) >= 0


@pytest.mark.unit
def test_outlier_bounds_order() -> None:
    bounds = outlier_bounds(S, k=1.5)
    assert bounds.lower < bounds.upper


# =========================================================
# ROLLING
# =========================================================

@pytest.mark.unit
def test_rolling_mean_length() -> None:
    result = rolling_mean(S, window=3)
    assert len(result) == len(S)


@pytest.mark.unit
def test_rolling_mean_values() -> None:
    result = rolling_mean(S, window=3)
    # Index 2 (third element): mean of [1,2,3] = 2.0
    assert result.iloc[2] == pytest.approx(2.0)


@pytest.mark.unit
def test_rolling_std_non_negative() -> None:
    result = rolling_std(S, window=3)
    assert all(v >= 0 for v in result.dropna())


@pytest.mark.unit
def test_rolling_min_values() -> None:
    result = rolling_min(S, window=2)
    assert result.iloc[2] == pytest.approx(2.0)


@pytest.mark.unit
def test_rolling_max_values() -> None:
    result = rolling_max(S, window=2)
    assert result.iloc[2] == pytest.approx(3.0)
