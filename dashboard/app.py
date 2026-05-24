from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


st.set_page_config(page_title="UAC Analytics Dashboard", layout="wide")
st.title("UAC Analytics Dashboard")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])


data_path = Path("data/uac_with_kpis.csv")
if not data_path.exists():
    st.error("Missing data/uac_with_kpis.csv. Generate it before launching the dashboard.")
    st.stop()

df = load_data(data_path).sort_values("date").reset_index(drop=True)
if df.empty:
    st.error("Dataset is empty.")
    st.stop()

min_date = df["date"].min().date()
max_date = df["date"].max().date()

st.sidebar.header("Filters")
date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)
show_ratio_metrics = st.sidebar.toggle("Show ratio metrics", value=True)
max_backlog = int(max(1000, df["backlog_accumulation_rate"].max() * 2))
backlog_threshold = st.sidebar.slider(
    "Backlog alert threshold", min_value=0, max_value=max_backlog, value=500, step=10
)

mask = (df["date"].dt.date >= date_range[0]) & (df["date"].dt.date <= date_range[1])
filtered = df.loc[mask].copy()
if filtered.empty:
    st.warning("No data in selected date range.")
    st.stop()

filtered = filtered.sort_values("date").reset_index(drop=True)
if filtered["is_weekend"].dtype == object:
    filtered["is_weekend"] = filtered["is_weekend"].map(
        {"True": True, "False": False}
    )


def compute_anomalies(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()
    metrics = ["transfer_efficiency_ratio", "discharge_effectiveness_index"]
    for col in metrics:
        roll_mean = data[col].rolling(window=30, min_periods=30).mean()
        roll_std = data[col].rolling(window=30, min_periods=30).std()
        data[f"{col}_anomaly"] = data[col] < (roll_mean - 2 * roll_std)
    data["is_anomaly"] = data[[f"{c}_anomaly" for c in metrics]].any(axis=1)
    return data


def backlog_periods(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return pd.DataFrame(
            columns=["start_date", "end_date", "days", "total_backlog", "avg_backlog"]
        )
    positive = data["backlog_accumulation_rate"] > 0
    date_gap = data["date"].diff().dt.days.fillna(1)
    group_id = ((positive != positive.shift()) | (date_gap > 1)).cumsum()
    periods = (
        data[positive]
        .groupby(group_id)
        .agg(
            start_date=("date", "min"),
            end_date=("date", "max"),
            days=("date", "count"),
            total_backlog=("backlog_accumulation_rate", "sum"),
            avg_backlog=("backlog_accumulation_rate", "mean"),
        )
        .reset_index(drop=True)
    )
    return periods[periods["days"] >= 7]


analyzed = compute_anomalies(filtered)
anomaly_days = analyzed[analyzed["is_anomaly"]]
current_backlog = filtered.iloc[-1]["backlog_accumulation_rate"]
if current_backlog > backlog_threshold:
    st.error(
        f"Current backlog change is {current_backlog:.0f}, above the {backlog_threshold} threshold."
    )

tabs = st.tabs(
    [
        "Care Pipeline Overview",
        "Transfer & Discharge Efficiency",
        "Bottleneck Detection",
        "Outcome Trend Analysis",
    ]
)

with tabs[0]:
    st.subheader("Care Pipeline Overview")

    if show_ratio_metrics:
        avg_transfer_eff = filtered["transfer_efficiency_ratio"].mean()
        avg_discharge_eff = filtered["discharge_effectiveness_index"].mean()
        avg_pipeline = filtered["pipeline_throughput_rate"].mean()
        metric_labels = [
            ("Avg Transfer Efficiency", f"{avg_transfer_eff:.3f}"),
            ("Avg Discharge Effectiveness", f"{avg_discharge_eff:.3f}"),
            ("Avg Pipeline Throughput", f"{avg_pipeline:.3f}"),
            ("Total Anomaly Days", f"{len(anomaly_days):,}"),
        ]
    else:
        metric_labels = [
            ("Avg Apprehended", f"{filtered['apprehended'].mean():.1f}"),
            ("Avg CBP Custody", f"{filtered['cbp_custody'].mean():.1f}"),
            ("Avg HHS Care", f"{filtered['hhs_care'].mean():.1f}"),
            ("Total Anomaly Days", f"{len(anomaly_days):,}"),
        ]

    cols = st.columns(4)
    for col, (label, value) in zip(cols, metric_labels):
        col.metric(label, value)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["cbp_custody"],
            name="CBP custody",
            line=dict(color="#1f77b4"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["hhs_care"],
            name="HHS care",
            line=dict(color="#ff7f0e"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Care Pipeline Load Over Time",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    fig.update_yaxes(title_text="CBP custody", secondary_y=False)
    fig.update_yaxes(title_text="HHS care", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

    area_data = filtered.melt(
        id_vars=["date"],
        value_vars=["apprehended", "discharged"],
        var_name="flow",
        value_name="count",
    )
    fig_area = px.area(
        area_data,
        x="date",
        y="count",
        color="flow",
        title="Inflow vs Outflow",
        color_discrete_map={"apprehended": "#8dd3c7", "discharged": "#fb8072"},
    )
    fig_area.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    st.plotly_chart(fig_area, use_container_width=True)

with tabs[1]:
    st.subheader("Transfer & Discharge Efficiency")

    if show_ratio_metrics:
        rolling_transfer = (
            filtered["transfer_efficiency_ratio"].rolling(window=30, min_periods=7).mean()
        )
        fig_transfer = go.Figure()
        fig_transfer.add_trace(
            go.Scatter(
                x=filtered["date"],
                y=filtered["transfer_efficiency_ratio"],
                name="Daily ratio",
                line=dict(color="#9ecae1"),
            )
        )
        fig_transfer.add_trace(
            go.Scatter(
                x=filtered["date"],
                y=rolling_transfer,
                name="30-day rolling avg",
                line=dict(color="#08519c", width=3),
            )
        )
        fig_transfer.add_hline(
            y=0.3, line_dash="dash", line_color="red", annotation_text="Threshold 0.3"
        )
        fig_transfer.update_layout(
            title="Transfer Efficiency Ratio", margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_transfer, use_container_width=True)

        fig_discharge = px.line(
            filtered,
            x="date",
            y="discharge_effectiveness_index",
            title="Discharge Effectiveness Index",
            color_discrete_sequence=["#2ca02c"],
        )
        fig_discharge.add_hline(
            y=0.3, line_dash="dash", line_color="red", annotation_text="Threshold 0.3"
        )
        fig_discharge.update_layout(margin=dict(l=40, r=40, t=60, b=40))
        st.plotly_chart(fig_discharge, use_container_width=True)
    else:
        fig_transfer = px.line(
            filtered,
            x="date",
            y="transferred",
            title="Transfers Over Time",
            color_discrete_sequence=["#1f77b4"],
        )
        fig_transfer.update_layout(margin=dict(l=40, r=40, t=60, b=40))
        st.plotly_chart(fig_transfer, use_container_width=True)

        fig_discharge = px.line(
            filtered,
            x="date",
            y="discharged",
            title="Discharges Over Time",
            color_discrete_sequence=["#2ca02c"],
        )
        fig_discharge.update_layout(margin=dict(l=40, r=40, t=60, b=40))
        st.plotly_chart(fig_discharge, use_container_width=True)

    weekend_summary = (
        filtered.groupby("is_weekend")["discharge_effectiveness_index"]
        .mean()
        .reset_index()
    )
    weekend_summary["day_type"] = weekend_summary["is_weekend"].map(
        {True: "Weekend", False: "Weekday"}
    )
    fig_weekend = px.bar(
        weekend_summary,
        x="day_type",
        y="discharge_effectiveness_index",
        title="Weekend vs Weekday Discharge Performance",
        color="day_type",
        color_discrete_map={"Weekend": "#ff7f0e", "Weekday": "#1f77b4"},
    )
    fig_weekend.update_layout(showlegend=False, margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig_weekend, use_container_width=True)

with tabs[2]:
    st.subheader("Bottleneck Detection")

    monthly_backlog = (
        filtered.set_index("date")["backlog_accumulation_rate"].resample("ME").mean()
    )
    fig_backlog = px.bar(
        x=monthly_backlog.index.to_period("M").astype(str),
        y=monthly_backlog.values,
        labels={"x": "Month", "y": "Avg backlog accumulation"},
        title="Monthly Backlog Accumulation",
        color_discrete_sequence=["#9467bd"],
    )
    fig_backlog.update_layout(margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig_backlog, use_container_width=True)

    fig_anomaly = go.Figure()
    fig_anomaly.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["backlog_accumulation_rate"],
            name="Backlog accumulation",
            line=dict(color="#636363"),
        )
    )
    if not anomaly_days.empty:
        fig_anomaly.add_trace(
            go.Scatter(
                x=anomaly_days["date"],
                y=anomaly_days["backlog_accumulation_rate"],
                mode="markers",
                name="Anomaly days",
                marker=dict(color="red", size=7),
            )
        )
    fig_anomaly.update_layout(
        title="Anomaly Timeline",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)

    worst_periods = (
        backlog_periods(filtered)
        .sort_values(["total_backlog", "days"], ascending=[False, False])
        .head(10)
    )
    if worst_periods.empty:
        st.info("No sustained backlog periods found in selected range.")
    else:
        worst_periods = worst_periods.copy()
        worst_periods["start_date"] = worst_periods["start_date"].dt.date
        worst_periods["end_date"] = worst_periods["end_date"].dt.date
        st.dataframe(worst_periods, use_container_width=True)

with tabs[3]:
    st.subheader("Outcome Trend Analysis")

    kpi_cols = [
        "transfer_efficiency_ratio",
        "discharge_effectiveness_index",
        "pipeline_throughput_rate",
        "backlog_accumulation_rate",
        "outcome_stability_score",
    ]
    monthly_means = filtered.set_index("date")[kpi_cols].resample("ME").mean()
    monthly_pct = monthly_means.pct_change() * 100
    monthly_table = pd.concat(
        [monthly_means.add_suffix("_mean"), monthly_pct.add_suffix("_mom_pct")], axis=1
    )
    monthly_table.insert(
        0, "month", monthly_means.index.to_period("M").astype(str)
    )

    def color_mom(val: float) -> str:
        if pd.isna(val):
            return ""
        if val > 0:
            return "background-color: #e6f4ea; color: #0f5132"
        if val < 0:
            return "background-color: #f8d7da; color: #842029"
        return ""

    mom_cols = [c for c in monthly_table.columns if c.endswith("_mom_pct")]
    styled = monthly_table.style.format(precision=2).applymap(
        color_mom, subset=mom_cols
    )
    st.dataframe(styled, use_container_width=True)

    rolling_outcome = (
        filtered["outcome_stability_score"].rolling(window=30, min_periods=7).mean()
    )
    fig_outcome = go.Figure()
    fig_outcome.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["outcome_stability_score"],
            name="Daily score",
            line=dict(color="#17becf"),
        )
    )
    fig_outcome.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=rolling_outcome,
            name="30-day rolling avg",
            line=dict(color="#0d7f8c", width=3),
        )
    )
    fig_outcome.update_layout(
        title="Outcome Stability Score (Rolling)",
        margin=dict(l=40, r=40, t=60, b=40),
    )
    st.plotly_chart(fig_outcome, use_container_width=True)
