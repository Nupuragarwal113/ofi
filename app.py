import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("NexGen Predictive Delivery Optimizer")

# If using Streamlit Cloud, use st.file_uploader. For local, use pd.read_csv directly.
orders = pd.read_csv("orders.csv")
delivery = pd.read_csv("delivery_performance.csv")
costs = pd.read_csv("cost_breakdown.csv")

st.header("Raw Data Samples")
st.write("Orders:", orders.head())
st.write("Delivery:", delivery.head())
st.write("Costs:", costs.head())

delivery['delay'] = delivery['actual_delivery_time'] - delivery['promised_delivery_time']
delivery['is_late'] = delivery['delay'] > 0

carrier_list = delivery['carrier'].dropna().unique()
selected_carrier = st.selectbox("Filter by Carrier:", carrier_list)

filtered_data = delivery[delivery['carrier'] == selected_carrier]

st.subheader("Delay Rate by Carrier")
delay_rate_by_carrier = delivery.groupby('carrier')['is_late'].mean()
st.bar_chart(delay_rate_by_carrier)

st.subheader("Delays by Product Category")
merged = pd.merge(orders, delivery, on='order_id')
delay_by_category = merged.groupby('product_category')['is_late'].mean()
st.bar_chart(delay_by_category)

st.subheader("Ratings: Late vs On-Time")
late_ratings = delivery[delivery['is_late']]['customer_rating']
ontime_ratings = delivery[~delivery['is_late']]['customer_rating']
fig, ax = plt.subplots()
ax.hist([late_ratings, ontime_ratings], label=['Late', 'On-Time'], bins=5, alpha=0.7)
ax.legend()
st.pyplot(fig)

st.subheader("Cost Impact of Delays")
merged_costs = pd.merge(delivery, costs, on='order_id')
avg_costs = merged_costs.groupby('is_late')['total_cost'].mean()
st.bar_chart(avg_costs)

st.subheader("Current At-Risk Orders")
at_risk = delivery[(delivery['promised_delivery_time'] - pd.Timestamp.now()) < pd.Timedelta(hours=2)]
st.write(at_risk)

st.subheader("Estimated Savings")
late_rate = delivery['is_late'].mean()
monthly_orders = len(delivery)
avg_delay_cost = merged_costs[merged_costs['is_late']]['total_cost'].mean()
potential_saving = late_rate * monthly_orders * avg_delay_cost * 0.2  # assume 20% drop with intervention
st.write(f"Estimated monthly saving with optimizer: ₹{potential_saving:.2f}")
