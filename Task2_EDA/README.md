# CodeAlpha Task 2 — Exploratory Data Analysis (EDA)

## Objective
Explore a sample retail sales dataset, check data quality, summarize metrics, and identify patterns.

## Dataset
`data/sales_data.csv` is a synthetic learning dataset with 300 orders and 12 columns.

## Run
```bash
python -m pip install -r requirements.txt
python eda_analysis.py
```

## Outputs
- `output/summary.txt` — key metrics and observations
- `output/category_summary.csv` — revenue and profit by category
- `output/region_summary.csv` — revenue and profit by region
- `output/monthly_summary.csv` — monthly revenue/profit

Questions: What is total revenue/profit? Which category and region have the highest revenue? How does revenue change monthly? Are there missing values or duplicate orders?

The dataset is synthetic; do not present the findings as real business results.
