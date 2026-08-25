from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from src.metrics import calculate_kpis, data_quality_report, prepare_data, route_summary

st.set_page_config(page_title="Airline Operations KPI Dashboard", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "flight_operations.csv"

@st.cache_data
def load_data() -> pd.DataFrame:
    return prepare_data(pd.read_csv(DATA_PATH))


df = load_data()

st.title("Airline Operations KPI Dashboard")
st.caption("Synthetic operational data for a portfolio demonstration — no Lufthansa internal data is used.")

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Date range",
        value=(df["date"].min().date(), df["date"].max().date()),
        min_value=df["date"].min().date(),
        max_value=df["date"].max().date(),
    )
    origins = st.multiselect("Origin", sorted(df["origin"].unique()))
    routes = st.multiselect("Route", sorted(df["route"].unique()))

filtered = df.copy()
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["date"] >= start) & (filtered["date"] <= end)]
if origins:
    filtered = filtered[filtered["origin"].isin(origins)]
if routes:
    filtered = filtered[filtered["route"].isin(routes)]

kpis = calculate_kpis(filtered)
cols = st.columns(5)
cols[0].metric("Flights", f"{kpis['flights']:,}")
cols[1].metric("On-time performance", f"{kpis['on_time_performance']:.1%}")
cols[2].metric("Avg. arrival delay", f"{kpis['avg_arrival_delay']:.1f} min")
cols[3].metric("Cancellation rate", f"{kpis['cancellation_rate']:.1%}")
cols[4].metric("Avg. load factor", f"{kpis['avg_load_factor']:.1%}")

st.subheader("Operational trends")
daily = (
    filtered.groupby("date", as_index=False)
    .agg(on_time_performance=("on_time", "mean"), avg_arrival_delay=("arrival_delay_min", "mean"))
)
st.plotly_chart(
    px.line(daily, x="date", y="on_time_performance", markers=True, labels={"on_time_performance":"OTP"}),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    st.subheader("Delay causes")
    cause_df = (
        filtered.loc[filtered["delay_cause"] != "No delay"]
        .groupby("delay_cause", as_index=False)
        .size()
        .sort_values("size", ascending=False)
    )
    st.plotly_chart(px.bar(cause_df, x="delay_cause", y="size", labels={"size":"Flights"}), use_container_width=True)

with right:
    st.subheader("Route performance")
    routes_df = route_summary(filtered).head(12)
    display = routes_df.copy()
    display["on_time_performance"] = display["on_time_performance"].map(lambda x: f"{x:.1%}")
    display["avg_arrival_delay"] = display["avg_arrival_delay"].map(lambda x: f"{x:.1f}")
    display["avg_load_factor"] = display["avg_load_factor"].map(lambda x: f"{x:.1%}")
    st.dataframe(display, use_container_width=True, hide_index=True)

with st.expander("Data quality check"):
    report = data_quality_report(filtered)
    st.json(report)
    st.write("The synthetic data intentionally stores delay fields as blank for cancelled flights; this is expected operationally and is handled in KPI calculations.")

with st.expander("Why this project exists"):
    st.markdown(
        """
        This compact portfolio project demonstrates a typical IT/data-platform workflow:
        1. define operational KPIs,
        2. validate and transform source data,
        3. expose filters and repeatable reporting,
        4. compare performance across time and routes,
        5. keep data-quality checks visible alongside the dashboard.
        """
    )
