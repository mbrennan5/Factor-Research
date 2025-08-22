# Raw Data Directory

This directory contains the original minute-level stock data and Barra factor data.

## Directory Structure

```
data/raw/
├── datamin2/          # Minute-level data source 1
├── datamin3/          # Minute-level data source 2
├── datamin4/          # Additional data source
│   └── data_barra/    # Barra factor data
└── README.md          # This file
```

## Data Sources

### Minute-Level Stock Data
- **datamin2/**: Contains CSV files with minute-level OHLCV data
- **datamin3/**: Additional minute-level data source
- **datamin4/**: Supplementary data source

### Barra Factor Data
- **datamin4/data_barra/**: Contains Barra factor files (e.g., size factor)

## Data Format

### Minute-Level Data Files
Each CSV file contains:
- `datetime`: Timestamp
- `order_book_id`: Stock identifier
- `open`, `high`, `low`, `close`: Price data
- `volume`: Trading volume
- `money`: Trading amount

### Barra Factor Files
Each CSV file contains:
- `order_book_id`: Stock identifier
- `size`: Barra size factor value
- Additional factor columns as available

## File Naming Convention

- Minute data: `YYYY-MM-DD.csv` (e.g., `2022-07-05.csv`)
- Barra data: `data_barra_YYYY-MM-DD.csv` (e.g., `data_barra_2023-10-31.csv`)

## Usage

These raw data files are processed by:
1. `Data Preparation.ipynb` - Data loading and feature engineering
2. `Alpha_Factor_Generation_2.ipynb` - High-frequency factor generation

## Note

Due to file size limitations, actual data files are not included in this repository.
Place your data files in the corresponding directories to run the notebooks locally.
