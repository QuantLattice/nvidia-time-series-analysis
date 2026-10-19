# NVIDIA Time Series Analysis

Desktop application for loading, analysing, and visualising NVIDIA stock price data.
Built with Python 3.11, Tkinter GUI, MySQL, and a full analytics pipeline.

---

## Requirements

| Dependency | Version |
|---|---|
| [Anaconda](https://www.anaconda.com/download)
| MySQL Server | 8.0+ |
| Python | 3.11 (managed by conda) |

---

## Installation (Windows)

1. Install [Anaconda](https://www.anaconda.com/download) if not already installed.
2. Install and start **MySQL Server**.
3. Create a database:
   ```sql
   CREATE DATABASE nvidia_timeseries;
   ```
4. Double-click **`install.bat`**.
   It will automatically:
   - find Anaconda on your machine
   - create a conda environment `nvidia-tsa` with Python 3.11
   - install all required packages from `requirements.txt`
   - copy `.env.example` → `.env`
5. Open **`.env`** and fill in your MySQL credentials:
   ```
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_DB=nvidia_timeseries
   ```
6. Double-click **`run.bat`** to start the application.

---

## Installation (macOS / Linux)

```bash
# Create and activate the conda environment
conda create -n nvidia-tsa python=3.11 -y
conda activate nvidia-tsa

# Install packages
pip install -r requirements.txt

# Copy and fill in credentials
cp .env.example .env
nano .env

# Run
python -m work.scripts.main
```

---

## Running

**Windows:**
```
run.bat
```

**macOS / Linux:**
```bash
conda activate nvidia-tsa
python -m work.scripts.main
```

---

## Features

### Data
- Import stock price data from CSV
- Export data to CSV
- Browse data with pagination

### Analysis
- Interactive charts: Candlestick, Line, Scatter, Box, Histogram
- Filter by date range

### Feature Generation
- **Moving Averages** — SMA, EMA, VWMA
- **Returns** — daily, log, cumulative, rolling
- **Technical Indicators** — RSI, MACD, Bollinger Bands, Volatility, Momentum
- Select any combination of generated columns and plot as line chart

### Reports
- Export data to CSV
- Export analytics report to TXT

---

## Project Structure

```
nvidia-time-series-analysis/
├── work/
│   ├── config/          # App configuration (JSON)
│   ├── data/            # Input datasets
│   ├── graphics/        # Icons and images
│   ├── library/         # Reusable utilities (plotting, config, IO)
│   ├── output/          # Exported reports
│   ├── resources/i18n/  # Localization (en, ru, pt, ky)
│   └── scripts/
│       ├── analytics/   # Indicators and feature generators
│       ├── controllers/ # GUI ↔ service layer
│       ├── db/          # SQLAlchemy models and migrations
│       ├── gui/         # Tkinter interface
│       ├── repositories/# Data access layer
│       ├── services/    # Business logic
│       └── main.py      # Entry point
├── install.bat          # Windows installer
├── run.bat              # Windows launcher
├── environment.yml      # Conda environment definition
├── requirements.txt     # Python packages
└── .env.example         # Database credentials template
```

---

## Running Tests

```bash
conda activate nvidia-tsa

pytest                   # all tests
pytest -m unit           # unit tests only
pytest -m integration    # integration tests only
```

---

## Architecture

```
GUI → Controllers → Services → Repositories → Database
                       ↓
                   Analytics
                       ↓
                    Library
```
