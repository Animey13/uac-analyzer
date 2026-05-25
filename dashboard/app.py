import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="UAC Care Transition Analytics",
    page_icon="🏛️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('data/uac_with_kpis.csv', parse_dates=['date'])
    df_trends = pd.read_csv('data/monthly_trends.csv')
    try:
        df_bottlenecks = pd.read_csv('data/top_bottleneck_periods.csv')
    except Exception:
        df_bottlenecks = pd.DataFrame()
    return df, df_trends, df_bottlenecks

try:
    df, df_trends, df_bottlenecks = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("UAC Analytics Dashboard")
st.sidebar.markdown("Care Transition Efficiency & Placement Outcome Analytics")

min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

show_ratio = st.sidebar.toggle("Show Ratio Metrics", value=True)
alert_threshold = st.sidebar.slider("Backlog Alert Threshold", min_value=0, max_value=5000, value=500, step=50)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** HHS / U.S. Department of Health and Human Services")

# Filter data
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
mask = (df['date'] >= start_date) & (df['date'] <= end_date)
filtered_df = df.loc[mask]

# Filter df_trends based on selected date range as well
# Create a dummy date to filter trends or just filter by year and month
# Using start and end dates directly if trends contains month numbers
trend_mask = []
for idx, row in df_trends.iterrows():
    # approximate start of month
    row_date = pd.to_datetime(f"{row['year']}-{row['month']:02d}-01")
    # if row_date falls within the range roughly
    # Alternatively we can filter df_trends by building year-month comparable objects
    if (row['year'] > start_date.year or (row['year'] == start_date.year and row['month'] >= start_date.month)) and \
       (row['year'] < end_date.year or (row['year'] == end_date.year and row['month'] <= end_date.month)):
        trend_mask.append(True)
    else:
        trend_mask.append(False)
filtered_trends = df_trends[trend_mask].copy()


# --- Global Alert Banner ---
most_recent_day = df.loc[df['date'].idxmax()]
if most_recent_day['backlog_accumulation_rate'] > alert_threshold:
    st.error("⚠️ ALERT: Current backlog accumulation exceeds threshold. Immediate review recommended.")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Care Pipeline Overview",
    "Transfer & Discharge Efficiency",
    "Bottleneck Detection",
    "Outcome Trend Analysis"
])

# --- TAB 1 ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    avg_te = filtered_df['transfer_efficiency_ratio'].mean() * 100
    avg_de = filtered_df['discharge_effectiveness_index'].mean() * 100
    avg_pt = filtered_df['pipeline_throughput_rate'].mean() * 100
    total_anomalies = filtered_df['is_anomaly'].sum()

    col1.metric("Avg Transfer Efficiency", f"{avg_te:.1f}%")
    col2.metric("Avg Discharge Effectiveness", f"{avg_de:.1f}%")
    col3.metric("Avg Pipeline Throughput", f"{avg_pt:.1f}%")
    col4.metric("Total Anomaly Days", int(total_anomalies))

    # Row 2: Dual-axis Plotly line chart
    fig_load = go.Figure()
    fig_load.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['cbp_custody'], name="CBP Custody", line=dict(color='blue')))
    fig_load.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['hhs_care'], name="HHS Care", line=dict(color='green'), yaxis='y2'))
    fig_load.update_layout(
        title="Care Pipeline Load Over Time",
        xaxis_title="Date",
        yaxis=dict(title="CBP Custody", titlefont=dict(color='blue'), tickfont=dict(color='blue')),
        yaxis2=dict(title="HHS Care", titlefont=dict(color='green'), tickfont=dict(color='green'), overlaying='y', side='right'),
        legend=dict(x=0, y=1.1, orientation='h')
    )
    st.plotly_chart(fig_load, use_container_width=True)

    # Row 3: Area chart
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['apprehended'], fill='tozeroy', name='Apprehended', line=dict(color='blue')))
    fig_area.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharged'], fill='tozeroy', name='Discharged', line=dict(color='orange')))
    fig_area.update_layout(title="Daily Inflow vs Outflow", xaxis_title="Date", yaxis_title="Count")
    st.plotly_chart(fig_area, use_container_width=True)

# --- TAB 2 ---
with tab2:
    if show_ratio:
        # TE Ratio
        fig_te = go.Figure()
        fig_te.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['transfer_efficiency_ratio'], name='Transfer Efficiency', line=dict(color='blue')))
        fig_te.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['rolling_30d_transfer_efficiency'], name='30D Rolling Mean', line=dict(color='red', dash='dash')))
        fig_te.update_layout(title="Transfer Efficiency Ratio (CBP → HHS)")
        st.plotly_chart(fig_te, use_container_width=True)

        # DE Index
        fig_de = go.Figure()
        fig_de.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharge_effectiveness_index'], name='Discharge Effectiveness', line=dict(color='green')))
        fig_de.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['rolling_30d_discharge_effectiveness'], name='30D Rolling Mean', line=dict(color='red', dash='dash')))
        fig_de.add_hline(y=0.3, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
        fig_de.update_layout(title="Discharge Effectiveness Index")
        st.plotly_chart(fig_de, use_container_width=True)
    else:
        # Raw counts
        fig_raw = go.Figure()
        fig_raw.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['transferred'], name='Transferred', line=dict(color='blue')))
        fig_raw.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharged'], name='Discharged', line=dict(color='orange')))
        fig_raw.update_layout(title="Raw Counts: Transferred vs Discharged")
        st.plotly_chart(fig_raw, use_container_width=True)

    # Weekday vs Weekend grouped bar chart
    weekday_de = filtered_df.groupby('is_weekend')['discharge_effectiveness_index'].mean().reset_index()
    weekday_de['Day Type'] = weekday_de['is_weekend'].map({True: 'Weekend', False: 'Weekday'})
    fig_wk = px.bar(weekday_de, x='Day Type', y='discharge_effectiveness_index', title="Average Discharge Effectiveness: Weekday vs Weekend", color='Day Type')
    st.plotly_chart(fig_wk, use_container_width=True)

# --- TAB 3 ---
with tab3:
    # Monthly Backlog bar chart (already naturally filtered if we compute from filtered_df)
    monthly_backlog = filtered_df.groupby(['year', 'month', 'month_name'])['backlog_accumulation_rate'].mean().reset_index()
    monthly_backlog = monthly_backlog.sort_values(['year', 'month'])
    monthly_backlog['year_month'] = monthly_backlog['year'].astype(str) + "-" + monthly_backlog['month_name']
    monthly_backlog['color'] = np.where(monthly_backlog['backlog_accumulation_rate'] > 0, 'red', 'green')

    fig_mb = go.Figure(data=[
        go.Bar(
            x=monthly_backlog['year_month'],
            y=monthly_backlog['backlog_accumulation_rate'],
            marker_color=monthly_backlog['color']
        )
    ])
    fig_mb.update_layout(title="Monthly Average Backlog Accumulation Rate", xaxis_title="Month", yaxis_title="Avg Backlog Accumulation")
    st.plotly_chart(fig_mb, use_container_width=True)

    # Backlog accumulation over time with anomalies
    fig_ba = go.Figure()
    fig_ba.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['backlog_accumulation_rate'], name='Backlog Accumulation', line=dict(color='blue')))
    anomalies = filtered_df[filtered_df['is_anomaly']]
    fig_ba.add_trace(go.Scatter(x=anomalies['date'], y=anomalies['backlog_accumulation_rate'], mode='markers', name='Anomalies', marker=dict(color='red', size=8)))
    fig_ba.update_layout(title="Backlog Accumulation Rate over Time with Anomalies Highlighted")
    st.plotly_chart(fig_ba, use_container_width=True)

    st.subheader("Top 10 Worst Bottleneck Periods")
    if not df_bottlenecks.empty and len(df_bottlenecks.columns) > 0:
        # Filter bottlenecks overlapping with date range
        mask_bn = (pd.to_datetime(df_bottlenecks['end_date']) >= start_date) & (pd.to_datetime(df_bottlenecks['start_date']) <= end_date)
        filtered_bn = df_bottlenecks[mask_bn]
        if not filtered_bn.empty:
            st.dataframe(filtered_bn)
        else:
            st.info("No bottleneck periods found in this date range.")
    else:
        st.info("No bottleneck periods found.")

    st.subheader("Anomaly Summary")
    st.write(f"Total anomalies in selected date range: {len(anomalies)}")
    if not anomalies.empty:
        worst_anomalies = anomalies.sort_values('discharge_effectiveness_index').head(5)
        st.write("Top 5 Worst Anomaly Days (by Discharge Effectiveness):")
        st.dataframe(worst_anomalies[['date', 'transfer_efficiency_ratio', 'discharge_effectiveness_index', 'backlog_accumulation_rate']])

# --- TAB 4 ---
with tab4:
    fig_stb = go.Figure()
    fig_stb.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['outcome_stability_score'], name='Stability Score', line=dict(color='purple')))
    fig_stb.update_layout(title="Outcome Stability Score (7-Day Rolling Std)")
    st.plotly_chart(fig_stb, use_container_width=True)

    st.subheader("Monthly KPI Trends")
    # Styling dataframe
    def color_mom(val):
        if pd.isna(val): return ''
        if isinstance(val, (int, float)):
            color = 'green' if val > 0 else 'red' if val < 0 else 'black'
            return f'color: {color}'
        return ''

    mom_cols = [c for c in filtered_trends.columns if 'mom_change' in c]
    st.dataframe(filtered_trends.style.map(color_mom, subset=mom_cols), use_container_width=True)

    # MoM % change line chart for DE
    if 'discharge_effectiveness_index_mom_change' in filtered_trends.columns:
        filtered_trends['year_month'] = filtered_trends['year'].astype(str) + "-" + filtered_trends['month_name']
        fig_mom = px.line(filtered_trends, x='year_month', y='discharge_effectiveness_index_mom_change', title="Month-over-Month % Change: Discharge Effectiveness", markers=True)
        st.plotly_chart(fig_mom, use_container_width=True)
