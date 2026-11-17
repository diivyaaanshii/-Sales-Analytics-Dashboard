"""Generate descriptive summaries and charts from cleaned Superstore data."""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "sales_cleaned.csv"
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY = ROOT / "reports" / "eda_summary.txt"


def save_plot(fig, filename):
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    if not INPUT.exists():
        raise FileNotFoundError("Run 01_data_cleaning.py before EDA.")

    df = pd.read_csv(INPUT, parse_dates=["order_date"], low_memory=False)
    needed = {"sales", "profit", "order_date"}
    if not needed.issubset(df.columns):
        raise ValueError(f"Dataset needs columns: {sorted(needed)}")

    sales = df["sales"].sum()
    profit = df["profit"].sum()
    orders = df["order_id"].nunique() if "order_id" in df else len(df)
    customers = df["customer_id"].nunique() if "customer_id" in df else None
    margin = profit / sales * 100 if sales else 0

    lines = [
        "SALES ANALYTICS — EXPLORATORY DATA ANALYSIS",
        "=" * 48,
        f"Rows: {len(df):,}",
        f"Columns: {len(df.columns):,}",
        f"Total sales: {sales:,.2f}",
        f"Total profit: {profit:,.2f}",
        f"Distinct orders: {orders:,}",
        f"Overall profit margin: {margin:.2f}%",
    ]
    if customers is not None:
        lines.append(f"Unique customers: {customers:,}")

    if "category" in df:
        category = df.groupby("category", dropna=False).agg(
            sales=("sales", "sum"), profit=("profit", "sum")
        ).sort_values("sales", ascending=False)
        lines += ["", "CATEGORY PERFORMANCE", category.to_string()]
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=category.reset_index(), x="category", y="sales", ax=ax)
        ax.set(title="Sales by Category", xlabel="Category", ylabel="Sales")
        save_plot(fig, "sales_by_category.png")

    if "sub_category" in df:
        subcat = df.groupby("sub_category", dropna=False).agg(
            sales=("sales", "sum"), profit=("profit", "sum")
        ).sort_values("profit")
        lines += ["", "SUB-CATEGORY PROFITABILITY", subcat.to_string()]
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(data=subcat.reset_index(), x="profit", y="sub_category", ax=ax)
        ax.set(title="Profit by Sub-Category", xlabel="Profit", ylabel="Sub-Category")
        save_plot(fig, "profit_by_subcategory.png")

    if "region" in df:
        region = df.groupby("region", dropna=False).agg(
            sales=("sales", "sum"), profit=("profit", "sum")
        ).sort_values("profit", ascending=False)
        lines += ["", "REGIONAL PERFORMANCE", region.to_string()]
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=region.reset_index(), x="region", y="profit", ax=ax)
        ax.set(title="Profit by Region", xlabel="Region", ylabel="Profit")
        save_plot(fig, "profit_by_region.png")

    monthly = (
        df.set_index("order_date")
        .resample("MS")
        .agg(sales=("sales", "sum"), profit=("profit", "sum"))
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=monthly, x="order_date", y="sales", marker="o", ax=ax)
    ax.set(title="Monthly Sales Trend", xlabel="Order Month", ylabel="Sales")
    save_plot(fig, "monthly_sales_trend.png")

    if {"discount", "profit"}.issubset(df.columns):
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.scatterplot(data=df, x="discount", y="profit", alpha=0.4, ax=ax)
        ax.set(title="Discount vs Profit", xlabel="Discount", ylabel="Profit")
        save_plot(fig, "discount_vs_profit.png")

    SUMMARY.write_text("\n".join(lines), encoding="utf-8")
    print(f"EDA summary saved to {SUMMARY}")
    print(f"Charts saved to {FIG_DIR}")


if __name__ == "__main__":
    main()
