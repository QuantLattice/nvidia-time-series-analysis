# Data Contracts

## 1. Raw Data (Quotes)

All stock data MUST follow this structure:

Columns:
- trade_date (YYYY-MM-DD)
- open_price (float)
- high_price (float)
- low_price (float)
- close_price (float)
- adj_close_price (float, optional)
- volume (int)

Rules:
- Dates format: YYYY-MM-DD
- No duplicates (ticker + trade_date)
- Data must be sorted by date
- No negative prices or volume

## 2. Column Mapping (CSV → Internal Format)

All imported CSV files MUST be normalized:

- date → trade_date
- open → open_price
- high → high_price
- low → low_price
- close → close_price
- adj close → adj_close_price
- volume → volume

## 3. Database Table: stock_quotes

Columns:
- id (int, primary key)
- trade_date (date)
- open_price (float)
- high_price (float)
- low_price (float)
- close_price (float)
- adj_close_price (float)
- volume (int)
