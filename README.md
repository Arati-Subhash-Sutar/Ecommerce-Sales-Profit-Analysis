# End-to-End E-Commerce Sales, Profitability & Logistics Analysis

## Project Overview
This project analyzes **50,000+ e-commerce orders** across India to identify profit margin leakage, evaluate promotional discount effectiveness, and uncover operational bottlenecks causing high return and cancellation rates. 

Following an end-to-end data analytics workflow, the project begins with a formal **Business Requirement Document (BRD)**, moves through automated data cleaning in **Python (pandas)**, answers 10 core business questions using **SQL**, and delivers an interactive **3-page Power BI dashboard** for executive decision-making.

---

## Business Objectives
* **Margin & Discount Optimization:** Identify which product sub-categories generate the highest net profit and determine the exact discount threshold where orders become unprofitable.
* **Logistics & Payment Risk Analysis:** Measure how shipping delays (7+ days) and payment modes (Cash on Delivery vs. Digital Payments) impact order failure rates.
* **Customer & Regional Segmentation:** Rank top-performing cities by region and segment active buyers by order frequency and lifetime spend.

---

## Tech Stack & Data Architecture
* **Data Cleaning & Transformation:** Python (`pandas`, `numpy`)
* **Relational Querying & Analysis:** SQL (`DuckDB` / `PostgreSQL` / `Oracle` compatible Star Schema)
* **Business Intelligence & Reporting:** Power BI Desktop (`DAX`, Data Modeling)

### Star Schema Data Model
The dataset is structured into three relational tables:
1. **`orders` (Fact Table — 50,000 rows):** Order ID, order date, customer ID, product ID, quantity, discount percentage, payment mode, shipping days, and order status (`Delivered`, `Returned`, `Cancelled`).
2. **`customers` (Dimension Table — 5,000 rows):** Customer ID, segment (`Consumer`, `Corporate`, `Prime Member`), city, region (`West`, `South`, `North`, `East`), and signup date.
3. **`products` (Dimension Table — 100 rows):** Product ID, category, sub-category, unit cost price, and selling price.

---

## Repository Structure
```text
Ecommerce-Sales-Profit-Analysis/
├── BRD.md                          # Business Requirement Document & stakeholder scope
├── README.md                       # Project documentation and key insights
├── data/
│   ├── clean_customers.csv         # Cleaned customer dimension table
│   ├── clean_products.csv          # Product catalog & pricing table
│   └── clean_orders.csv            # Cleaned transactional fact table
├── scripts/
│   ├── data_cleaning.py            # Python script for deduplication & null handling
│   └── run_sql_analysis.py         # Script executing 10 analytical SQL queries
├── sql_outputs/
│   └── sql_query_results.txt       # Formatted output tables for all 10 SQL queries
└── powerbi/
    ├── ecommerce_dashboard.pbix    # Interactive Power BI report file
    ├── page1_executive_overview.png
    ├── page2_discount_analysis.png
    └── page3_logistics_customers.png
```

---

## Key Analytical Insights & Recommendations
* **Cap Promotional Discounts at 20%:** SQL discount erosion analysis revealed that promotional discounts of **25% to 30%** eroded net profit margins and pushed multiple orders below unit cost price. Capping standard promotions at 20% protects profitability while maintaining conversion volume.
* **Optimize Last-Mile Delivery Speed:** Orders delivered within **1–3 days** maintained significantly lower return rates compared to orders delayed beyond **7 days**. Prioritizing faster courier partners in high-volume metro cities can directly reduce return losses.
* **Incentivize Prepaid Digital Payments:** **Cash on Delivery (COD)** orders exhibited higher return and cancellation rates than UPI and Credit Card transactions. Offering a small instant UPI discount can shift buyers toward prepaid orders and lower failed delivery costs.

---

## Power BI Dashboard Preview
*(Screenshots will be visible once uploaded to the `powerbi/` folder)*

### 1. Executive Sales & Profit Overview
![Executive Overview](powerbi/page1_executive_overview.png)

### 2. Discount & Pricing Optimization
![Discount Analysis](powerbi/page2_discount_analysis.png)

### 3. Logistics, Returns & Customer Segments
![Logistics and Customers](powerbi/page3_logistics_customers.png)

---

## How to Run This Project Locally
1. Clone this repository or download the project folder.
2. Install the required Python libraries:
   ```bash
   pip install pandas numpy duckdb
   ```
3. Run `scripts/run_sql_analysis.py` to execute all 10 SQL business queries against the CSV files in `data/`.
4. Open `powerbi/ecommerce_dashboard.pbix` in Power BI Desktop to interact with the filters and visuals.
