import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Coffee Sales Trend Analysis",
    page_icon="☕",
    layout="wide"
)

# Load Data
df = pd.read_csv("data/processed/coffee_sales_processed.csv")

# Title
st.title("☕ Sales Trend and Time-Based Performance Analysis")
st.subheader("Afficionado Coffee Roasters")

# Sidebar Filters
st.sidebar.header("Filters")

store_filter = st.sidebar.multiselect(
    "Select Store Location",
    options=df["store_location"].unique(),
    default=df["store_location"].unique()
)

time_bucket_filter = st.sidebar.multiselect(
    "Select Time Bucket",
    options=df["time_bucket"].unique(),
    default=df["time_bucket"].unique()
)

hour_range = st.sidebar.slider(
    "Select Hour Range",
    min_value=int(df["hour"].min()),
    max_value=int(df["hour"].max()),
    value=(int(df["hour"].min()), int(df["hour"].max()))
)

filtered_df = df[
    (df["store_location"].isin(store_filter)) &
    (df["time_bucket"].isin(time_bucket_filter)) &
    (df["hour"].between(hour_range[0], hour_range[1]))
]

# KPI Section
total_revenue = filtered_df["revenue"].sum()
total_transactions = filtered_df["transaction_id"].nunique()
total_quantity = filtered_df["transaction_qty"].sum()
avg_order_value = filtered_df["revenue"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Transactions", f"{total_transactions:,}")
col3.metric("Quantity Sold", f"{total_quantity:,}")
col4.metric("Avg Order Value", f"${avg_order_value:.2f}")

st.divider()

# Hourly Revenue
hourly_revenue = (
    filtered_df.groupby("hour")["revenue"]
    .sum()
    .reset_index()
)

fig_hourly_revenue = px.bar(
    hourly_revenue,
    x="hour",
    y="revenue",
    title="Revenue by Hour",
    labels={"hour": "Hour of Day", "revenue": "Revenue"}
)

st.plotly_chart(fig_hourly_revenue, use_container_width=True)

# Hourly Transactions
hourly_transactions = (
    filtered_df.groupby("hour")["transaction_id"]
    .count()
    .reset_index(name="transactions")
)

fig_hourly_transactions = px.line(
    hourly_transactions,
    x="hour",
    y="transactions",
    markers=True,
    title="Transaction Volume by Hour",
    labels={"hour": "Hour of Day", "transactions": "Transactions"}
)

st.plotly_chart(fig_hourly_transactions, use_container_width=True)

# Store Revenue
store_revenue = (
    filtered_df.groupby("store_location")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

fig_store = px.bar(
    store_revenue,
    x="store_location",
    y="revenue",
    title="Revenue by Store Location",
    labels={"store_location": "Store Location", "revenue": "Revenue"}
)

st.plotly_chart(fig_store, use_container_width=True)