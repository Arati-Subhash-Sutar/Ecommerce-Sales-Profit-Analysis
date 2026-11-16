import pandas as pd
import numpy as np

np.random.seed(42)

# --- 1. GENERATE CUSTOMERS TABLE (5,000 Rows) ---
n_customers = 5000
customers = pd.DataFrame({
    'customer_id': [f'CUST-{10000 + i}' for i in range(n_customers)],
    'customer_segment': np.random.choice(['Consumer', 'Corporate', 'Prime Member'], n_customers, p=[0.50, 0.25, 0.25]),
    'city': np.random.choice(['Mumbai', 'Bengaluru', 'Delhi', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata'], n_customers),
    'region': np.random.choice(['West', 'South', 'North', 'East'], n_customers, p=[0.35, 0.30, 0.20, 0.15]),
    'signup_date': np.random.choice(pd.date_range('2023-01-01', '2025-12-31'), n_customers)
})
# Inject messy data (null segments & duplicate IDs)
customers.loc[np.random.choice(customers.index, 150), 'customer_segment'] = np.nan
customers = pd.concat([customers, customers.sample(40)], ignore_index=True)

# --- 2. GENERATE PRODUCTS TABLE (100 Rows) ---
n_products = 100
categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Beauty & Health', 'Sports & Fitness']
sub_cats = {
    'Electronics': ['Smartphones', 'Audio', 'Laptops', 'Accessories'],
    'Fashion': ['Men Apparel', 'Women Apparel', 'Footwear', 'Watches'],
    'Home & Kitchen': ['Appliances', 'Cookware', 'Furniture', 'Decor'],
    'Beauty & Health': ['Skincare', 'Supplements', 'Haircare', 'Fragrance'],
    'Sports & Fitness': ['Gym Gear', 'Activewear', 'Cycling', 'Yoga']
}

prod_cats = np.random.choice(categories, n_products)
prod_subcats = [np.random.choice(sub_cats[c]) for c in prod_cats]
base_costs = np.round(np.random.uniform(150, 12000, n_products), 2)

products = pd.DataFrame({
    'product_id': [f'PROD-{100 + i}' for i in range(n_products)],
    'category': prod_cats,
    'sub_category': prod_subcats,
    'cost_price': base_costs,
    'selling_price': np.round(base_costs * np.random.uniform(1.25, 1.65, n_products), 2)
})

# --- 3. GENERATE ORDERS TABLE (50,000 Rows) ---
n_orders = 50000
order_dates = np.random.choice(pd.date_range('2025-01-01', '2026-10-31', freq='h'), n_orders)

orders = pd.DataFrame({
    'order_id': [f'ORD-{100000 + i}' for i in range(n_orders)],
    'order_date': order_dates,
    'customer_id': np.random.choice(customers['customer_id'].unique(), n_orders),
    'product_id': np.random.choice(products['product_id'], n_orders),
    'quantity': np.random.randint(1, 6, n_orders),
    'discount_pct': np.random.choice([0, 5, 10, 15, 20, 30], n_orders, p=[0.25, 0.20, 0.20, 0.15, 0.12, 0.08]),
    'payment_mode': np.random.choice(['UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery'], n_orders, p=[0.45, 0.25, 0.15, 0.15]),
    'shipping_days': np.random.randint(1, 10, n_orders),
    'order_status': np.random.choice(['Delivered', 'Returned', 'Cancelled'], n_orders, p=[0.82, 0.11, 0.07])
})
# Inject messy nulls and duplicates
orders.loc[np.random.choice(orders.index, 600), 'payment_mode'] = np.nan
orders = pd.concat([orders, orders.sample(250)], ignore_index=True)

# --- 4. PANDAS DATA CLEANING & FEATURE ENGINEERING ---
customers_clean = customers.drop_duplicates(subset=['customer_id']).copy()
customers_clean['customer_segment'] = customers_clean['customer_segment'].fillna('Consumer')

orders_clean = orders.drop_duplicates(subset=['order_id']).copy()
orders_clean['payment_mode'] = orders_clean['payment_mode'].fillna('Unknown')
orders_clean['order_date'] = pd.to_datetime(orders_clean['order_date'])
orders_clean['order_year_month'] = orders_clean['order_date'].dt.to_period('M').astype(str)

# Export clean CSVs for PostgreSQL & Power BI
customers_clean.to_csv('clean_customers.csv', index=False)
products.to_csv('clean_products.csv', index=False)
orders_clean.to_csv('clean_orders.csv', index=False)

print(f"Done! Customers: {len(customers_clean)}, Products: {len(products)}, Orders: {len(orders_clean)}")
