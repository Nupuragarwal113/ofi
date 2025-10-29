# NexGen Predictive Delivery Optimizer

## Overview
This Streamlit dashboard helps NexGen Logistics analyze delivery delays, carrier performance, customer satisfaction, and cost impact, enabling more predictive and data-driven operations.

## Features
- Visualizes delay rates by carrier
- Shows distribution of late vs on-time deliveries (pie chart)
- Compares customer ratings (late vs on-time)
- Calculates average cost impact of delays
- Lists all at-risk (delayed) orders
- Estimates actionable cost savings

## Setup Instructions
1. Clone/download this repository and unzip the folder.
2. Ensure the following files are in your project folder:
   - `app.py`
   - `orders.csv`, `delivery_performance.csv`, `cost_breakdown.csv`
   - `requirements.txt`
3. Install required dependencies: pip install -r requirements.txt
4. Run the dashboard: streamlit run app.py
5. Upload your CSV files as prompted (or keep them in the folder).

## Requirements
- Python 3.7+
- Required packages: streamlit, pandas, matplotlib

## How to Use
- Use filter widgets to focus on specific carriers.
- Read explanations below each chart for actionable insights.
- Explore the “At-Risk Orders” table for immediate operational follow-up.

## Notes
- The visualization by "Product Category" was omitted, as this data was unavailable.
- All other core features and business impact calculations are included.
