# Business Requirement Document (BRD)

**Project Name:** Ecommerce-Sales-Profit-Analysis
**Author:** Arati Sutar  
**Date:** November 2026  
**Stakeholders:** Retail Operations Lead, Pricing Team, Logistics Manager  

---

## 1. Background and Problem Statement
Our e-commerce platform processes over 50,000 orders across four major Indian regions (West, South, North, and East). Over the past few quarters, order volume has remained steady, but overall net profit margins have dropped and product return rates have increased. 

Currently, order transactions, customer details, and product pricing are stored in separate files. Without combining these records, management cannot clearly see which discounts are hurting margins, which cities generate the highest profit, or why certain orders are being returned.

## 2. Project Goals
The goal of this analysis is to combine our sales, customer, and product records into a single reporting model to answer three operational questions:
1. **Profitability & Pricing:** Which product categories make the most money, and at what discount percentage do orders start losing money?
2. **Customer & Regional Performance:** Which regions, cities, and customer segments bring in the highest revenue and average order value?
3. **Returns & Delivery Risk:** How strongly do shipping delays and payment methods (such as Cash on Delivery) affect return and cancellation rates?

## 3. Data Sources
The analysis uses three cleaned tables covering 50,000 orders, 5,000 customers, and 100 products:
* **Orders Table (`clean_orders.csv`):** Order ID, order date, customer ID, product ID, quantity ordered, discount percentage, payment mode, shipping days, and final order status (`Delivered`, `Returned`, `Cancelled`).
* **Customers Table (`clean_customers.csv`):** Customer ID, account segment (`Consumer`, `Corporate`, `Prime Member`), city, region, and registration date.
* **Products Table (`clean_products.csv`):** Product ID, category, sub-category, unit cost price, and selling price.

## 4. Specific Questions to Answer (Scope)
The SQL analysis and Power BI report must answer the following 10 questions:
1. What are the total delivered orders, net revenue, total cost, and net profit?
2. How do revenue, profit, and profit margin compare across product categories and sub-categories?
3. How does average profit per order change across different discount tiers (0% to 30%), and how many orders are sold below cost?
4. What percentage of total revenue comes from each region?
5. Which are the top 3 profit-generating cities in each region?
6. What is the Month-over-Month (MoM) revenue growth trend?
7. What is the Average Order Value (AOV) across Consumer, Corporate, and Prime Member segments?
8. How do return and cancellation rates differ between fast deliveries (1–3 days), standard deliveries (4–6 days), and delayed deliveries (7+ days)?
9. Which payment methods have the highest rate of returned or cancelled orders?
10. How many customers fall into high-value repeat tiers versus occasional one-time buyers?

## 5. Expected Deliverables
* **Cleaned Datasets:** Deduplicated CSV files with standardized date formats and no missing payment or segment values.
* **SQL Query Output:** Documented SQL queries and result tables answering all 10 scope questions.
* **Power BI Dashboard:** A 3-page interactive report covering Executive Sales Overview, Discount & Pricing Analysis, and Logistics & Customer Segments.
