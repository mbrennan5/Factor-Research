# Project Structure Documentation

## 📁 Complete Project Organization

```
Quantitative-Factor-Research/
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file - detailed structure
├── REQUIREMENTS.md              # Dependencies and setup
├── .gitignore                   # Git ignore rules
├── .gitattributes              # Line ending configuration
│
├── notebooks/                   # Jupyter notebooks
│   ├── 01_Data_Preparation.ipynb
│   ├── 02_Alpha_Factor_Generation.ipynb
│   ├── 03_Alpha_Factor_Generation_2.ipynb
│   ├── 04_Alpha_Factor_Selection.ipynb
│   └── 05_ML_Model.ipynb
│
├── data/                        # Data directory structure
│   ├── raw/                     # Raw data (not uploaded)
│   │   ├── datamin2/            # Minute-level data source 1
│   │   ├── datamin3/            # Minute-level data source 2
│   │   └── datamin4/            # Additional data source
│   │       └── data_barra/      # Barra factor data
│   │
│   ├── processed/               # Processed data (not uploaded)
│   │   └── wide_data_preparation/
│   │       ├── daily_ret_data.csv
│   │       ├── daily_turnover_data.csv
│   │       ├── vwap_daily_data.csv
│   │       └── ...
│   │
│   └── factors/                 # Generated factors (not uploaded)
│       ├── obtained_features/   # All generated factors
│       │   ├── alpha_001.csv
│       │   ├── alpha_002.csv
│       │   └── ... (50+ factors)
│       │
│       └── selected_factors/    # Final selected factors
│           ├── factor_001.csv
│           ├── factor_002.csv
│           └── ... (85 factors)
│
├── results/                     # Model results (not uploaded)
│   ├── model_performance/
│   ├── factor_analysis/
│   └── backtest_results/
│
└── docs/                        # Additional documentation
    ├── methodology.md
    ├── factor_descriptions.md
    └── model_comparison.md
```

## 🔄 Data Flow Pipeline

### Phase 1: Data Preparation
```
Raw Data → Data Preparation.ipynb → Processed Data
```

**Input**: Minute-level OHLCV data, Barra factors
**Output**: Daily returns, turnover rates, VWAP, etc.

### Phase 2: Factor Generation
```
Processed Data → Alpha_Factor_Generation.ipynb → Alpha Factors
```

**Generated Factors**:
- Classic Alpha101 (10 factors)
- Liquidity factors (4 factors)
- Volatility & Momentum (4 factors)
- Advanced Technical (4 factors)
- Turnover & Correlation (3 factors)

### Phase 3: High-Frequency Factors
```
Raw Data → Alpha_Factor_Generation_2.ipynb → High-Freq Factors
```

**Generated Factors**:
- Time-based factors (20+ factors)
- Technical & Statistical (15+ factors)
- Volume & Amount (10+ factors)
- Advanced Statistical (15+ factors)

### Phase 4: Feature Selection
```
All Factors → Alpha_Factor_Selection.ipynb → Selected Factors
```

**Selection Process**:
1. IC filtering (IC > 0.02)
2. Correlation filtering (Spearman < 0.7)
3. ML-based selection (Lasso/Ridge + LGBM)
4. Final selection (85 factors)

### Phase 5: Model Training
```
Selected Factors → ML_Model.ipynb → Model Results
```

**Models Implemented**:
- Linear Regression (baseline)
- Deep Neural Network (DNN)
- DeepNet (with residual connections)
- AlexNet (CNN for time series)
- LSTM+ResNet (hybrid architecture)
- Transformer (attention-based)

## 📊 Key Metrics & Results

### Feature Selection Results
- **Initial Factors**: 50+ generated factors
- **IC Filtered**: Factors with IC > 0.02
- **Correlation Filtered**: Spearman correlation < 0.7
- **Final Selection**: 85 high-quality factors

### Model Performance
- **Best Model**: LSTM+ResNet
- **Target IC**: 0.06476
- **Improvement**: 72% over baseline Linear Regression
- **Optimization**: Optuna hyperparameter tuning

### Technical Implementation
- **Vectorized Operations**: High-performance pandas/numpy
- **GPU Support**: PyTorch with CUDA
- **Memory Optimization**: Efficient data handling
- **Time Series CV**: Proper cross-validation for financial data

## 🛠 Technical Stack

### Core Libraries
- **Data Processing**: pandas, numpy, scipy
- **Machine Learning**: scikit-learn, PyTorch, LightGBM
- **Optimization**: Optuna
- **Visualization**: matplotlib, seaborn
- **Development**: Jupyter, Git

### Performance Features
- **Vectorized Calculations**: Fast factor generation
- **Memory Management**: Efficient large dataset handling
- **Parallel Processing**: Multi-core support where applicable
- **GPU Acceleration**: CUDA support for deep learning models

## 📈 Research Contributions

### Novel Approaches
1. **Hybrid Factor Generation**: Combining classic and high-frequency factors
2. **Multi-Stage Selection**: IC + correlation + ML-based filtering
3. **Advanced Architectures**: LSTM+ResNet for financial time series
4. **Comprehensive Evaluation**: Multiple metrics and backtesting

### Practical Applications
- **Quantitative Trading**: Factor-based stock selection
- **Risk Management**: Volatility and correlation analysis
- **Portfolio Construction**: Multi-factor model implementation
- **Performance Attribution**: Factor contribution analysis

## 🔬 Methodology Details

### Factor Generation Techniques
- **Time-Series Operators**: ts_max, ts_min, ts_sum, ts_std_dev, ts_rank
- **Cross-Sectional Operators**: rank, correlation, covariance
- **Advanced Indicators**: MACD, VWAP, momentum, volatility
- **High-Frequency Features**: Intraday patterns, microstructure

### Feature Selection Methods
- **Information Coefficient (IC)**: Measures factor predictive power
- **Spearman Correlation**: Identifies redundant factors
- **L1/L2 Regularization**: Lasso/Ridge for feature importance
- **Gradient Boosting**: LightGBM for non-linear relationships

### Model Training Framework
- **Time Series Split**: Forward-looking validation
- **Early Stopping**: Prevents overfitting
- **Learning Rate Scheduling**: Adaptive optimization
- **Gradient Clipping**: Stable training for deep models
