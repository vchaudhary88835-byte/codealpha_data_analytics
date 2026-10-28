"""CodeAlpha Task 3: Create charts from sample retail sales data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = Path("data/sales_data.csv")
OUTPUT_DIR = Path("output")

def save_chart(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path.resolve()}")

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH.resolve()}")
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    category = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    plt.figure(figsize=(9, 5))
    category.plot(kind="bar")
    plt.title("Total Revenue by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=25, ha="right")
    save_chart(OUTPUT_DIR / "revenue_by_category.png")

    region = df.groupby("region")["profit"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    region.plot(kind="bar")
    plt.title("Total Profit by Region")
    plt.xlabel("Region")
    plt.ylabel("Profit")
    plt.xticks(rotation=0)
    save_chart(OUTPUT_DIR / "profit_by_region.png")

    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["revenue"].sum().sort_index()
    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=35, ha="right")
    save_chart(OUTPUT_DIR / "monthly_revenue_trend.png")

    plt.figure(figsize=(8, 5))
    plt.scatter(df["revenue"], df["profit"], alpha=0.7)
    plt.title("Revenue vs Profit by Order")
    plt.xlabel("Revenue")
    plt.ylabel("Profit")
    save_chart(OUTPUT_DIR / "revenue_vs_profit_scatter.png")

    print("\\nAll charts generated. Open PNG files in the output folder.")

if __name__ == "__main__":
    main()
