# Power BI DAX Measures

Import `sales_cleaned.csv` and rename the table to `sales_cleaned`. Create each measure via **Modeling → New measure**.

```dax
Total Sales = SUM(sales_cleaned[sales])

Total Profit = SUM(sales_cleaned[profit])

Total Orders = DISTINCTCOUNT(sales_cleaned[order_id])

Unique Customers = DISTINCTCOUNT(sales_cleaned[customer_id])

Total Quantity = SUM(sales_cleaned[quantity])

Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0)

Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)

Average Discount = AVERAGE(sales_cleaned[discount])

Average Shipping Days = AVERAGE(sales_cleaned[days_to_ship])
```

Format sales, profit, and average order value as currency. Format profit margin and average discount as percentages. The discount source values are decimal fractions (e.g. 0.2 means 20%), so percentage formatting is appropriate.

**Important:** Overall profit margin must be total profit divided by total sales. Do not average row-level `profit_margin_pct`.
