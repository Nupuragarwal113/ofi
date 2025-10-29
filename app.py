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

# Visualization 1: Delay Rate by Carrier
st.subheader("Delay Rate by Carrier")
delay_rate_by_carrier = delivery.groupby('Carrier')['is_late'].mean()
st.bar_chart(delay_rate_by_carrier)
st.markdown("**This chart shows average delay rates for each carrier, letting you spot which partners need attention.**")

# Visualization 2: Proportion of Late vs On-Time Deliveries (Pie chart)
st.subheader("Proportion of Late vs On-Time Deliveries")
pie_data = delivery['is_late'].value_counts()
labels = ['On-Time', 'Late']
fig, ax = plt.subplots()
ax.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
st.markdown("**This chart breaks down total deliveries into on-time and late, giving a sense of overall performance.**")

# Visualization 3: Ratings for Late vs On-Time Deliveries
if 'Customer_Rating' in delivery.columns:
    st.subheader("Ratings: Late vs On-Time")
    late_ratings = delivery[delivery['is_late']]['Customer_Rating']
    ontime_ratings = delivery[~delivery['is_late']]['Customer_Rating']
    fig, ax = plt.subplots()
    ax.hist([late_ratings, ontime_ratings], label=['Late', 'On-Time'], bins=5, alpha=0.7)
    ax.set_xlabel("Customer Rating")
    ax.set_ylabel("Number of Deliveries")
    ax.legend()
    st.pyplot(fig)
    st.markdown("**This chart compares customer ratings for late vs on-time orders, showing the impact of delays on satisfaction.**")
else:
    st.write("Column 'Customer_Rating' not found in delivery dataset.")

# Visualization 4: Cost Impact of Delays
if 'Order_ID' in delivery.columns and 'Order_ID' in costs.columns:
    merged_costs = pd.merge(delivery, costs, on='Order_ID')
    if 'Delivery_Cost_INR' in merged_costs.columns:
        avg_costs = merged_costs.groupby('is_late')['Delivery_Cost_INR'].mean()
        st.subheader("Cost Impact of Delays")
        st.bar_chart(avg_costs)
        st.markdown("**This shows the average delivery cost for late vs on-time orders, helping analyze financial impact.**")
    else:
        st.write("Column 'Delivery_Cost_INR' not found in cost breakdown dataset.")
else:
    st.write("Column 'Order_ID' missing in delivery or cost dataset.")

# Table: Current At-Risk Orders
st.subheader("Current At-Risk Orders")
# For example, orders delayed by more than 1 day
at_risk = delivery[delivery['delay'] > 1]
st.write(at_risk)
st.markdown("**This table lists orders that are significantly delayed, enabling targeted follow-up.**")

# Estimated Savings
late_rate = delivery['is_late'].mean()
monthly_orders = len(delivery)
if 'Delivery_Cost_INR' in merged_costs.columns:
    avg_delay_cost = merged_costs[merged_costs['is_late']]['Delivery_Cost_INR'].mean()
    potential_saving = late_rate * monthly_orders * avg_delay_cost * 0.2  # assume 20% drop with intervention
    st.subheader("Estimated Savings")
    st.write(f"Estimated monthly saving with optimizer: ₹{potential_saving:.2f}")
    st.markdown("**Potential monthly savings calculated assuming a 20% reduction in late deliveries.**")
else:
    st.write("Cost information not available to estimate savings.")
