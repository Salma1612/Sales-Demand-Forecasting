# E-Commerce Sales & Customer Analysis (SQL + Python)

🔗 **Live dashboard:** https://ecommerce-sales-analysis-sql-fvzszzdahsj6vdc3yzoqzh.streamlit.app/

A business analytics project demonstrating SQL-based revenue analysis, customer
segmentation, and trend analysis on e-commerce transaction data.

## Dataset

**Note: This is a synthetically generated dataset** (`generate_data.py`), created
with realistic seasonal patterns (festive-season demand spike in Nov–Dec),
category price ranges, and customer/region distributions, seeded for
reproducibility. It is not scraped or sourced from any real company's data —
built this way so the project is self-contained and reproducible without
external downloads.

- **customers.csv** — 400 customers (customer_id, region, signup_date)
- **orders.csv** — 6,692 orders (order_id, customer_id, order_date, category,
  quantity, unit_price, revenue), spanning Sep 2025 – Aug 2026

## What This Project Demonstrates

- SQL: `JOIN`, `GROUP BY`, aggregation, and window functions (`RANK()`, `LAG()`)
- Business KPIs: monthly revenue trend, month-over-month growth, top customers,
  category revenue share, regional performance
- Python: pulling SQL query results into Pandas and visualizing with Matplotlib

## Live Dashboard

An interactive Streamlit dashboard (`app.py`) is included — with sidebar filters for
date range, region, and category, live KPI cards, and the same SQL-driven charts
as above.

🔗 **Live app:** https://ecommerce-sales-analysis-sql-fvzszzdahsj6vdc3yzoqzh.streamlit.app/

## Key Results (from actual query output — see `analysis.py`)

- **Electronics** is the top revenue category at **66.35%** of total revenue
- **North** region generates the highest total revenue (₹16.47M), while
  **Central** has the highest revenue per active customer (₹180,314.77)
- **Peak month: December 2025** (₹10.33M revenue) — consistent with the
  built-in festive-season demand spike
- **Average month-over-month growth: 3.25%** across the 12-month period
- Top customer (`CUST0298`, East region) generated ₹450,540 across 29 orders

Full query outputs, including the top-10 customer ranking and full
month-by-month growth table, are in `analysis.py`'s printed output.

## Project Structure

```
├── generate_data.py             # Generates the synthetic dataset
├── load_to_sqlite.py            # Loads CSVs into ecommerce.db (SQLite)
├── queries.sql                  # All 5 SQL queries (JOIN, GROUP BY, window functions)
├── analysis.py                  # Runs queries, prints results, generates charts
├── app.py                       # Streamlit interactive dashboard (deployable)
├── customers.csv, orders.csv    # Generated dataset
├── ecommerce.db                 # SQLite database
├── monthly_revenue_trend.png
├── category_revenue_share.png
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python generate_data.py     # generates customers.csv and orders.csv
python load_to_sqlite.py    # loads them into ecommerce.db
python analysis.py          # runs all SQL queries, prints results, saves charts
streamlit run app.py        # launches the interactive dashboard locally
```

## Tech Stack

Python, SQLite (SQL), Pandas, Matplotlib

## Author

Shaik Salma — [LinkedIn](https://www.linkedin.com/in/sksalma1612) | [GitHub](https://github.com/Salma1612)
