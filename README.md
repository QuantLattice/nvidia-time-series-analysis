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
