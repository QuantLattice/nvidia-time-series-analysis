"""
Categorical summary statistics for exploratory data analysis.

This module provides descriptive metrics for categorical Series,
including frequency distributions, dominant category detection,
entropy, and imbalance measurement.
"""


from dataclasses import dataclass
import pandas as pd
import numpy as np

from work.scripts.analytics.constants import DEFAULT_UNKNOWN_CATEGORY_NAME


@dataclass(frozen=True)
class CategoryDistribution:
    """
    Distribution summary for categorical values.

    Attributes
    ----------
    counts : pd.Series
        Absolute frequency of each category.

    ratios : pd.Series
        Relative frequency of each category.
    """

    counts: pd.Series
    ratios: pd.Series


# =========================================================
# DISTRIBUTION
# =========================================================

def category_distribution(
    series: pd.Series
) -> CategoryDistribution:
    """
    Calculate category frequency distribution.

    Parameters
    ----------
    series : pd.Series
        Input categorical series.

    Returns
    -------
    CategoryDistribution
        Absolute and relative category frequencies.
    """

    clean = series.dropna()

    counts = clean.value_counts()

    ratios = clean.value_counts(normalize=True)

    return CategoryDistribution(
        counts=counts,
        ratios=ratios
    )


# =========================================================
# DOMINANCE
# =========================================================

def dominant_category(
    series: pd.Series
) -> str:
    """
    Return the most frequent category.

    Parameters
    ----------
    series : pd.Series
        Input categorical series.

    Returns
    -------
    str
        Dominant category label, or the default unknown category
        name when the series is empty.
    """

    clean = series.dropna()

    if clean.empty:
        return DEFAULT_UNKNOWN_CATEGORY_NAME

    return str(clean.value_counts().idxmax())


# =========================================================
# ENTROPY
# =========================================================

def category_entropy(
    series: pd.Series
) -> float:
    """
    Calculate Shannon entropy of a categorical series.

    Parameters
    ----------
    series : pd.Series
        Input categorical series.

    Returns
    -------
    float
        Shannon entropy in bits, or NaN if the series is empty.
    """

    clean = series.dropna()

    if clean.empty:
        return np.nan

    probabilities = clean.value_counts(normalize=True).astype(dtype=float)

    entropy_terms = pd.Series(
        data=probabilities * np.log2(probabilities),
    )

    entropy = -entropy_terms.sum()

    return float(entropy)


# =========================================================
# IMBALANCE
# =========================================================

def imbalance_ratio(
    series: pd.Series
) -> float:
    """
    Calculate the category imbalance ratio.

    The imbalance ratio is defined as:

    .. math:: max(p_i) / min(p_i)

    Parameters
    ----------
    series : pd.Series
        Input categorical series.

    Returns
    -------
    float
        Ratio between the most and least frequent categories,
        or NaN if the series is empty.
    """

    clean = series.dropna()

    if clean.empty:
        return np.nan

    ratios = clean.value_counts(normalize=True)

    min_ratio = ratios.min()

    if min_ratio == 0:
        return np.inf

    return ratios.max() / min_ratio
