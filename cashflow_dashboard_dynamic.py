import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate cash flow
def calculate_cash_flow(months, savings, sales, consulting_costs, licensing_costs, cloud_costs):
    data = []
    cumulative_cash_flow = 0
    for month in range(1, months + 1):
        consulting_cost = consulting_costs.get(month, 0)
        licensing_cost = licensing_costs.get(month, 0)
        cloud_cost = cloud_costs.get(month, 0)
        total_cost = consulting_cost + licensing_cost + cloud_cost
        total_revenue = savings + sales if month >= 3 else 0
        cash_flow = total_revenue - total_cost
        cumulative_cash_flow += cash_flow
        data.append([month, consulting_cost, licensing_cost, cloud_cost, total_cost, total_revenue, cash_flow, cumulative_cash_flow])
    return pd.DataFrame(data, columns=["Month", "Consulting Cost", "Licensing Cost", "Cloud Cost", "Total Cost", "Total Revenue", "Cash Flow", "Cumulative Cash Flow"])

# Streamlit UI
st.title("Interactive Cash Flow Dashboard")

# Sidebar inputs for parameters
st.sidebar.header("Project Stages and Costs")

# Stage durations
stage_durations = {
    "Stage 1 (Initial Setup)": 3,
    "Stage 2 (Manufacturing)": 1,
    "Stage 3 (Accounting)": 3.5
}

# Collect consulting, licensing, and cloud costs for each stage
consulting_costs = {}
licensing_costs = {}
cloud_costs = {}

month_counter = 1
for stage, duration in stage_durations.items():
    st.sidebar.subheader(stage)
    consulting_cost = st.sidebar.number_input(f"{stage} - Consulting Cost ($/Month)", value=4500 if "Initial" in stage else 1500, step=100, format="%d")
    licensing_cost = st.sidebar.number_input(f"{stage} - Licensing Cost ($/Month)", value=170 if "Initial" in stage else 340, step=10, format="%d")
    cloud_cost = st.sidebar.number_input(f"{stage} - Cloud Cost ($/Month)", value=91.25 if "Initial" in stage else 165.75, step=1.0, format="%.2f")
    
    for month in range(month_counter, month_counter + int(duration)):
        consulting_costs[month] = consulting_cost
        licensing_costs[month] = licensing_cost
        cloud_costs[month] = cloud_cost
    
    month_counter += int(duration)

# Savings and Sales Revenue Inputs
st.sidebar.header("Financial Parameters")
months = st.sidebar.slider("Number of Months", 1, 12, 8)
savings = st.sidebar.number_input("Monthly Savings ($)", value=6000, step=100)
sales = st.sidebar.number_input("Monthly Sales Revenue ($)", value=5000, step=100)

# Calculate Cash Flow
df = calculate_cash_flow(months, savings, sales, consulting_costs, licensing_costs, cloud_costs)

# Display Data
st.header("Cash Flow Data")
st.dataframe(df)

# Visualize Cash Flow
st.header("Cash Flow Chart")
fig, ax = plt.subplots()
ax.plot(df["Month"], df["Cumulative Cash Flow"], label="Cumulative Cash Flow", marker="o")
ax.plot(df["Month"], df["Total Revenue"], label="Total Revenue", linestyle="--")
ax.plot(df["Month"], df["Total Cost"], label="Total Cost", linestyle="--")
ax.set_xlabel("Month")
ax.set_ylabel("Amount ($)")
ax.set_title("Cash Flow Analysis")
ax.legend()
st.pyplot(fig)

# Save user interactions
if st.button("Save Data"):
    df.to_csv("user_interactions.csv", index=False)
    st.success("User interactions saved!")
