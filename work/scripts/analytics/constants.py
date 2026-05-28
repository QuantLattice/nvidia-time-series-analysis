"""
Default analytical configuration constants.

This module centralizes shared default parameters, thresholds,
and type definitions used throughout the analytics pipeline.

The constants defined here provide a unified configuration layer for:
- feature engineering;
- exploratory data analysis (EDA);
- statistical analysis;
- technical indicators;
- categorical feature generation;
- time-series diagnostics.

Covered analytical domains
--------------------------

Return features
    Rolling return window definitions used in return-based analysis.

Moving averages
    Default windows for SMA, EMA, and VWMA indicators.

Technical indicators
    Hyperparameters for RSI, MACD, Bollinger Bands,
    volatility, and momentum calculations.

Categorical features
    Thresholds and quantile boundaries used for
    categorical regime classification.

EDA utilities
    Shared defaults for descriptive statistics,
    histogram generation, outlier detection,
    and correlation analysis.

Stationarity testing
    Configuration defaults for Augmented Dickey-Fuller (ADF)
    stationarity diagnostics.

Autocorrelation analysis
    Shared defaults for autocorrelation (ACF) and
    partial autocorrelation (PACF) analysis.

Design goals
------------
Centralized configuration provides:

- consistency across analytical modules;
- reproducible statistical behavior;
- simplified experimentation and tuning;
- separation of configuration from implementation logic;
- easier long-term maintenance and extensibility.
"""


from typing import Literal, TypeAlias


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


# ==========================================
# STATISCTICS
# ==========================================

# Default label used when a categorical value is unavailable.
DEFAULT_UNKNOWN_CATEGORY_NAME = "unknown"


# ==========================================
# EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================

# Default trimming ratio used for robust statistics.
DEFAULT_TRIM_RATIO = 0.05

# Default number of histogram bins for distribution summaries.
DEFAULT_HISTOGRAM_BINS = 10

# Default Tukey IQR multiplier for outlier detection.
DEFAULT_OUTLIER_IQR_MULTIPLIER = 1.5

# Default correlation method used in pairwise analysis.
DEFAULT_CORRELATION_METHOD = "pearson"

# Default threshold for strong correlations.
DEFAULT_STRONG_CORRELATION_THRESHOLD = 0.7

# Default number of top correlations to return.
DEFAULT_TOP_CORRELATIONS_COUNT = 5

# Default fallback name for unnamed pandas Series.
DEFAULT_SERIES_NAME = "unnamed_series"

# Default quantile probabilities for descriptive distribution tables.
DEFAULT_QUANTILE_PROBS = [
    0.01,
    0.05,
    0.25,
    0.50,
    0.75,
    0.95,
    0.99,
]


# =============================================================================
# TIME SERIES: STATIONARITY TESTING (ADF)
# =============================================================================

# Significance level for Augmented Dickey-Fuller test.
ADF_DEFAULT_ALPHA = 0.05

# Deterministic term used in ADF regression ("c" = constant).
ADF_DEFAULT_REGRESSION = "c"

# Lag selection method used by ADF test.
ADF_DEFAULT_AUTOLAG = "AIC"

# Maximum lag order (None = automatic selection).
ADF_DEFAULT_MAXLAG = None

# Minimum number of observations required for ADF test validity.
ADF_DEFAULT_MIN_LENGTH = 8


# =============================================================================
# ADF INTERPRETATION MESSAGES
# =============================================================================

ADF_HYPOTHESIS_STATIONARY = "Series is stationary."
ADF_HYPOTHESIS_NON_STATIONARY = "Series is non-stationary."

ADF_RECOMMENDATION_STATIONARY = (
    "The series is suitable for many classical time-series models."
)

ADF_RECOMMENDATION_NON_STATIONARY = (
    "Differencing or detrending may be required before forecasting."
)

# =============================================================================
# TIME SERIES: AUTOCORRELATION ANALYSIS
# =============================================================================

# Default maximum lag used for ACF/PACF analysis.
AUTOCORRELATION_DEFAULT_MAX_LAG = 40

# Default significance level for autocorrelation confidence intervals.
AUTOCORRELATION_DEFAULT_ALPHA = 0.05

# Default FFT flag for ACF computation.
AUTOCORRELATION_DEFAULT_FFT = True

# Default minimum series length required for autocorrelation analysis.
AUTOCORRELATION_DEFAULT_MIN_LENGTH = 8

# Default lag index name used in returned series/dataframes.
AUTOCORRELATION_LAG_INDEX_NAME = "lag"

# Default names for returned summary series.
AUTOCORRELATION_ACF_SERIES_NAME = "acf"
AUTOCORRELATION_PACF_SERIES_NAME = "pacf"

# Default confidence interval column names.
AUTOCORRELATION_CI_LOWER_COLUMN = "lower"
AUTOCORRELATION_CI_UPPER_COLUMN = "upper"

# Supported PACF methods.
PACFMethod: TypeAlias = Literal[
    "yw",
    "ywadjusted",
    "ols",
    "ols-inefficient",
    "ols-adjusted",
    "ywm",
    "ywmle",
    "ld",
    "ldadjusted",
    "ldb",
    "ldbiased",
    "burg",
]

# Default PACF method.
AUTOCORRELATION_DEFAULT_PACF_METHOD: PACFMethod = "ywadjusted"
