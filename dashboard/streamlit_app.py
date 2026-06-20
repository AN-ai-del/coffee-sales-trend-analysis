import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Coffee Sales Trend Analysis",
    page_icon="☕",
    layout="wide"
)

df = pd.read_csv("./data/processed/coffee_sales_processed.csv")

st.title("☕ Sales Trend and Time-Based Performance Analysis")
st.subheader("Afficionado Coffee Roasters")

st.sidebar.header("Dashboard Filters")

store_filter = st.sidebar.multiselect(
    "Select Store Location",
    options=sorted(df["store_location"].unique()),
    default=sorted(df["store_location"].unique())
)

category_filter = st.sidebar.multiselect(
    "Select Product Category",
    options=sorted(df["product_category"].unique()),
    default=sorted(df["product_category"].unique())
)

time_bucket_filter = st.sidebar.multiselect(
    "Select Time Bucket",
    options=sorted(df["time_bucket"].unique()),
    default=sorted(df["time_bucket"].unique())
)

hour_range = st.sidebar.slider(
    "Select Hour Range",
    min_value=int(df["hour"].min()),
    max_value=int(df["hour"].max()),
    value=(int(df["hour"].min()), int(df["hour"].max()))
)

filtered_df = df[
    (df["store_location"].isin(store_filter)) &
    (df["product_category"].isin(category_filter)) &
    (df["time_bucket"].isin(time_bucket_filter)) &
    (df["hour"].between(hour_range[0], hour_range[1]))
]

st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="coffee_sales_filtered.csv",
    mime="text/csv"
)

total_revenue = filtered_df["revenue"].sum()
total_transactions = filtered_df["transaction_id"].nunique()
total_quantity = filtered_df["transaction_qty"].sum()
avg_order_value = filtered_df["revenue"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Transactions", f"{total_transactions:,}")
col3.metric("Quantity Sold", f"{total_quantity:,}")
col4.metric("Average Order Value", f"${avg_order_value:.2f}")

st.divider()

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

st.divider()

category_revenue = (
    filtered_df.groupby("product_category")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

fig_category = px.bar(
    category_revenue,
    x="product_category",
    y="revenue",
    title="Revenue by Product Category",
    labels={"product_category": "Product Category", "revenue": "Revenue"}
)

st.plotly_chart(fig_category, use_container_width=True)

top_products = (
    filtered_df.groupby("product_detail")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
    .head(10)
)

fig_top_products = px.bar(
    top_products,
    x="revenue",
    y="product_detail",
    orientation="h",
    title="Top 10 Products by Revenue",
    labels={"product_detail": "Product", "revenue": "Revenue"}
)

fig_top_products.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig_top_products, use_container_width=True)

bucket_revenue = (
    filtered_df.groupby("time_bucket")["revenue"]
    .sum()
    .reset_index()
    .sort_values(by="revenue", ascending=False)
)

fig_bucket = px.bar(
    bucket_revenue,
    x="time_bucket",
    y="revenue",
    title="Revenue by Time Bucket",
    labels={"time_bucket": "Time Bucket", "revenue": "Revenue"}
)

st.plotly_chart(fig_bucket, use_container_width=True)

st.header("Business Recommendations")

st.success("""
✅ Increase staffing during morning rush hours (8 AM - 11 AM)

✅ Focus inventory planning on Coffee and Tea products

✅ Replicate successful operational practices across all stores

✅ Introduce evening promotions to improve low-demand periods

✅ Use demand-based workforce scheduling to improve efficiency
""")

st.info("""
Dataset Limitation:

The dataset contains transaction time but does not include transaction dates. Therefore, daily, weekly, monthly, weekday, and weekend trend analyses cannot be performed accurately.

The dashboard focuses on intraday sales patterns, store performance, product performance, and operational insights.
""")