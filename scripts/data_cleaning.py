import pandas as pd

# Load raw e-commerce datasets
customers_raw = pd.read_csv('data/raw_customers.csv')
products_raw = pd.read_csv('data/raw_products.csv')
orders_raw = pd.read_csv('data/raw_orders.csv')

# 1. Clean Customers Table: remove duplicate IDs and fill missing segments
customers_clean = customers_raw.drop_duplicates(subset=['customer_id']).copy()
customers_clean['customer_segment'] = customers_clean['customer_segment'].fillna('Consumer')
customers_clean['signup_date'] = pd.to_datetime(customers_clean['signup_date'])

# 2. Clean Products Table: ensure no duplicate SKUs and validate pricing
products_clean = products_raw.drop_duplicates(subset=['product_id']).copy()
products_clean = products_clean[products_clean['selling_price'] > 0]

# 3. Clean Orders Table: deduplicate orders, standardize dates, and handle missing payment modes
orders_clean = orders_raw.drop_duplicates(subset=['order_id']).copy()
orders_clean['payment_mode'] = orders_clean['payment_mode'].fillna('Unknown')
orders_clean['order_date'] = pd.to_datetime(orders_clean['order_date'])

# Extract Year-Month for monthly trend reporting
orders_clean['order_year_month'] = orders_clean['order_date'].dt.to_period('M').astype(str)

# Export cleaned datasets for SQL analysis and Power BI modeling
customers_clean.to_csv('data/clean_customers.csv', index=False)
products_clean.to_csv('data/clean_products.csv', index=False)
orders_clean.to_csv('data/clean_orders.csv', index=False)

print("Data cleaning completed successfully.")
