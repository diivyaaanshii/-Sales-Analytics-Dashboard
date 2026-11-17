-- Run this in the sales_analytics PostgreSQL database.
-- The schema matches the normalized Sample Superstore fields and derived columns.

CREATE TABLE IF NOT EXISTS sales_cleaned (
    row_id INTEGER,
    order_id VARCHAR(30),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(40),
    customer_id VARCHAR(30),
    customer_name VARCHAR(150),
    segment VARCHAR(40),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INTEGER,
    region VARCHAR(30),
    product_id VARCHAR(40),
    category VARCHAR(60),
    sub_category VARCHAR(60),
    product_name TEXT,
    sales NUMERIC(14,2),
    quantity INTEGER,
    discount NUMERIC(8,4),
    profit NUMERIC(14,2),
    order_year INTEGER,
    order_month INTEGER,
    month_name VARCHAR(20),
    order_quarter VARCHAR(3),
    days_to_ship INTEGER,
    profit_margin_pct NUMERIC(12,4)
);

-- Import data/processed/sales_cleaned.csv using pgAdmin Import/Export:
-- Format: CSV; Header: Yes; Delimiter: comma; Encoding: UTF8.
-- Or from psql, use a local absolute path:
-- \copy sales_cleaned FROM 'C:/path/to/sales_cleaned.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
