# Power BI Dashboard Build Guide

## Load data
1. Run `notebooks/01_data_cleaning.py`.
2. Power BI Desktop → **Get data → Text/CSV**.
3. Select `data/processed/sales_cleaned.csv`.
4. Rename the table to `sales_cleaned`.
5. Set `order_date` and `ship_date` to Date; sales/profit/discount to Decimal Number; quantity to Whole Number.

## Page 1 — Retail Sales & Profitability Overview

**Slicers:** Order Date, Region, Category, Segment.

**KPI cards (top row):**
- Total Sales
- Total Profit
- Profit Margin %
- Total Orders
- Unique Customers

**Charts:**
1. Line chart: Axis = Order Date (month); Values = Total Sales and Total Profit.
2. Clustered column: Axis = Category; Values = Total Sales and Total Profit.
3. Horizontal bar: Axis = Sub-Category; Values = Total Profit; sort ascending to surface loss-making areas.
4. Donut: Legend = Segment; Values = Total Sales.
5. Bar: Axis = Region; Values = Total Profit.
6. Scatter: X = Average Discount; Y = Total Profit; Details = Sub-Category.

Optional map: State as Location, Total Sales as Size, Total Profit in Tooltips. Use only if geographic fields resolve correctly.

## Page 2 — Product & Customer Analysis (optional)
- Top 10 products by sales
- Bottom 10 products by profit
- Top customers by sales
- Sales and profit by segment
- Category/sub-category drill-down

## Design
Use a consistent restrained palette, clear titles, aligned visuals, readable labels, and useful tooltips. Avoid 3D charts and visual clutter.

## Validation
Compare Power BI KPI cards to the SQL KPI query. Check slicers and cross-filtering. Verify profit margin uses `SUM(profit) / SUM(sales)`. Save as `powerbi/Sales_Analytics_Dashboard.pbix`.
