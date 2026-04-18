
# Testing System Documentation

## 1. Overview

The project uses a `pytest`-based testing system to ensure correctness of:

- data normalization
- validation rules
- ETL pipeline integrity
- service layer logic

Testing is designed according to the layered architecture of the project:

```
contracts → validation → services → database
```

Each layer has its own responsibility and is tested independently or in combination depending on test type.

---

## 2. Test Structure

All tests are located in:

```
work/tests/
```

### Directory layout:

```
tests/
├── unit/
│   └── contracts/
│       └── validation/
├── integration/
│   └── contracts/
├── fixtures/
└── helpers/
```

### Purpose of each directory:

#### `unit/`
Tests individual components in isolation.

Examples:
- `StockQuoteNormalizer`
- `StockQuoteValidator`

Focus:
- correctness of logic
- deterministic behavior
- no external dependencies

---

#### `integration/`
Tests full pipeline behavior across multiple layers.

Example flow:

```
raw input → normalization → validation → final dataset
```

Focus:
- real-world data simulation
- cross-module correctness
- contract enforcement

---

#### `fixtures/`
Reusable test data.

Contains:
- sample DataFrames
- synthetic CSV-like datasets
- edge-case inputs

Purpose:
- avoid duplication
- ensure consistent test inputs

---

#### `helpers/`
Shared utilities for testing.

Examples:
- pipeline builders
- dataset generators
- assertion helpers

---

## 3. Test Configuration

Testing is configured via `pytest.ini`:

```ini
[pytest]
pythonpath = .

testpaths = work/tests

markers =
    unit: unit tests
    integration: integration tests
````

### Explanation:

* `pythonpath = .`
  → allows absolute imports from project root

* `testpaths`
  → restricts discovery scope to test directory

* `markers`
  → enables separation of test types

---

## 4. Running Tests

### Run all tests:

```bash
pytest
```

### Run unit tests only:

```bash
pytest -m unit
```

### Run integration tests only:

```bash
pytest -m integration
```

### Run specific module:

```bash
pytest work/tests/unit
pytest work/tests/integration
```

---

## 5. Testing Strategy

### 5.1 Unit Testing

Unit tests validate isolated logic.

Covered components:

* normalization rules
* validation rules
* schema transformations
* column mapping logic

#### Example responsibilities:

* column renaming consistency
* type conversion correctness
* sorting by trade_date
* handling invalid rows

---

### 5.2 Integration Testing

Integration tests validate the full ETL pipeline.

Pipeline:

```
CSV input → normalization → validation → clean dataset
```

Covered scenarios:

* valid real-world datasets
* missing columns
* incorrect data types
* negative values (prices, volume)
* OHLC rule violations
* null handling
* noisy datasets from external sources

---

## 6. Design Principles

The testing system follows these principles:

### 6.1 Isolation

Unit tests must not depend on:

* database
* filesystem
* external APIs

---

### 6.2 Determinism

All tests must produce identical results across runs.

---

### 6.3 Layer Awareness

Each layer is tested according to its responsibility:

| Layer      | Test Type          |
| ---------- | ------------------ |
| contracts  | unit + integration |
| validation | unit               |
| services   | unit + integration |
| database   | integration        |

---

### 6.4 Real-world data simulation

Integration tests simulate:

* messy CSV inputs
* missing fields
* incorrect formats
* edge cases from Kaggle datasets

---

## 7. Key Rules

* Every validator MUST have unit tests
* Every service MUST have at least one integration test
* Every dataset transformation MUST be validated
* Contracts are considered a “source of truth” and must never break tests

---

## 8. Future Improvements

Planned enhancements:

* CI pipeline (GitHub Actions)
* test coverage reporting
* synthetic dataset generator
* performance tests for large CSV imports
