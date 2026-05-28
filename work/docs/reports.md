# Reports Module

## Purpose

The reports module provides a unified reporting layer for the application.  
It converts raw DataFrames and time-series data into structured outputs — tabular DataFrames and plain-text summaries.

All classes in this module are pure and stateless. They do not contain GUI logic, do not access the database, and do not produce side effects.

## Architectural Role

The reports module sits between the analytics and forecasting subsystems and the presentation layer:

Analytics / Forecasting → Reports → GUI / Export

Its responsibility is to transform structured analytical results into formats ready for display or export.

## Module Location

```
work/scripts/reports/
```

## Reports Overview

The module contains two categories of reports: data reports and ML reports.

---

## Data Reports

### `TextReport`

Generates a human-readable multi-section summary of a stock dataset.

Output sections:
- dataset shape;
- date range;
- unique data sources;
- column overview with dtype and non-null count;
- missing value summary;
- numeric descriptives — mean, std, min, median, max.

The result is a plain string suitable for display in a text widget or terminal output.

---

### `StatisticalReport`

Computes a comprehensive set of statistical metrics for every numeric column in the dataset.

Each row in the output table represents one column. Each column in the output table represents one metric.

Computed metrics:
- `count` — non-null observation count;
- `missing` — number of missing values;
- `missing_pct` — missing ratio as a percentage;
- `mean` — arithmetic mean;
- `median` — 50th percentile;
- `std` — sample standard deviation;
- `variance` — sample variance;
- `mad` — median absolute deviation;
- `min` — minimum value;
- `max` — maximum value;
- `range` — max minus min;
- `q25` — 25th percentile;
- `q75` — 75th percentile;
- `iqr` — interquartile range;
- `skewness` — Fisher skewness;
- `kurtosis` — Fisher excess kurtosis;
- `cv` — coefficient of variation.

The result is a pandas DataFrame.

---

### `PivotReport`

Groups the dataset by a configurable column and computes aggregate statistics for selected numeric columns.

Default configuration:
- group column: `source`;
- value columns: `open_price`, `high_price`, `low_price`, `close_price`, `volume`;
- aggregation functions: `mean`, `std`, `min`, `max`, `count`.

The result is a pandas DataFrame with multi-level column headers.  
Custom configuration is provided through `PivotReportConfig`.

---

## ML Reports

ML reports wrap the existing forecasting subsystem located in `work/scripts/forecasting/reports/`.  
They do not duplicate forecasting logic. Their responsibility is to expose forecasting results as tabular DataFrames and plain-text summaries consistent with the rest of this module.

### `ForecastSummary`

Fits a forecasting model on a historical series and generates future predictions.

Inputs:
- `series` — historical time series;
- `config` — model configuration;
- `horizon` — number of future steps to predict.

Outputs:
- `predictions_table` — DataFrame indexed by the future time index with a single `predicted` column;
- `text_summary` — plain-text summary including model name, history size, horizon, predicted values, and basic statistics;
- `source` — raw `ForecastReportResult` from the forecasting subsystem.

---

### `BacktestSummary`

Performs a chronological train/test evaluation of a forecasting model.

Inputs:
- `series` — historical time series;
- `config` — model configuration;
- `test_ratio` — fraction of the series reserved for testing.

Outputs:
- `metrics_table` — DataFrame with columns `mae`, `mse`, `rmse`, `mape`, `train_n`, `test_n` indexed by model name;
- `comparison_table` — DataFrame with `actual` and `predicted` columns aligned on the test index;
- `text_summary` — plain-text summary including model name, split sizes, error metrics, and the first 10 comparison rows;
- `source` — raw `BacktestReportResult` from the forecasting subsystem.

---

## Supported Model Configurations

All ML reports accept any of the following model configurations defined in `work/scripts/forecasting/contracts/model_configs.py`:

- `NaiveConfig` — last observed value as forecast for all future steps;
- `MovingAverageConfig` — rolling window average over the last N observations;
- `ARIMAConfig` — classical ARIMA model parameterized by order (p, d, q);
- `SARIMAXConfig` — seasonal ARIMA model parameterized by non-seasonal and seasonal orders.

## Extension Rules

When adding a new report to this module, follow these rules:

1. Place the new report file in `work/scripts/reports/`.
2. Define a frozen dataclass for the result object.
3. Define a class with a `generate()` method that accepts typed inputs and returns the result dataclass.
4. Export the class and result type from `work/scripts/reports/__init__.py`.
5. Do not import GUI or database modules inside report classes.
6. Do not modify state or produce side effects inside `generate()`.
