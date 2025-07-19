# Sales-Prediction-Analytics

# 📈 Sales Prediction System with ARIMA

This repository contains a sales prediction system using ARIMA models to analyze synthetically generated transactional data.

## 🧩 Project Components

### 🔹 Synthetic Data Generation (`generator.py`)
- Simulates **multi-item** and **single-item** transactions with correlations between products.
- Configurable by:
  - Date range
  - Data volume
  - Output format: **CSV** or **Parquet**

### 🔹 Predictive Modeling (`main.py`)
- Predicts future sales by channel: **Online**, **In-Store**, and **Mobile** using **ARIMA** models.
- Computes:
  - Confidence intervals for each prediction
  - Certainty metrics to assess accuracy

### 🔹 Reference Data (`channels.csv`)
- Maps channel IDs to descriptive names to make results easier to interpret.

## 🛠️ Technologies Used

- **Python 3.10+**
- [**Pandas**] – Data manipulation
- [**Statsmodels**] – ARIMA modeling
- [**PyArrow**] – Parquet file support
- [**NumPy**] – Numerical computations

## 🚀 How to Run



