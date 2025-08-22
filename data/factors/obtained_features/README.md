# Alpha Factors Directory

This directory contains generated alpha factors from `Alpha_Factor_Generation.ipynb`.

## Factor Categories

### Classic Alpha101 Factors
- `alpha_001.csv` - Alpha #1: Rank-based volatility factor
- `alpha_002.csv` - Alpha #2: Volume-return correlation
- `alpha_003.csv` - Alpha #3: Open-volume correlation
- `alpha_004.csv` - Alpha #4: Low price rank
- `alpha_006.csv` - Alpha #6: Open-volume correlation
- `alpha_007.csv` - Alpha #7: Volume-based momentum
- `alpha_008.csv` - Alpha #8: Open-return interaction
- `alpha_009.csv` - Alpha #9: Conditional price change
- `alpha_010.csv` - Alpha #10: Ranked conditional price change

### Liquidity Factors
- `alpha_liq_01.csv` - Volume momentum
- `alpha_liq_02.csv` - 20-day average volume
- `alpha_liq_03.csv` - Turnover rank
- `alpha_liq_04.csv` - Turnover momentum

### Volatility & Momentum Factors
- `alpha_vol_01.csv` - 20-day return volatility
- `alpha_vol_02.csv` - Max price change over 10 days
- `alpha_mom_01.csv` - 10-day price momentum
- `alpha_mom_02.csv` - 20-day price momentum

### Advanced Technical Factors
- `alpha_tech_01.csv` - Price position in range
- `alpha_tech_02.csv` - Return-volume correlation
- `alpha_tech_03.csv` - Price vs VWAP
- `alpha_tech_04.csv` - MACD signal

### Turnover & Correlation Factors
- `alpha_turn_01.csv` - 5-day mean turnover
- `alpha_corr_01.csv` - Turnover-volume correlation
- `alpha_corr_02.csv` - Close-VWAP correlation

## Data Format

All factor files are in wide format (dates × stocks):
- Rows: Trading dates
- Columns: Stock IDs
- Values: Factor values (typically normalized/ranked)

## Usage

These factors are used in:
1. `Alpha_Factor_Selection.ipynb` - Feature selection and filtering
2. `ML_Model.ipynb` - Model training and prediction

## Sample Data

Due to file size limitations, only sample data is included.
Full factor files are generated when running the notebooks locally.
