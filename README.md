# Sales Demand Forecasting

🔗 **Live dashboard:** https://sales-demand-forecasting-esbgsgxsqec3bhxdveokam.streamlit.app/

A time-series forecasting project predicting daily product demand using
Holt-Winters exponential smoothing — directly demonstrating forecasting and
prediction skills for data-driven business planning.

## Dataset

**Note: This is a synthetically generated dataset** (`generate_demand_data.py`),
built with a realistic upward trend, weekly seasonality (weekend demand boost),
yearly seasonality (festive-season spike in Nov–Dec), and random noise —
seeded for reproducibility. Not scraped or sourced from any real company's data.

- **demand.csv** — 730 days (2 years) of daily unit sales for one product category

## Approach

1. **Model:** Holt-Winters triple exponential smoothing (additive trend,
   additive weekly seasonality, period = 7)
2. **Validation:** Trained on all but the last 60 days; evaluated forecast
   accuracy against that held-out period
3. **Forecast:** Refit on full history, produced a 30-day forward forecast
4. **Metrics:** MAE, RMSE, MAPE

## Live Dashboard

An interactive Streamlit dashboard (`app.py`) is included — adjust the test
window, forecast horizon, and seasonality period live, retrain the model on
the fly, and download the forecast as CSV.

🔗 **Live app:** https://sales-demand-forecasting-esbgsgxsqec3bhxdveokam.streamlit.app/

## Results (from actual model run — see `forecast.py`)

| Metric | Value |
|---|---|
| MAE (held-out test) | 23.20 units |
| RMSE (held-out test) | 27.80 units |
| MAPE (held-out test) | 5.99% |

A MAPE under 6% indicates the model's forecasts are, on average, within ~6%
of actual demand — a strong result for a demand-forecasting use case, and
directly usable for inventory/staffing planning decisions.

See `forecast_vs_actual.png` (test-period accuracy) and `future_forecast.png`
(30-day forward forecast) for visualizations, and `forecast_next_30_days.csv`
for the raw forecasted values.

## Project Structure

```
├── generate_demand_data.py     # Generates the synthetic daily demand dataset
├── forecast.py                  # Trains Holt-Winters model, evaluates, forecasts
├── app.py                       # Streamlit interactive dashboard (deployable)
├── demand.csv                   # Generated dataset
├── forecast_vs_actual.png       # Test-period accuracy chart
├── future_forecast.png          # 30-day forward forecast chart
├── forecast_next_30_days.csv    # Raw forecast values
├── metrics.json                 # MAE / RMSE / MAPE
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python generate_demand_data.py   # generates demand.csv
python forecast.py               # trains model, evaluates, forecasts, saves charts
streamlit run app.py             # launches the interactive dashboard locally
```

## Tech Stack

Python, Statsmodels (Holt-Winters / Exponential Smoothing), Pandas, NumPy,
Scikit-learn (metrics), Matplotlib

## Author

Shaik Salma — [LinkedIn](https://www.linkedin.com/in/sksalma1612) | [GitHub](https://github.com/Salma1612)
