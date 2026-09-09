"""
generate_demand_data.py
------------------------
Generates a realistic SYNTHETIC daily product-demand time series with
trend, weekly seasonality, yearly (festive-season) seasonality, and noise.
Seeded for reproducibility. Clearly labeled synthetic -- not scraped from
any real company's data (see README).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(7)

START_DATE = datetime(2024, 1, 1)
N_DAYS = 730  # 2 years of daily data

dates = [START_DATE + timedelta(days=i) for i in range(N_DAYS)]

# Base trend: gradual growth over 2 years
trend = np.linspace(200, 340, N_DAYS)

# Weekly seasonality: higher demand on weekends
day_of_week = np.array([d.weekday() for d in dates])  # 0=Mon ... 6=Sun
weekly_effect = np.where(day_of_week >= 5, 35, 0)  # Sat/Sun boost

# Yearly seasonality: festive-season spike (Nov-Dec) + mild summer dip
day_of_year = np.array([d.timetuple().tm_yday for d in dates])
yearly_effect = 60 * np.sin(2 * np.pi * (day_of_year - 300) / 365)  # peak ~ late Nov
yearly_effect = np.clip(yearly_effect, -20, 60)

# Random noise
noise = np.random.normal(0, 15, N_DAYS)

demand = trend + weekly_effect + yearly_effect + noise
demand = np.clip(demand, 20, None).round().astype(int)

df = pd.DataFrame({
    "date": [d.strftime("%Y-%m-%d") for d in dates],
    "category": "Electronics",
    "units_sold": demand,
})

df.to_csv("demand.csv", index=False)
print(f"Generated {len(df)} daily demand records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Mean daily demand: {df['units_sold'].mean():.1f} units")
