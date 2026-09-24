from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.ai_models import ai_insights, customer_segments, detect_anomalies
from src.preprocessing import load_and_clean

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "data" / "supermarket_sales.csv"

st.set_page_config(
    page_title="Supermarket Sales Analytics with AI",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def get_data():
    return load_and_clean(DATA_PATH)


df, cleaning_info = get_data()

st.title("📊 Supermarket Sales Analytics with AI")
st.caption(
    "Data cleaning → analysis → AI insights → business decisions"
)

with st.sidebar:
    st.header("Filters")

    branches = st.multiselect(
        "Branch",
        sorted(df["Branch"].unique()),
        default=sorted(df["Branch"].unique()),
    )

    products = st.multiselect(
        "Product line",
        sorted(df["Product_Line"].unique()),
        default=sorted(df["Product_Line"].unique()),
    )

    customers = st.multiselect(
        "Customer type",
        sorted(df["Customer_Type"].unique()),
        default=sorted(df["Customer_Type"].unique()),
    )

filtered = df[
    df["Branch"].isin(branches)
    & df["Product_Line"].isin(products)
    & df["Customer_Type"].isin(customers)
].copy()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total sales",
    f"₹{filtered['Total'].sum():,.0f}"
)

c2.metric(
    "Transactions",
    f"{len(filtered):,}"
)

c3.metric(
    "Average basket",
    f"₹{filtered['Total'].mean():,.0f}"
)

c4.metric(
    "Average rating",
    f"{filtered['Rating'].mean():.2f}/10"
)

trend = (
    filtered.groupby("Date", as_index=False)["Total"]
    .sum()
)

branch = (
    filtered.groupby("Branch", as_index=False)["Total"]
    .sum()
    .sort_values("Total", ascending=False)
)

product = (
    filtered.groupby("Product_Line", as_index=False)["Total"]
    .sum()
    .sort_values("Total", ascending=False)
)

left, right = st.columns(2)

with left:
    st.subheader("Sales trend")

    st.plotly_chart(
        px.line(
            trend,
            x="Date",
            y="Total",
            markers=True,
        ),
        use_container_width=True,
    )

with right:
    st.subheader("Revenue by branch")

    st.plotly_chart(
        px.bar(
            branch,
            x="Branch",
            y="Total",
            text_auto=".2s",
        ),
        use_container_width=True,
    )

st.subheader("Revenue by product line")

st.plotly_chart(
    px.bar(
        product,
        x="Total",
        y="Product_Line",
        orientation="h",
        text_auto=".2s",
    ),
    use_container_width=True,
)

with st.expander("🔎 Data cleaning summary"):
    st.json(cleaning_info)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("AI-generated business insights")

    for item in ai_insights(filtered):
        st.write("•", item)

with col2:
    st.subheader("AI anomaly detection")

    anomalies = detect_anomalies(filtered)

    flagged = anomalies[
        anomalies["Anomaly"]
    ].head(10)

    anomaly_count = anomalies[
        anomalies["Anomaly"]
    ].shape[0]

    st.write(
        f"Flagged transactions: "
        f"{anomaly_count} out of {len(anomalies)}"
    )

    st.dataframe(
        flagged,
        use_container_width=True,
        hide_index=True,
    )

st.divider()

st.subheader("Customer analytics")

segments, payments = customer_segments(filtered)

ca, cb = st.columns(2)

with ca:
    st.dataframe(
        segments,
        use_container_width=True,
        hide_index=True,
    )

with cb:
    st.plotly_chart(
        px.pie(
            payments,
            names="Payment",
            values="Transactions",
            title="Payment mix",
        ),
        use_container_width=True,
    )

st.download_button(
    "Download cleaned dataset",
    filtered.to_csv(index=False).encode("utf-8"),
    "cleaned_supermarket_sales.csv",
    "text/csv",
)

st.caption(
    "Educational project dataset generated locally for demonstration. "
    "Replace the CSV with your approved internship dataset when available."
)
