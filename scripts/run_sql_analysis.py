import duckdb

# 1. Connecting to duckdb and loading all .csv files
con = duckdb.connect()
con.execute("CREATE TABLE customers AS SELECT * FROM read_csv_auto('clean_customers.csv');")
con.execute("CREATE TABLE products AS SELECT * FROM read_csv_auto('clean_products.csv');")
con.execute("CREATE TABLE orders AS SELECT * FROM read_csv_auto('clean_orders.csv');")

# 2. Dictionalry with all solved problems
queries = {
    "PROBLEM 1: Overall Net Revenue, Total Cost, and Net Profit": """
        SELECT 
            COUNT(o.order_id) AS delivered_orders,
            ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)), 2) AS net_revenue,
            ROUND(SUM(o.quantity * p.cost_price), 2) AS total_cost,
            ROUND(SUM((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)), 2) AS net_profit
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Delivered';
    """,

    "PROBLEM 2: Category & Sub-Category Profit Margin Ranking": """
        SELECT 
            p.category,
            p.sub_category,
            ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)), 2) AS revenue,
            ROUND(SUM((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)), 2) AS profit,
            ROUND(
                (SUM((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)) /
                 SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0))) * 100, 2
            ) AS profit_margin_pct
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Delivered'
        GROUP BY p.category, p.sub_category
        ORDER BY profit DESC;
    """,

    "PROBLEM 3: Discount Erosion Analysis (Loss-Making Tiers)": """
        SELECT 
            o.discount_pct,
            COUNT(o.order_id) AS total_orders,
            ROUND(AVG((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)), 2) AS avg_profit_per_order,
            SUM(CASE WHEN (p.selling_price * (1 - o.discount_pct / 100.0)) < p.cost_price THEN 1 ELSE 0 END) AS loss_making_orders
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Delivered'
        GROUP BY o.discount_pct
        ORDER BY o.discount_pct;
    """,

    "PROBLEM 4: Regional Revenue Contribution % (Window Function)": """
        SELECT 
            c.region,
            COUNT(o.order_id) AS orders,
            ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)), 2) AS regional_revenue,
            ROUND(
                SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) * 100.0 /
                SUM(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0))) OVER(), 2
            ) AS revenue_share_pct
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Delivered'
        GROUP BY c.region
        ORDER BY regional_revenue DESC;
    """,

    "PROBLEM 5: Top 3 Most Profitable Cities per Region (CTE + DENSE_RANK)": """
        WITH city_profits AS (
            SELECT 
                c.region,
                c.city,
                ROUND(SUM((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)), 2) AS total_profit,
                DENSE_RANK() OVER(PARTITION BY c.region ORDER BY SUM((o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) - (o.quantity * p.cost_price)) DESC) AS city_rank
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_status = 'Delivered'
            GROUP BY c.region, c.city
        )
        SELECT * FROM city_profits WHERE city_rank <= 3;
    """,

    "PROBLEM 6: Month-over-Month (MoM) Revenue Growth Rate (LAG)": """
        WITH monthly_sales AS (
            SELECT 
                o.order_year_month,
                ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)), 2) AS current_month_rev
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_status = 'Delivered'
            GROUP BY o.order_year_month
        )
        SELECT 
            order_year_month,
            current_month_rev,
            LAG(current_month_rev) OVER(ORDER BY order_year_month) AS prev_month_rev,
            ROUND(((current_month_rev - LAG(current_month_rev) OVER(ORDER BY order_year_month)) / 
                   LAG(current_month_rev) OVER(ORDER BY order_year_month)) * 100, 2) AS mom_growth_pct
        FROM monthly_sales
        ORDER BY order_year_month;
    """,

    "PROBLEM 7: Customer Segment Value & Average Order Value (AOV)": """
        SELECT 
            c.customer_segment,
            COUNT(DISTINCT c.customer_id) AS active_customers,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)) / COUNT(o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_status = 'Delivered'
        GROUP BY c.customer_segment
        ORDER BY avg_order_value DESC;
    """,

    "PROBLEM 8: Shipping Delay Impact on Return & Cancellation Rates": """
        SELECT 
            CASE 
                WHEN shipping_days <= 3 THEN 'Fast (1-3 Days)'
                WHEN shipping_days BETWEEN 4 AND 6 THEN 'Standard (4-6 Days)'
                ELSE 'Delayed (7+ Days)'
            END AS delivery_speed,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2) AS return_rate_pct,
            ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2) AS cancellation_rate_pct
        FROM orders
        GROUP BY delivery_speed
        ORDER BY return_rate_pct DESC;
    """,

    "PROBLEM 9: Payment Mode Risk Analysis (COD vs Digital)": """
        SELECT 
            payment_mode,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(CASE WHEN order_status IN ('Returned', 'Cancelled') THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 2) AS failed_order_rate_pct
        FROM orders
        GROUP BY payment_mode
        ORDER BY failed_order_rate_pct DESC;
    """,

    "PROBLEM 10: RFM-Style Customer Tiering (Champions vs Occasional)": """
        WITH customer_metrics AS (
            SELECT 
                c.customer_id,
                c.customer_segment,
                COUNT(o.order_id) AS order_frequency,
                ROUND(SUM(o.quantity * p.selling_price * (1 - o.discount_pct / 100.0)), 2) AS monetary_value
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN products p ON o.product_id = p.product_id
            WHERE o.order_status = 'Delivered'
            GROUP BY c.customer_id, c.customer_segment
        )
        SELECT 
            CASE 
                WHEN order_frequency >= 12 AND monetary_value >= 150000 THEN 'VIP Champion'
                WHEN order_frequency >= 6 THEN 'Loyal Customer'
                ELSE 'Occasional Buyer'
            END AS customer_tier,
            COUNT(customer_id) AS customer_count,
            ROUND(AVG(monetary_value), 2) AS avg_lifetime_spend
        FROM customer_metrics
        GROUP BY customer_tier
        ORDER BY avg_lifetime_spend DESC;
    """
}

# 3. Printing and saving all results
with open("sql_query_results.txt", "w") as f:
    for title, sql in queries.items():
        df_result = con.execute(sql).df()
        output_text = df_result.to_string(index=False)
        
        print("=" * 70)
        print(title)
        print("=" * 70)
        print(output_text)
        print("\n")
        
        f.write("=" * 70 + "\n")
        f.write(title + "\n")
        f.write("=" * 70 + "\n")
        f.write(output_text + "\n\n")

print("Success! All 10 queries executed and saved to sql_query_results.txt")
