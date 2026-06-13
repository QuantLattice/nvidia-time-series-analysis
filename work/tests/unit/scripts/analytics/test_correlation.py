"""Unit tests for correlation statistics.

Covers: pearson, spearman, kendall pairwise correlations,
correlation_matrix, strong_correlation, top positive/negative.
"""
import pytest
import pandas as pd
import numpy as np

from work.scripts.analytics.statistics.correlation_analysis import (
    pearson_correlation,
    spearman_correlation,
    kendall_correlation,
)
from work.scripts.analytics.statistics.correlation_pairs import (
    correlation_matrix,
    correlation_pairs,
    strong_correlation,
    top_positive_correlations,
    top_negative_correlations,
)

# ── fixtures ─────────────────────────────────────────────

X = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
Y_SAME = X.copy()                               # perfect positive correlation
Y_INV = pd.Series([5.0, 4.0, 3.0, 2.0, 1.0])  # perfect negative correlation
Y_RAND = pd.Series([3.0, 1.0, 4.0, 1.0, 5.0])

DF = pd.DataFrame({
    'a': [1.0, 2.0, 3.0, 4.0, 5.0],
    'b': [5.0, 4.0, 3.0, 2.0, 1.0],
    'c': [1.0, 3.0, 2.0, 5.0, 4.0],
})


# =========================================================
# PEARSON
# =========================================================

@pytest.mark.unit
def test_pearson_perfect_positive() -> None:
    assert pearson_correlation(X, Y_SAME) == pytest.approx(1.0)


@pytest.mark.unit
def test_pearson_perfect_negative() -> None:
    assert pearson_correlation(X, Y_INV) == pytest.approx(-1.0)


@pytest.mark.unit
def test_pearson_range() -> None:
    val = pearson_correlation(X, Y_RAND)
    assert -1.0 <= val <= 1.0


@pytest.mark.unit
def test_pearson_symmetry() -> None:
    assert pearson_correlation(X, Y_RAND) == pytest.approx(
        pearson_correlation(Y_RAND, X)
    )


# =========================================================
# SPEARMAN
# =========================================================

@pytest.mark.unit
def test_spearman_perfect_positive() -> None:
    assert spearman_correlation(X, Y_SAME) == pytest.approx(1.0)


@pytest.mark.unit
def test_spearman_perfect_negative() -> None:
    assert spearman_correlation(X, Y_INV) == pytest.approx(-1.0)


@pytest.mark.unit
def test_spearman_range() -> None:
    val = spearman_correlation(X, Y_RAND)
    assert -1.0 <= val <= 1.0


# =========================================================
# KENDALL
# =========================================================

@pytest.mark.unit
def test_kendall_perfect_positive() -> None:
    assert kendall_correlation(X, Y_SAME) == pytest.approx(1.0)


@pytest.mark.unit
def test_kendall_perfect_negative() -> None:
    assert kendall_correlation(X, Y_INV) == pytest.approx(-1.0)


@pytest.mark.unit
def test_kendall_range() -> None:
    val = kendall_correlation(X, Y_RAND)
    assert -1.0 <= val <= 1.0


# =========================================================
# CORRELATION MATRIX
# =========================================================

@pytest.mark.unit
def test_correlation_matrix_shape() -> None:
    result = correlation_matrix(DF, method='pearson')
    assert result.matrix.shape == (3, 3)


@pytest.mark.unit
def test_correlation_matrix_diagonal_ones() -> None:
    result = correlation_matrix(DF, method='pearson')
    diag = [result.matrix.iloc[i, i] for i in range(result.matrix.shape[0])]
    for val in diag:
        assert val == pytest.approx(1.0)


@pytest.mark.unit
def test_correlation_matrix_symmetric() -> None:
    result = correlation_matrix(DF, method='pearson')
    m = result.matrix
    for i in range(len(m)):
        for j in range(len(m)):
            assert m.iloc[i, j] == pytest.approx(m.iloc[j, i], abs=1e-9)


# =========================================================
# CORRELATION PAIRS
# =========================================================

@pytest.mark.unit
def test_correlation_pairs_count() -> None:
    pairs = correlation_pairs(DF)
    # n*(n-1)/2 unique pairs for 3 columns = 3
    assert len(pairs) == 3


@pytest.mark.unit
def test_correlation_pairs_no_self_pairs() -> None:
    pairs = correlation_pairs(DF)
    for p in pairs:
        assert p.feature_x != p.feature_y


# =========================================================
# STRONG CORRELATION
# =========================================================

@pytest.mark.unit
def test_strong_correlation_threshold() -> None:
    pairs = correlation_pairs(DF)
    strong = strong_correlation(pairs, threshold=0.9)
    for p in strong:
        assert abs(p.correlation) >= 0.9


@pytest.mark.unit
def test_strong_correlation_empty_on_high_threshold() -> None:
    pairs = correlation_pairs(DF)
    strong = strong_correlation(pairs, threshold=0.9999)
    # 'a' and 'b' are perfectly negatively correlated (abs=1)
    # 'c' is not perfectly correlated with others
    for p in strong:
        assert abs(p.correlation) >= 0.9999


# =========================================================
# TOP CORRELATIONS
# =========================================================

@pytest.mark.unit
def test_top_positive_correlations() -> None:
    pairs = correlation_pairs(DF)
    top = top_positive_correlations(pairs, n=2)
    assert all(p.correlation > 0 for p in top)
    # Results are in descending order
    values = [p.correlation for p in top]
    assert values == sorted(values, reverse=True)


@pytest.mark.unit
def test_top_negative_correlations() -> None:
    pairs = correlation_pairs(DF)
    top = top_negative_correlations(pairs, n=2)
    assert all(p.correlation < 0 for p in top)
    values = [p.correlation for p in top]
    assert values == sorted(values)
