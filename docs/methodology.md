# Research Methodology

## 🎯 Research Objective

This project implements a comprehensive quantitative factor research framework for stock return prediction, combining traditional financial factor models with modern machine learning techniques.

## 📊 Data Processing Methodology

### 1. Data Preparation Phase

**Input Data Sources:**
- Minute-level OHLCV (Open, High, Low, Close, Volume) data
- Barra factor data (size factor and others)
- Additional market microstructure data

**Processing Steps:**
1. **Data Loading**: Efficient loading of large CSV files with error handling
2. **Data Cleaning**: Handling missing values, outliers, and data quality issues
3. **Feature Engineering**: Creating base features like daily returns, turnover rates, VWAP
4. **Data Alignment**: Ensuring consistent date ranges and stock universes
5. **Format Standardization**: Converting to wide format (dates × stocks) for analysis

**Key Features Generated:**
- Daily return rates
- Daily turnover rates
- Volume-weighted average price (VWAP)
- Barra size factor integration

### 2. Factor Generation Methodology

#### Classic Alpha101 Factors
Based on WorldQuant's "101 Formulaic Alphas" paper, implementing:
- **Alpha #1**: Rank-based volatility factor
- **Alpha #2**: Volume-return correlation
- **Alpha #3**: Open-volume correlation
- **Alpha #4**: Low price rank
- **Alpha #6-10**: Various momentum and correlation factors

#### Technical Operator Library
Custom implementation of financial time-series operators:
- **Time-Series Operators**: `ts_max`, `ts_min`, `ts_sum`, `ts_std_dev`, `ts_rank`
- **Cross-Sectional Operators**: `rank`, `correlation`, `covariance`
- **Advanced Functions**: Rolling statistics, momentum indicators

#### High-Frequency Factors
Generation of microstructure-based factors:
- **Time-Based Factors**: Intraday patterns, time-of-day effects
- **Technical & Statistical**: Advanced technical indicators
- **Volume & Amount**: Trading activity and liquidity measures
- **Advanced Statistical**: Complex statistical relationships

## 🔍 Feature Selection Methodology

### 1. Information Coefficient (IC) Filtering

**Purpose**: Identify factors with predictive power for future returns

**Methodology**:
```python
IC = correlation(factor_t, return_{t+1})
```

**Selection Criteria**: Factors with IC > 0.02 (statistically significant predictive power)

**Implementation**:
- Rolling IC calculation over 60-day windows
- Cross-sectional correlation analysis
- Statistical significance testing

### 2. Correlation-Based Filtering

**Purpose**: Remove redundant factors to reduce multicollinearity

**Methodology**:
- Calculate Spearman correlation matrix between all factors
- Identify highly correlated factor pairs (correlation > 0.7)
- Implement greedy selection algorithm to retain most informative factors

**Algorithm**:
1. Sort factors by absolute IC value
2. Iteratively add factors with correlation < 0.7 to existing set
3. Continue until no more factors can be added

### 3. Machine Learning-Based Selection

#### Lasso Regression (L1 Regularization)
**Purpose**: Feature selection through sparse regularization

**Implementation**:
```python
from sklearn.linear_model import Lasso
lasso = Lasso(alpha=0.01)
lasso.fit(X_train, y_train)
selected_features = np.where(lasso.coef_ != 0)[0]
```

#### Ridge Regression (L2 Regularization)
**Purpose**: Feature importance through regularization

**Implementation**:
```python
from sklearn.linear_model import Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
feature_importance = np.abs(ridge.coef_)
```

#### LightGBM Feature Importance
**Purpose**: Non-linear feature selection

**Implementation**:
```python
import lightgbm as lgb
model = lgb.LGBMRegressor()
model.fit(X_train, y_train)
importance = model.feature_importances_
```

## 🤖 Machine Learning Methodology

### 1. Model Architecture Design

#### Linear Regression (Baseline)
- **Purpose**: Establish baseline performance
- **Implementation**: Standard linear regression with regularization
- **Evaluation**: MSE, MAE, IC metrics

#### Deep Neural Network (DNN)
- **Architecture**: Multi-layer perceptron with dropout
- **Layers**: Input → Dense → Dropout → Dense → Output
- **Activation**: ReLU for hidden layers, linear for output
- **Regularization**: Dropout (0.2), L2 regularization

#### DeepNet (with Residual Connections)
- **Architecture**: DNN with skip connections
- **Innovation**: Residual blocks for better gradient flow
- **Implementation**: Additive skip connections every 2-3 layers

#### AlexNet (CNN for Time Series)
- **Architecture**: Convolutional neural network adapted for 1D time series
- **Layers**: Conv1D → MaxPool → Conv1D → MaxPool → Dense
- **Purpose**: Capture temporal patterns in factor sequences

#### LSTM+ResNet (Hybrid Architecture)
- **Architecture**: LSTM layers with residual connections
- **Purpose**: Combine sequence modeling with deep learning
- **Implementation**: LSTM → Residual Block → LSTM → Dense

#### Transformer (Attention-Based)
- **Architecture**: Multi-head self-attention mechanism
- **Purpose**: Capture complex temporal dependencies
- **Implementation**: Positional encoding + attention layers + feed-forward

### 2. Training Framework

#### Time Series Cross-Validation
**Methodology**: Forward-looking validation to prevent look-ahead bias

**Implementation**:
```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, val_idx in tscv.split(X):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]
```

#### Early Stopping
**Purpose**: Prevent overfitting

**Implementation**:
```python
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)
```

#### Learning Rate Scheduling
**Purpose**: Adaptive optimization

**Implementation**:
```python
scheduler = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-6
)
```

### 3. Hyperparameter Optimization

#### Optuna Framework
**Purpose**: Automated hyperparameter tuning

**Search Space**:
- Learning rate: [1e-5, 1e-2]
- Hidden layers: [1, 5]
- Neurons per layer: [32, 512]
- Dropout rate: [0.1, 0.5]
- Batch size: [32, 256]

**Optimization Strategy**:
- TPE (Tree-structured Parzen Estimator) sampler
- Median pruner for early stopping
- 100 trials per model architecture

## 📈 Evaluation Methodology

### 1. Performance Metrics

#### Information Coefficient (IC)
**Formula**: `IC = correlation(predicted_returns, actual_returns)`
**Purpose**: Measure predictive accuracy

#### Mean Squared Error (MSE)
**Formula**: `MSE = mean((predicted - actual)²)`
**Purpose**: Overall prediction accuracy

#### Mean Absolute Error (MAE)
**Formula**: `MAE = mean(|predicted - actual|)`
**Purpose**: Robust error measurement

### 2. Financial Performance Metrics

#### Sharpe Ratio
**Formula**: `Sharpe = (Return - Risk_Free_Rate) / Volatility`
**Purpose**: Risk-adjusted returns

#### Maximum Drawdown
**Formula**: `MaxDD = min((Peak - Current) / Peak)`
**Purpose**: Risk measurement

#### Calmar Ratio
**Formula**: `Calmar = Annual_Return / Max_Drawdown`
**Purpose**: Risk-adjusted performance

### 3. Statistical Validation

#### Cross-Validation
- Time series split to prevent look-ahead bias
- Multiple folds for robust evaluation
- Out-of-sample testing

#### Statistical Significance
- T-tests for performance differences
- Confidence intervals for metrics
- Bootstrap resampling for robust estimates

## 🔬 Research Contributions

### 1. Novel Methodological Approaches

#### Hybrid Factor Generation
- Combination of classic Alpha101 and high-frequency factors
- Multi-timeframe analysis (minute, daily, weekly)
- Cross-asset correlation analysis

#### Multi-Stage Feature Selection
- Sequential filtering: IC → Correlation → ML-based
- Ensemble feature importance from multiple models
- Stability analysis across different time periods

#### Advanced Model Architectures
- LSTM+ResNet for financial time series
- Attention mechanisms for factor relationships
- Multi-task learning for different prediction horizons

### 2. Practical Innovations

#### Scalable Implementation
- Vectorized operations for high performance
- Memory-efficient data handling
- GPU acceleration for deep learning models

#### Robust Evaluation Framework
- Comprehensive backtesting methodology
- Multiple performance metrics
- Statistical significance testing

#### Production-Ready Code
- Modular design for easy extension
- Comprehensive error handling
- Detailed documentation and examples

## 📚 Theoretical Foundation

### 1. Factor Models
- **Fama-French Three-Factor Model**: Market, Size, Value
- **Carhart Four-Factor Model**: Adding Momentum
- **Modern Factor Models**: Quality, Low Volatility, etc.

### 2. Machine Learning in Finance
- **Deep Learning**: Neural networks for pattern recognition
- **Ensemble Methods**: Combining multiple models
- **Time Series Analysis**: Proper handling of temporal data

### 3. Quantitative Trading
- **Alpha Generation**: Creating predictive signals
- **Risk Management**: Controlling portfolio risk
- **Performance Attribution**: Understanding factor contributions

This methodology provides a comprehensive framework for quantitative factor research, combining traditional financial theory with modern machine learning techniques to achieve superior stock return prediction performance.
