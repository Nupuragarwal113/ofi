import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("NexGen Predictive Delivery Optimizer")

# Load data
orders = pd.read_csv("orders.csv")
delivery = pd.read_csv("delivery_performance.csv")
costs = pd.read_csv("cost_breakdown.csv")

# Show raw data samples
st.header("Raw Data Samples")
st.write("Orders:", orders.head())
st.write("Delivery:", delivery.head())
st.write("Costs:", costs.head())

# Calculate delay in days
delivery['delay'] = delivery['Actual_Delivery_Days'] - delivery['Promised_Delivery_Days']

# Flag if order was late
delivery['is_late'] = delivery['delay'] > 0

# Carrier filter widget
carrier_list = delivery['Carrier'].dropna().unique()
selected_carrier = st.selectbox("Filter by Carrier:", carrier_list)

# Filter data based on selected carrier
filtered_data = delivery[delivery['Carrier'] == selected_carrier]

# Delay Rate by Carrier (use correct column name 'Carrier' with capital C)
st.subheader("Delay Rate by Carrier")
delay_rate_by_carrier = delivery.groupby('Carrier')['is_late'].mean()
st.bar_chart(delay_rate_by_carrier)

# Delays by Product Category
# Merge on 'Order_ID' with correct key and case matching
merged = pd.merge(orders, delivery, left_on='Order_ID', right_on='Order_ID')

# Use correct column 'product_category' - check if it exists in orders, otherwise adjust accordingly
if 'product_category' in merged.columns:
    delay_by_category = merged.groupby('product_category')['is_late'].mean()
    st.subheader("Delays by Product Category")
    st.bar_chart(delay_by_category)
else:
    st.write("Column 'product_category' not found in orders dataset.")

# Ratings: Late vs On-Time, use exact column names with case sensitivity
if 'Customer_Rating' in delivery.columns:
    st.subheader("Ratings: Late vs On-Time")
    late_ratings = delivery[delivery['is_late']]['Customer_Rating']
    ontime_ratings = delivery[~delivery['is_late']]['Customer_Rating']
    fig, ax = plt.subplots()
    ax.hist([late_ratings, ontime_ratings], label=['Late', 'On-Time'], bins=5, alpha=0.7)
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Column 'Customer_Rating' not found in delivery dataset.")

# Cost Impact of Delays
# Merge costs and delivery on 'Order_ID'
if 'Order_ID' in delivery.columns and 'Order_ID' in costs.columns:
    merged_costs = pd.merge(delivery, costs, on='Order_ID')
    if 'Delivery_Cost_INR' in merged_costs.columns:
        avg_costs = merged_costs.groupby('is_late')['Delivery_Cost_INR'].mean()
        st.subheader("Cost Impact of Delays")
        st.bar_chart(avg_costs)
    else:
        st.write("Column 'Delivery_Cost_INR' not found in cost breakdown dataset.")
else:
    st.write("Column 'Order_ID' missing in delivery or cost dataset.")

# Current At-Risk Orders
# Adjust logic because you don't have datetime columns but day counts, so remove this, or replace with simple late orders
st.subheader("Current At-Risk Orders")
at_risk = delivery[delivery['delay'] > 1]  # For example, orders delayed by more than 1 day
st.write(at_risk)

# Estimated Savings
late_rate = delivery['is_late'].mean()
monthly_orders = len(delivery)
if 'Delivery_Cost_INR' in merged_costs.columns:
    avg_delay_cost = merged_costs[merged_costs['is_late']]['Delivery_Cost_INR'].mean()
    potential_saving = late_rate * monthly_orders * avg_delay_cost * 0.2  # assume 20% drop with intervention
    st.subheader("Estimated Savings")
    st.write(f"Estimated monthly saving with optimizer: ₹{potential_saving:.2f}")
else:
    st.write("Cost information not available to estimate savings.")

