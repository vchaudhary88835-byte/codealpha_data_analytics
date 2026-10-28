"""CodeAlpha Task 2: Exploratory Data Analysis."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/sales_data.csv")
OUTPUT_DIR = Path("output")

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH.resolve()}")
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df.columns = [c.strip().lower() for c in df.columns]
    duplicate_orders = int(df["order_id"].duplicated().sum())
    missing_values = df.isna().sum()
    df = df.drop_duplicates(subset=["order_id"]).copy()
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").astype(str)

    category_summary = df.groupby("category", as_index=False).agg(
        orders=("order_id","count"), units_sold=("quantity","sum"),
        revenue=("revenue","sum"), profit=("profit","sum")
    ).sort_values("revenue", ascending=False)
    region_summary = df.groupby("region", as_index=False).agg(
        orders=("order_id","count"), revenue=("revenue","sum"), profit=("profit","sum")
    ).sort_values("revenue", ascending=False)
    monthly_summary = df.groupby("month", as_index=False).agg(
        revenue=("revenue","sum"), profit=("profit","sum")
    ).sort_values("month")

    category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)
    region_summary.to_csv(OUTPUT_DIR / "region_summary.csv", index=False)
    monthly_summary.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)

    best_category = category_summary.iloc[0]
    best_region = region_summary.iloc[0]
    report = f"""EXPLORATORY DATA ANALYSIS REPORT
================================
Dataset: {DATA_PATH}
Rows after removing duplicate order IDs: {len(df)}
Duplicate order IDs detected before cleaning: {duplicate_orders}

Missing values by column:
{missing_values.to_string()}

KEY METRICS
-----------
Total revenue: {df['revenue'].sum():,.2f}
Total profit: {df['profit'].sum():,.2f}
Average revenue per order: {df['revenue'].mean():,.2f}
Total units sold: {int(df['quantity'].sum())}

FINDINGS
--------
Highest-revenue category: {best_category['category']} ({best_category['revenue']:,.2f} revenue)
Highest-revenue region: {best_region['region']} ({best_region['revenue']:,.2f} revenue)
Monthly summary saved to output/monthly_summary.csv.

LIMITATION
----------
The included dataset is synthetic and intended only for learning.
Do not treat these results as actual company sales.
"""
    (OUTPUT_DIR / "summary.txt").write_text(report, encoding="utf-8")
    print(report)
    print(f"Output files saved in: {OUTPUT_DIR.resolve()}")

if __name__ == "__main__":
    main()
