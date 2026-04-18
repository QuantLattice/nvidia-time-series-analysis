# 📁 Project Structure

This project follows a layered architecture to ensure scalability, maintainability, and parallel development.  
The structure is aligned with the technical requirements (TZ) and designed for team collaboration.

---

## Root Directory

### `work/`

All project-related files are contained inside the `work/` directory, as required by the specification.

---

## 📂 Directory Overview

### 🔧 `config/`
Contains application configuration files.

- `app_config.json` — main configuration file
- Stores paths, UI settings, and runtime parameters

---

### 📊 `data/`
Stores input datasets.

- Base dataset (provided with the project)
- Additional CSV files imported by the user

---

### 📄 `docs/`
Project documentation.

- User Guide
- Developer Guide
- Diagrams, screenshots, and additional materials

---

### 📈 `graphics/`
Output directory for generated charts.

- PNG / PDF files
- Created by the reporting module

---

### 🧩 `library/` (Core Utility Layer)

Reusable, generic utilities independent of business logic.

#### Submodules:
- `config/` — configuration loading utilities
- `io/` — file and CSV operations
- `plotting/` — common plotting helpers and export logic
- `utils/` — helper functions (dates, logging, etc.)
- `validation/` — data validation and schema checks

⚠️ This module must NOT contain business-specific logic.

---

### 📝 `logs/`
Application logs.

- Runtime logs
- Error tracking

---

### 📤 `output/`
Generated text reports.

- CSV exports
- Analytical tables

---

### ⚙️ `scripts/` (Application Layer)

Main application logic and business-specific modules.

#### Submodules:

##### `analytics/`
- Financial calculations
- Indicators (SMA, EMA, etc.)
- Time series analysis
- Forecasting models

##### `db/`
- Database models (SQLAlchemy)
- DB session management
- Low-level database operations

##### `repositories/`
- Data access layer
- Abstraction over database queries

##### `services/`
- Business logic
- Combines analytics, DB, and processing
- Used by GUI

##### `reports/`
- Text reports (tables, statistics)
- Graphical reports (charts)

##### `gui/`
- Tkinter-based user interface
- Windows, dialogs, forms

---

### 🚀 Entry Point


### `scripts/main.py`


Main application entry point.

Run the application using:
```bash
python main.py
```

---

### 🛠️ `setup/`

Installation and deployment scripts.

* `install.bat` — environment setup (Conda)
* `create_shortcut.bat` — optional desktop shortcut

---

## 🧠 Architecture Overview

The project follows a layered design:

```
GUI → Services → Repositories → Database
         ↓
     Analytics
         ↓
      Library
```

### Key Principles:

* Separation of concerns
* Reusable utility layer (`library`)
* Clear data flow
* Minimal coupling between modules

### Global system rules:

- `contracts.md` defines data structures (static truth)
- `app_config.json` defines runtime behavior (dynamic settings)
- All modules MUST respect both layers

---

## 👥 Development Guidelines

### Where to write code:

| Task                   | Directory                       |
| ---------------------- | ------------------------------- |
| File handling, helpers | `library/`                      |
| Business logic         | `scripts/services/`             |
| Data analysis          | `scripts/analytics/`            |
| Database logic         | `scripts/db/` + `repositories/` |
| UI (Tkinter)           | `scripts/gui/`                  |
| Reports                | `scripts/reports/`              |

---

### ⚠️ Important Rules

* Do NOT mix GUI and business logic
* Do NOT write business logic inside `library/`
* All data processing should go through `services/`
* Follow PEP 8 and PEP 257
* Keep modules under ~300 lines (as required)

## ⚙️ Configuration System

The project uses a centralized JSON-based configuration system.

### Files:
- `work/config/app_config.json` — active runtime configuration
- `work/config/default_config.json` — fallback default configuration

### Purpose:
The configuration system defines all runtime parameters of the application, including:
- file system paths
- database connection settings
- UI parameters
- report export settings
- analysis parameters

### Key principles:
- Single source of truth for all runtime settings
- No hardcoded paths or parameters in code
- All modules must read settings from config at runtime

## 📐 Data Contracts

The project enforces strict data contracts to ensure consistency across all modules
(GUI, analytics, database, and reporting).

### Main contract file:
- `work/docs/contracts.md`

### Purpose:
Defines canonical formats for:
- stock price data (OHLCV)
- column naming conventions
- CSV import rules
- database schema structure
- DataFrame formats used in processing pipeline

## 🧪 Testing System

The project includes a structured testing system based on `pytest`, designed to ensure correctness of data processing, validation logic, and full ETL pipeline consistency.

### 📁 Test Structure

All tests are located in:

```
work/tests/
```

#### Test categories:

* `unit/` — isolated tests for individual components
* `integration/` — full pipeline and cross-module tests
* `fixtures/` — reusable test datasets and mock inputs
* `helpers/` — shared testing utilities and pipeline builders

---

### 🧪 Test Configuration

Testing is configured via `pytest.ini`:

```ini
[pytest]
pythonpath = .

testpaths = work/tests

markers =
    unit: unit tests
    integration: integration tests
```

### Key settings:

* `pythonpath = .`
  Ensures project root imports work correctly.

* `testpaths = work/tests`
  Restricts discovery to the project test directory.

* Custom markers:

  * `unit` → fast isolated tests
  * `integration` → full system pipeline tests

---

### ▶️ Running Tests

#### Run all tests:

```bash
pytest
```

#### Run only unit tests:

```bash
pytest -m unit
```

#### Run only integration tests:

```bash
pytest -m integration
```

#### Run specific directory:

```bash
pytest work/tests/unit
pytest work/tests/integration
```

---

### 🔬 Testing Strategy

The testing system is designed around a layered validation approach:

#### 1. Unit Tests

Validate isolated components:

* `StockQuoteNormalizer`
* `StockQuoteValidator`
* schema transformations
* column cleanup logic
* type conversion rules

These tests ensure correctness of individual functions without external dependencies.

---

#### 2. Integration Tests

Validate full data pipeline:

```
raw input → normalization → validation → clean dataset
```

Coverage includes:

* valid CSV-like datasets
* schema violations (missing or extra columns)
* type conversion failures
* business rule enforcement (OHLC logic)
* invalid numeric values (negative volume, prices)
* real-world noisy datasets
* null handling scenarios

Integration tests ensure that all system layers work correctly together:

* contracts
* services
* validation
* data processing pipeline
