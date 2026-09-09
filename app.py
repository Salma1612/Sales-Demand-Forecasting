"""
app.py
------
Interactive Streamlit dashboard for the Sales Demand Forecasting project.
Lets you adjust the test window and forecast horizon, retrains the
Holt-Winters model live, and shows accuracy metrics + forecast charts.

Deploy on Streamlit Community Cloud (share.streamlit.io) with this file
as the "main file path".
"""

import os

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(
    page_title="Sales Demand Forecasting",
    page_icon="📈",
    layout="wide",
)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_data():
    demand_path = os.path.join(DATA_DIR, "demand.csv")
    if not os.path.exists(demand_path):
        import generate_demand_data  # noqa: F401  (generates demand.csv as a side effect)
    df = pd.read_csv(demand_path, parse_dates=["date"])
    df = df.set_index("date").asfreq("D")
    return df["units_sold"]


series = load_data()

st.title("📈 Sales Demand Forecasting")
st.caption(
    "Time-series demand forecasting using Holt-Winters exponential smoothing on a "
    "synthetically generated 2-year daily demand dataset. Built with Python and Statsmodels."
)

# ---------------- Sidebar controls ----------------
st.sidebar.header("Model Settings")
test_days = st.sidebar.slider("Held-out test period (days)", min_value=14, max_value=120, value=60, step=7)
forecast_days = st.sidebar.slider("Forecast horizon (days)", min_value=7, max_value=90, value=30, step=7)
seasonal_periods = st.sidebar.selectbox("Seasonality period (days)", options=[7, 14, 30], index=0,
                                          help="7 = weekly seasonality (default)")

st.sidebar.divider()
st.sidebar.metric("Total historical days", f"{len(series):,}")
st.sidebar.metric("Mean daily demand", f"{series.mean():.1f} units")

# ---------------- Train/test split + model ----------------
train = series.iloc[:-test_days]
test = series.iloc[-test_days:]

with st.spinner("Training Holt-Winters model..."):
    model = ExponentialSmoothing(
        train, trend="add", seasonal="add",
        seasonal_periods=seasonal_periods, initialization_method="estimated",
    )
    fit = model.fit(optimized=True)
    test_pred = fit.forecast(test_days)

    mae = mean_absolute_error(test, test_pred)
    rmse = np.sqrt(mean_squared_error(test, test_pred))
    mape = np.mean(np.abs((test.values - test_pred.values) / test.values)) * 100

# ---------------- KPI row ----------------
k1, k2, k3 = st.columns(3)
k1.metric("MAE", f"{mae:.2f} units")
k2.metric("RMSE", f"{rmse:.2f} units")
k3.metric("MAPE", f"{mape:.2f}%")

st.divider()

# ---------------- Test period chart ----------------
st.subheader(f"Forecast vs Actual — Held-Out {test_days}-Day Test Period")
fig1, ax1 = plt.subplots(figsize=(10, 4.5))
ax1.plot(train.index[-90:], train.values[-90:], label="Train (last 90 days)", color="steelblue")
ax1.plot(test.index, test.values, label="Actual", color="black")
ax1.plot(test.index, test_pred.values, label="Forecast", color="orange", linestyle="--")
ax1.legend()
ax1.set_xlabel("Date")
ax1.set_ylabel("Units Sold")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig1)

st.divider()

# ---------------- Forward forecast ----------------
st.subheader(f"{forecast_days}-Day Forward Forecast")
with st.spinner("Refitting on full history and forecasting..."):
    full_model = ExponentialSmoothing(
        series, trend="add", seasonal="add",
        seasonal_periods=seasonal_periods, initialization_method="estimated",
    )
    full_fit = full_model.fit(optimized=True)
    future_forecast = full_fit.forecast(forecast_days)

fig2, ax2 = plt.subplots(figsize=(10, 4.5))
ax2.plot(series.index[-180:], series.values[-180:], label="Historical demand", color="steelblue")
ax2.plot(future_forecast.index, future_forecast.values, label="Forecast", color="crimson", linestyle="--")
ax2.legend()
ax2.set_xlabel("Date")
ax2.set_ylabel("Units Sold")
plt.xticks(rotation=45, ha="right")
st.pyplot(fig2)

with st.expander("View forecasted values"):
    forecast_df = future_forecast.round(1).reset_index()
    forecast_df.columns = ["date", "forecasted_units"]
    st.dataframe(forecast_df, use_container_width=True)
    st.download_button(
        "Download forecast as CSV",
        forecast_df.to_csv(index=False),
        file_name="forecast.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Dataset is synthetically generated (seeded, reproducible) for demonstration "
    "purposes — see README.md for details. "
    "Source: github.com/Salma1612/Sales-Demand-Forecasting"
)
