# NVIDIA Stock Analyzer — Setup System Documentation

## Overview

This directory contains all automation scripts responsible for:
- project installation
- database initialization
- environment configuration
- system reset and cleanup

The setup system is designed to ensure **fully reproducible installation** on any Windows 10 machine with Anaconda + MySQL installed.

All scripts are written in Windows Batch (`.bat`) and follow a modular execution model.

---

# ⚙️ Directory Structure

```
setup/
│   install.bat                  → Full system installation entry point
│   reset.bat                    → Full system reset entry point
│   README_SETUP.MD              → This documentation file
│
├── db/                          → Database management utilities
│   ├── check_mysql.bat          → Validates MySQL connection
│   ├── create_mysql_config.bat  → Generates MySQL config from .env
│   ├── init_db.bat              → Creates application database
│   ├── reset_db.bat             → Drops application database
│
├── install/
│   ├── post_install.bat         → Post-installation verification checks
│
└── reset/
├── clear_files.bat          → Removes generated outputs (logs, charts, reports)
```
---

# 🚀 Installation Flow

## ▶ Entry Point

```
install.bat
```

This script performs a full automated installation of the system.

### Execution Steps:

### 1. MySQL Configuration Setup
```
db/create_mysql_config.bat
```

- Reads environment variables from `.env`
- Generates MySQL client configuration file (`mysql.cnf`)
- Used for secure database access without hardcoded credentials

---

### 2. MySQL Connection Check
```
db/check_mysql.bat
```

- Validates that MySQL server is running
- Tests authentication using generated config
- Ensures database access is available before initialization

---

### 3. Database Initialization
```
db/init_db.bat
```

- Creates the main application database:
```
nvidia_timeseries
```
- Applies UTF-8 encoding (`utf8mb4`)
- Safe to run multiple times (idempotent)

---

### 4. Post-Installation Verification
```
install/post_install.bat
```

- Verifies:
  - MySQL configuration existence
  - Database creation status
  - Project structure integrity

---

# 🔁 Reset Flow

## ▶ Entry Point

```
reset.bat
```

This script performs a full system reset.

### WARNING:
This operation is destructive and removes all application data.

---

### Reset Steps:

### 1. MySQL Configuration Preparation
```
db/create_mysql_config.bat
```

Ensures database access before reset operations.

---

### 2. Database Removal
```
db/reset_db.bat
```

- Drops database:
```
nvidia_timeseries
```
- Fully removes all stored financial data

---

### 3. Workspace Cleanup
```
reset/clear_files.bat
```

Deletes all generated runtime artifacts:

- `/output` (CSV reports)
- `/graphics` (charts, plots)
- `/logs` (runtime logs)

---

# 🧩 Database Utilities

## check_mysql.bat

### Purpose:
Validates MySQL connectivity.

### Behavior:
- Checks existence of `mysql.cnf`
- Executes test query:
```sql
  SELECT 1;
```

* Returns success/failure status

## create_mysql_config.bat

### Purpose:

Securely generates MySQL configuration file.

### Input:

`.env` file in project root:

```
MYSQL_USER=root
MYSQL_PASSWORD=****
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### Output:

```
config/mysql.cnf
```

Used by all database scripts.

---

## init_db.bat

### Purpose:

Creates application database.

### SQL:

```sql
CREATE DATABASE IF NOT EXISTS nvidia_timeseries
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## reset_db.bat

### Purpose:

Drops application database.

### SQL:

```sql
DROP DATABASE IF EXISTS nvidia_timeseries;
```

# ▶ Usage

## Full Installation

```bash
work/setup/install.bat
```

## Full Reset

```bash
work/setup/reset.bat
```

---

# 📌 Notes

* These scripts are intended for **local development and academic deployment**
* They simulate production-grade initialization pipelines
* All scripts are safe to re-run unless explicitly performing reset operations
