-- 1. Overall KPIs
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM sales_cleaned;

-- 2. Monthly trend
SELECT DATE_TRUNC('month', order_date)::date AS order_month,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM sales_cleaned
GROUP BY 1 ORDER BY 1;

-- 3. Category and sub-category
SELECT category, sub_category,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit,
       ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS margin_pct
FROM sales_cleaned
GROUP BY category, sub_category
ORDER BY sales DESC;

-- 4. Region performance
SELECT region, ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM sales_cleaned
GROUP BY region ORDER BY profit DESC;

-- 5. Top 10 customers
SELECT customer_id, customer_name,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales_cleaned
GROUP BY customer_id, customer_name
ORDER BY sales DESC LIMIT 10;

-- 6. Ten least profitable products
SELECT product_id, product_name,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM sales_cleaned
GROUP BY product_id, product_name
ORDER BY profit ASC LIMIT 10;

-- 7. Discount band analysis
SELECT CASE
         WHEN discount = 0 THEN 'No discount'
         WHEN discount <= 0.10 THEN '1-10%'
         WHEN discount <= 0.20 THEN '11-20%'
         WHEN discount <= 0.30 THEN '21-30%'
         ELSE 'Above 30%'
       END AS discount_band,
       COUNT(*) AS order_lines,
       ROUND(AVG(discount) * 100, 2) AS avg_discount_pct,
       ROUND(SUM(sales), 2) AS sales,
       ROUND(SUM(profit), 2) AS profit
FROM sales_cleaned
GROUP BY 1
ORDER BY MIN(discount);

-- 8. Shipping duration
SELECT ship_mode, ROUND(AVG(days_to_ship), 2) AS avg_days_to_ship,
       COUNT(*) AS order_lines
FROM sales_cleaned
WHERE days_to_ship IS NOT NULL
GROUP BY ship_mode ORDER BY avg_days_to_ship;

-- 9. Year-over-year sales growth
WITH yearly AS (
    SELECT EXTRACT(YEAR FROM order_date)::int AS sales_year, SUM(sales) AS sales
    FROM sales_cleaned GROUP BY 1
)
SELECT sales_year, ROUND(sales, 2) AS sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY sales_year))
             / NULLIF(LAG(sales) OVER (ORDER BY sales_year), 0), 2) AS growth_pct
FROM yearly ORDER BY sales_year;

-- 10. States with negative profit
SELECT state, ROUND(SUM(sales), 2) AS sales, ROUND(SUM(profit), 2) AS profit
FROM sales_cleaned
GROUP BY state HAVING SUM(profit) < 0
ORDER BY profit;
