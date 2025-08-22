# Quantitative Factor Research Project

A comprehensive quantitative finance research project implementing **factor modeling**, **feature selection**, and **machine learning** for stock return prediction. This project demonstrates advanced techniques in alpha factor generation, systematic feature selection, and deep learning model comparison.

## 🎯 Project Overview

This project implements a complete quantitative research pipeline covering the entire workflow from raw market data to production-ready predictive models. The research achieved **significant performance improvements** with the best model (LSTM+ResNet) reaching an **Information Coefficient of 0.06476**, representing a **72% improvement** over traditional linear regression benchmarks.

## 📊 Key Achievements

- **🏗️ Factor Library**: Generated comprehensive alpha factor library using vectorized operations and technical operators
- **🔍 Feature Selection**: Systematically reduced features from 100+ candidates to 85 high-quality factors using statistical and ML methods
- **🤖 Model Performance**: Achieved IC of 0.06476 with LSTM+ResNet architecture, significantly outperforming baseline models
- **⚡ Optimization**: Implemented automated hyperparameter tuning using Optuna for all model architectures

## 🏗️ Project Structure

```
quantitative-factor-research/
├── notebooks/                          # Jupyter notebooks for analysis
│   ├── Data_Preparation.ipynb         # Data loading and preprocessing
│   ├── Alpha_Factor_Generation.ipynb   # Base alpha factor creation
│   ├── Alpha_Factor_Generation_2.ipynb # High-frequency technical factors
│   ├── Alpha_Factor_Selection.ipynb    # Feature selection pipeline
│   ├── ML_Model.ipynb                  # Machine learning models
│   └── factor_backtest.ipynb          # Factor backtesting framework
├── data/                               # Data storage
│   ├── raw/                           # Raw market data
│   ├── processed/                     # Processed datasets
│   ├── factors/                       # Generated factors
│   │   ├── obtained_features/         # Raw factor library
│   │   └── selected_factors/          # Final selected factors
│   └── backtest_results/              # Backtesting outputs
└── README.md                          # Project documentation
```

## 🔬 Research Methodology

### 1. Factor Modeling

**Objective**: Develop a comprehensive factor library capturing various market dynamics and price-volume relationships.

**Implementation**:
- **Technical Operators**: Implemented time-series operators (ts_max, ts_min, ts_sum, ts_std_dev, ts_delta, delay, rank)
- **Vectorized Operations**: Utilized pandas and numpy for efficient large-scale factor computation
- **Wide-table Dataset**: Generated standardized factor matrices aligned across time and assets
- **Base Alpha Enhancement**: Applied quantile-based segmentation to improve factor discriminative power
- **Dynamic Factors**: Incorporated rolling standard deviation and price-volume correlation factors

**Key Features Generated**:
- **Classic Alpha101 Factors**: Traditional quantitative factors
- **Technical Indicators**: RSI, MACD, Bollinger Bands variations
- **Volume Microstructure**: Intraday volume patterns and clustering
- **Price-Volume Relationships**: Correlation-based and interaction factors
- **Statistical Moments**: Skewness, kurtosis, and higher-order moments

### 2. Feature Selection

**Objective**: Systematically reduce the feature space while maintaining predictive power and ensuring factor independence.

**Multi-Stage Selection Process**:

1. **Statistical Screening**:
   - **Information Coefficient (IC)**: Filtered factors with |IC| > 0.02
   - **IC Consistency**: Maintained factors with stable predictive relationships

2. **Correlation Analysis**:
   - **Spearman Correlation**: Eliminated highly correlated factors (threshold < 0.7)
   - **Greedy Selection**: Iterative removal to maintain factor diversity

3. **Machine Learning Selection**:
   - **Lasso Regression**: L1 regularization for sparse feature selection
   - **Ridge Regression**: L2 regularization for feature importance ranking
   - **LightGBM**: Gradient boosting feature importance analysis

**Final Results**:
- **85 Selected Factors**: Optimized feature set balancing predictive power and independence
- **Spearman Correlation < 0.7**: Ensured factor diversification
- **High IC Factors**: Maintained strong predictive relationships with future returns

### 3. Machine Learning Models

**Objective**: Compare multiple architectures to identify the optimal model for stock return prediction.

**Model Architectures Implemented**:

1. **Linear Regression** (Baseline)
   - Traditional OLS regression for benchmark comparison
   - Provides interpretable baseline performance metrics

2. **Deep Neural Network (DNN)**
   - Multi-layer feedforward architecture
   - Batch normalization and dropout for regularization
   - Hidden layers: [128, 64, 32] with ReLU activation

3. **DeepNet**
   - Enhanced deep architecture with residual connections
   - Multiple hidden layers: [256, 128, 64, 32]
   - Skip connections to address vanishing gradient problem

4. **AlexNet**
   - Convolutional neural network adapted for financial time series
   - 1D convolutions to capture sequential patterns
   - Max pooling and adaptive pooling for feature extraction

5. **LSTM+ResNet** ⭐ **Best Performing**
   - Hybrid architecture combining LSTM and residual networks
   - Bidirectional LSTM for temporal pattern recognition
   - ResNet blocks for feature refinement
   - **Achieved IC: 0.06476**

6. **Transformer**
   - Self-attention mechanism for sequence modeling
   - Multi-head attention with positional encoding
   - Encoder-only architecture optimized for regression

**Training Framework**:
- **Time Series Cross-Validation**: Proper temporal splitting to avoid look-ahead bias
- **Early Stopping**: Prevents overfitting with validation-based stopping criteria
- **Hyperparameter Optimization**: Optuna-based automated tuning for all models
- **Information Coefficient**: Primary evaluation metric for financial relevance

## 📈 Performance Results

### Model Comparison

| Model | Mean IC | IC Std | Max IC | Hit Rate | Improvement vs Baseline |
|-------|---------|--------|--------|----------|------------------------|
| **LSTM+ResNet** | **0.06476** | 0.0234 | 0.0891 | 68.3% | **+72.0%** |
| Transformer | 0.05823 | 0.0198 | 0.0756 | 64.1% | +54.6% |
| DeepNet | 0.04992 | 0.0187 | 0.0634 | 61.2% | +32.5% |
| DNN | 0.04234 | 0.0156 | 0.0578 | 58.7% | +12.4% |
| AlexNet | 0.03891 | 0.0143 | 0.0523 | 56.9% | +3.3% |
| Linear Regression | 0.03767 | 0.0134 | 0.0489 | 55.4% | Baseline |

### Key Performance Highlights

- **🥇 Best Model**: LSTM+ResNet with IC = 0.06476
- **🚀 Significant Improvement**: 72% better than linear regression baseline
- **📊 Consistent Performance**: High hit rate (68.3%) indicating reliable predictions
- **⚡ Optimization Success**: Hyperparameter tuning improved all models by 15-25%

## 🛠️ Technical Implementation

### Data Processing Pipeline

1. **Data Ingestion**: Multi-source market data loading and validation
2. **Feature Engineering**: Vectorized factor computation using pandas/numpy
3. **Cross-sectional Standardization**: Z-score normalization across assets
4. **Time Series Alignment**: Consistent temporal indexing across all datasets

### Model Training Pipeline

1. **Data Preprocessing**: Standardization and missing value handling
2. **Time Series Splitting**: Rolling window validation with proper temporal ordering
3. **Model Training**: Batch processing with GPU acceleration
4. **Hyperparameter Optimization**: Optuna TPE sampler with median pruning
5. **Performance Evaluation**: IC calculation and statistical significance testing

### Key Technologies

- **Python**: Core programming language
- **PyTorch**: Deep learning framework
- **Pandas/NumPy**: Data manipulation and numerical computing
- **Optuna**: Hyperparameter optimization
- **Scikit-learn**: Traditional machine learning algorithms
- **LightGBM**: Gradient boosting for feature selection

## 📋 Usage Instructions

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd quantitative-factor-research

# Install dependencies
pip install torch pandas numpy scikit-learn lightgbm optuna matplotlib seaborn tqdm
```

### 2. Data Preparation

```python
# Run data preparation notebook
jupyter notebook notebooks/Data_Preparation.ipynb
```

### 3. Factor Generation

```python
# Generate base alpha factors
jupyter notebook notebooks/Alpha_Factor_Generation.ipynb

# Generate high-frequency factors
jupyter notebook notebooks/Alpha_Factor_Generation_2.ipynb
```

### 4. Feature Selection

```python
# Run comprehensive feature selection pipeline
jupyter notebook notebooks/Alpha_Factor_Selection.ipynb
```

### 5. Model Training

```python
# Train and compare all models
jupyter notebook notebooks/ML_Model.ipynb

# Run specific model training
results = train_all_models(splits, optimize_params=True)
summary_stats, best_model = analyze_results(results)
```

### 6. Backtesting

```python
# Evaluate factor performance
jupyter notebook notebooks/factor_backtest.ipynb
```

## 🔍 Research Insights

### Factor Analysis Findings

1. **Volume Microstructure Factors**: Intraday volume patterns show strong predictive power
2. **Price-Volume Correlations**: Dynamic correlation factors outperform static alternatives
3. **Rolling Statistics**: Time-varying standard deviation captures market regime changes
4. **Quantile Segmentation**: Enhances factor discriminative power across different market conditions

### Model Architecture Insights

1. **LSTM Effectiveness**: Temporal patterns in financial data benefit from LSTM memory mechanisms
2. **Residual Connections**: Skip connections crucial for training deep financial models
3. **Attention Mechanisms**: Transformer self-attention captures complex factor interactions
4. **Hyperparameter Sensitivity**: Proper optimization critical for model performance

### Performance Drivers

1. **Feature Quality**: High-IC factors with low correlation drive performance
2. **Temporal Modeling**: Sequence models outperform feedforward architectures
3. **Regularization**: Proper regularization prevents overfitting in noisy financial data
4. **Cross-Validation**: Time series splitting essential for realistic performance estimates

## 📚 References and Methodology

This project implements methodologies from:

- **Quantitative Finance Literature**: Alpha factor construction and IC analysis
- **Machine Learning Research**: Advanced neural architectures for time series
- **Feature Selection Theory**: Statistical and ML-based feature selection techniques
- **Hyperparameter Optimization**: Bayesian optimization for model tuning

---

**Project Timeline**: March 2025 - June 2025  
**Research Focus**: Quantitative Factor Modeling and Machine Learning for Alpha Generation  
**Key Achievement**: 72% improvement in stock return prediction accuracy using advanced ML architectures