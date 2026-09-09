"""
forecast.py
-----------
Trains a Holt-Winters (triple exponential smoothing) forecasting model on
daily product demand, evaluates it on a held-out test period, and produces
a 30-day forward forecast.
"""

import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

TEST_DAYS = 60
FORECAST_DAYS = 30

df = pd.read_csv("demand.csv", parse_dates=["date"])
df = df.set_index("date").asfreq("D")
series = df["units_sold"]

# Train/test split: last TEST_DAYS held out for evaluation
train = series.iloc[:-TEST_DAYS]
test = series.iloc[-TEST_DAYS:]

# Holt-Winters: additive trend, additive weekly seasonality (period=7)
model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=7,
    initialization_method="estimated",
)
fit = model.fit(optimized=True)

# Evaluate on held-out test period
test_pred = fit.forecast(TEST_DAYS)
mae = mean_absolute_error(test, test_pred)
rmse = np.sqrt(mean_squared_error(test, test_pred))
mape = np.mean(np.abs((test.values - test_pred.values) / test.values)) * 100

print("=== Holt-Winters Forecast Evaluation (60-day held-out test) ===")
print(f"MAE:  {mae:.2f} units")
print(f"RMSE: {rmse:.2f} units")
print(f"MAPE: {mape:.2f}%")

# Refit on FULL data, then forecast the next FORECAST_DAYS
full_model = ExponentialSmoothing(
    series, trend="add", seasonal="add", seasonal_periods=7,
    initialization_method="estimated",
)
full_fit = full_model.fit(optimized=True)
future_forecast = full_fit.forecast(FORECAST_DAYS)

print(f"\n=== {FORECAST_DAYS}-Day Forward Forecast ===")
print(future_forecast.round(1).to_string())

# --- Plot: actual vs test predictions ---
plt.figure(figsize=(10, 5))
plt.plot(train.index[-90:], train.values[-90:], label="Train (last 90 days)", color="steelblue")
plt.plot(test.index, test.values, label="Actual (test)", color="black")
plt.plot(test.index, test_pred.values, label="Forecast (test)", color="orange", linestyle="--")
plt.legend()
plt.title("Holt-Winters Forecast vs Actual — Held-Out Test Period")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("forecast_vs_actual.png", dpi=150)
plt.close()

# --- Plot: full history + forward forecast ---
plt.figure(figsize=(10, 5))
plt.plot(series.index[-180:], series.values[-180:], label="Historical demand", color="steelblue")
plt.plot(future_forecast.index, future_forecast.values, label=f"{FORECAST_DAYS}-day forecast",
          color="crimson", linestyle="--")
plt.legend()
plt.title("Demand Forecast — Next 30 Days")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("future_forecast.png", dpi=150)
plt.close()

# Save metrics + forecast
with open("metrics.json", "w") as f:
    json.dump({
        "mae": float(mae),
        "rmse": float(rmse),
        "mape_pct": float(mape),
        "test_days": TEST_DAYS,
        "forecast_days": FORECAST_DAYS,
    }, f, indent=2)

future_forecast.round(1).to_csv("forecast_next_30_days.csv", header=["forecasted_units"])

print("\nSaved: forecast_vs_actual.png, future_forecast.png, metrics.json, forecast_next_30_days.csv")
