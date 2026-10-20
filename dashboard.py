"""
Interactive Logistics Performance Dashboard
Run from project root: streamlit run dashboard.py
"""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "hypothetical_logistics_dataset.csv"
st.set_page_config(page_title="FastTrack Logistics Dashboard", page_icon="🚚", layout="wide")
st.title("🚚 FastTrack Logistics — Performance Analytics")
st.caption("Week 3 project | Hypothetical dataset for learning and demonstration")

df = pd.read_csv(DATA)
for col in ["weight_kg", "transportation_cost_inr"]:
    df[col] = df[col].fillna(df[col].median())
df["region"] = df["region"].fillna(df["region"].mode()[0])
df["on_time"] = df["actual_delivery_days"] <= df["promised_delivery_days"]
df["delay_days"] = (df["actual_delivery_days"] - df["promised_delivery_days"]).clip(lower=0)

with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    modes = st.multiselect("Transport mode", sorted(df["transport_mode"].unique()), default=sorted(df["transport_mode"].unique()))
    types = st.multiselect("Shipment type", sorted(df["shipment_type"].unique()), default=sorted(df["shipment_type"].unique()))
    st.info("This dashboard uses simulated data, not actual company records.")

filtered = df[df["region"].isin(regions) & df["transport_mode"].isin(modes) & df["shipment_type"].isin(types)]
if filtered.empty:
    st.warning("No shipments match the selected filters.")
    st.stop()

total = len(filtered)
avg_days = filtered["actual_delivery_days"].mean()
avg_cost = filtered["transportation_cost_inr"].mean()
on_time_rate = filtered["on_time"].mean() * 100
late_rate = (filtered["delay_days"] > 0).mean() * 100
c1,c2,c3,c4 = st.columns(4)
c1.metric("Shipments", f"{total:,}")
c2.metric("Avg. delivery time", f"{avg_days:.2f} days")
c3.metric("Avg. transport cost", f"₹{avg_cost:,.0f}")
c4.metric("On-time delivery", f"{on_time_rate:.1f}%")

left,right = st.columns(2)
with left:
    fig = px.histogram(filtered, x="actual_delivery_days", nbins=18, title="Delivery Time Distribution",
                       labels={"actual_delivery_days":"Actual delivery (days)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    cost_mode = filtered.groupby("transport_mode", as_index=False)["transportation_cost_inr"].mean()
    fig = px.bar(cost_mode, x="transport_mode", y="transportation_cost_inr", title="Average Cost by Transport Mode",
                 labels={"transport_mode":"Mode","transportation_cost_inr":"Average cost (INR)"})
    st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    fig = px.box(filtered, x="region", y="actual_delivery_days", color="region",
                 title="Delivery Time by Region", labels={"actual_delivery_days":"Actual delivery (days)"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.scatter(filtered, x="distance_km", y="transportation_cost_inr", color="transport_mode",
                     size="shipment_volume_units", hover_data=["shipment_id","region"],
                     title="Distance vs Cost", labels={"distance_km":"Distance (km)","transportation_cost_inr":"Cost (INR)"})
    st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    rate = filtered.groupby("transport_mode", as_index=False)["on_time"].mean()
    rate["on_time_pct"] = rate["on_time"]*100
    fig = px.bar(rate.sort_values("on_time_pct", ascending=False), x="transport_mode", y="on_time_pct",
                 title="On-Time Delivery Rate by Mode", labels={"on_time_pct":"On-time shipments (%)","transport_mode":"Mode"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    daily = filtered.groupby("shipment_date", as_index=False)["transportation_cost_inr"].sum().sort_values("shipment_date")
    daily["rolling_7_day_cost"] = daily["transportation_cost_inr"].rolling(7, min_periods=1).mean()
    fig = px.line(daily, x="shipment_date", y="rolling_7_day_cost", title="7-Day Rolling Average of Daily Cost",
                  labels={"shipment_date":"Shipment date","rolling_7_day_cost":"Rolling average cost (INR)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Summary by transport mode")
summary = filtered.groupby("transport_mode").agg(
    Shipments=("shipment_id","count"),
    Average_delivery_days=("actual_delivery_days","mean"),
    Average_cost_INR=("transportation_cost_inr","mean"),
    On_time_rate=("on_time","mean"),
).reset_index()
summary["On_time_rate"] = (summary["On_time_rate"]*100).round(1).astype(str) + "%"
st.dataframe(summary.round(2), use_container_width=True)

st.subheader("Filtered shipment data")
st.dataframe(filtered, use_container_width=True)
st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_logistics_shipments.csv", mime="text/csv")
