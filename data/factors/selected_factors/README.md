# Selected Factors Directory

This directory contains the final selected alpha factors after feature selection and filtering.

## Selection Process

The factors in this directory are the result of a comprehensive feature selection pipeline:

1. **IC Filtering**: Factors with Information Coefficient > 0.02
2. **Correlation Filtering**: Spearman correlation < 0.7 between factors
3. **ML-based Selection**: Lasso/Ridge regression and LightGBM feature importance
4. **Final Selection**: 85 high-quality factors for model training

## Factor Categories

The selected factors include:
- **Classic Alpha101 factors** (10 factors)
- **Liquidity factors** (4 factors)
- **Volatility & Momentum factors** (4 factors)
- **Advanced Technical factors** (4 factors)
- **Turnover & Correlation factors** (3 factors)
- **High-frequency Technical factors** (60+ factors)

## Data Format

All files are in wide format (dates × stocks):
- Rows: Trading dates
- Columns: Stock IDs
- Values: Normalized factor values

## Usage

These selected factors are used as input for:
- `ML_Model.ipynb` - Final model training and prediction
- Performance evaluation and backtesting

## Note

Due to file size limitations, actual factor files are not included in this repository.
The selection process and results are documented in `Alpha_Factor_Selection.ipynb`.
