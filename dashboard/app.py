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

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Global Backgrounds */

    /* Tab text color */
    .stTabs [data-baseweb="tab-list"] button {
        color: #f8fafc !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #3b82f6 !important;
        font-weight: bold;
    }

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }


    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
        color: #f8fafc;
    }

    /* Hero Banner */
    .hero-container {
        background-color: #1e293b;
        padding: 3rem 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
        border-top: 4px solid #3b82f6;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #334155;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .kpi-label {
        font-size: 0.875rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .kpi-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    .indicator-green { background-color: #22c55e; }
    .indicator-yellow { background-color: #eab308; }
    .indicator-red { background-color: #ef4444; }

    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-left: 1rem;
        border-left: 4px solid #3b82f6;
        color: #ffffff;
    }

    /* Pipeline Flow */
    .pipeline-flow {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1e293b;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .flow-stage {
        text-align: center;
        padding: 1rem;
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        flex: 1;
    }
    .flow-arrow {
        color: #3b82f6;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0 1rem;
    }
    .flow-label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    .flow-value {
        font-size: 1.5rem;
        color: #3b82f6;
        font-weight: bold;
    }

    /* Comparison Card */
    .comparison-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
        border-left: 4px solid #3b82f6;
    }

    /* Summary Box */
    .summary-box {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 2rem;
        border: 1px solid #334155;
    }

    /* Enter Button */
    .enter-btn-container {
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

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

# --- SIDEBAR REDESIGN ---
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 2.5rem; margin: 0;">🏛️</h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<p style="font-weight:bold; color:#94a3b8; font-size:0.875rem; letter-spacing:0.05em; text-transform:uppercase;">FILTERS</p>', unsafe_allow_html=True)

min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

show_ratio = st.sidebar.toggle("Show Ratio Metrics", value=True)
alert_threshold = st.sidebar.slider("Backlog Alert Threshold", min_value=0, max_value=5000, value=500, step=50)

st.sidebar.markdown("---")
st.sidebar.markdown('<p style="font-weight:bold; color:#94a3b8; font-size:0.875rem; letter-spacing:0.05em; text-transform:uppercase;">ABOUT</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p style="font-size:0.8rem; color:#94a3b8;">Data source: HHS / U.S. Department of Health and Human Services</p>', unsafe_allow_html=True)
st.sidebar.markdown(f'<p style="font-size:0.8rem; color:#94a3b8;">Dataset Range: {min_date.strftime("%b %d, %Y")} - {max_date.strftime("%b %d, %Y")}</p>', unsafe_allow_html=True)


# Filter data
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
mask = (df['date'] >= start_date) & (df['date'] <= end_date)
filtered_df = df.loc[mask]

trend_mask = []
for idx, row in df_trends.iterrows():
    if (row['year'] > start_date.year or (row['year'] == start_date.year and row['month'] >= start_date.month)) and \
       (row['year'] < end_date.year or (row['year'] == end_date.year and row['month'] <= end_date.month)):
        trend_mask.append(True)
    else:
        trend_mask.append(False)
filtered_trends = df_trends[trend_mask].copy()


# --- LANDING PAGE ---
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:
    avg_te = filtered_df['transfer_efficiency_ratio'].mean() * 100
    avg_de = filtered_df['discharge_effectiveness_index'].mean() * 100
    avg_pt = filtered_df['pipeline_throughput_rate'].mean() * 100
    total_anomalies = filtered_df['is_anomaly'].sum()

    te_color = "indicator-green" if avg_te > 80 else ("indicator-yellow" if avg_te > 50 else "indicator-red")
    de_color = "indicator-green" if avg_de > 20 else ("indicator-yellow" if avg_de > 10 else "indicator-red")
    pt_color = "indicator-green" if avg_pt > 5 else ("indicator-yellow" if avg_pt > 2 else "indicator-red")
    an_color = "indicator-green" if total_anomalies < 5 else ("indicator-yellow" if total_anomalies < 15 else "indicator-red")

    st.markdown(f'''<div class="hero-container"><div class="hero-title">UAC Care Transition & Placement Analytics</div><div class="hero-subtitle">Tracking how efficiently children move from CBP custody → HHS care → Sponsor placement</div><div style="display: flex; gap: 1rem; justify-content: space-between; margin-top: 2rem;"><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_te:.1f}%</div><div class="kpi-label">Transfer Efficiency</div><div class="kpi-indicator {te_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_de:.1f}%</div><div class="kpi-label">Discharge Effectiveness</div><div class="kpi-indicator {de_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{avg_pt:.1f}%</div><div class="kpi-label">Pipeline Throughput</div><div class="kpi-indicator {pt_color}"></div></div><div class="kpi-card" style="flex: 1;"><div class="kpi-value">{int(total_anomalies)}</div><div class="kpi-label">Total Anomaly Days</div><div class="kpi-indicator {an_color}"></div></div></div></div>''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Enter Dashboard →", use_container_width=True, type="primary"):
            st.session_state.show_dashboard = True
            st.rerun()

else:
    # --- DASHBOARD VIEW ---
    if st.button("← Back to Landing Page"):
        st.session_state.show_dashboard = False
        st.rerun()

    # --- Global Alert Banner ---
    most_recent_day = df.loc[df['date'].idxmax()]
    if most_recent_day['backlog_accumulation_rate'] > alert_threshold:
        st.error("🚨 **ALERT:** Current backlog accumulation exceeds threshold. Immediate review recommended.")

    # --- TAB STRUCTURE ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Pipeline Overview",
        "⚡ Efficiency Metrics",
        "🚨 Bottleneck Alerts",
        "📈 Outcome Trends"
    ])

    # --- TAB 1: PIPELINE OVERVIEW ---
    with tab1:
        st.markdown('<div class="section-header">Care Pipeline Load Over Time</div>', unsafe_allow_html=True)

        # Dual-axis Plotly line chart
        fig_load = go.Figure()
        fig_load.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['cbp_custody'], name="CBP Custody", line=dict(color='#3b82f6')))
        fig_load.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['hhs_care'], name="HHS Care", line=dict(color='#22c55e'), yaxis='y2'))
        fig_load.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis=dict(title="CBP Custody", title_font=dict(color='#3b82f6'), tickfont=dict(color='#3b82f6')),
            yaxis2=dict(title="HHS Care", title_font=dict(color='#22c55e'), tickfont=dict(color='#22c55e'), overlaying='y', side='right'),
            legend=dict(x=0, y=1.1, orientation='h'),
            hovermode="x unified"
        )
        st.plotly_chart(fig_load, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-header">Inflow vs Outflow</div>', unsafe_allow_html=True)
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['apprehended'], fill='tozeroy', name='Apprehended (In)', line=dict(color='#3b82f6')))
            fig_area.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharged'], fill='tozeroy', name='Discharged (Out)', line=dict(color='#f97316')))
            fig_area.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Date",
                yaxis_title="Count",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_area, use_container_width=True)

        with col2:
            st.markdown('<div class="section-header">Pipeline Flow (Averages)</div>', unsafe_allow_html=True)
            avg_cbp = int(filtered_df['cbp_custody'].mean())
            avg_hhs = int(filtered_df['hhs_care'].mean())
            avg_dis = int(filtered_df['discharged'].mean())

            st.markdown(f"""
            <div class="pipeline-flow">
                <div class="flow-stage">
                    <div class="flow-label">CBP Custody</div>
                    <div class="flow-value">{avg_cbp:,}</div>
                </div>
                <div class="flow-arrow">→</div>
                <div class="flow-stage">
                    <div class="flow-label">HHS Care</div>
                    <div class="flow-value">{avg_hhs:,}</div>
                </div>
                <div class="flow-arrow">→</div>
                <div class="flow-stage">
                    <div class="flow-label">Sponsor Placement</div>
                    <div class="flow-value">{avg_dis:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 2: EFFICIENCY METRICS ---
    with tab2:
        st.markdown('<div class="section-header">Efficiency Indicators</div>', unsafe_allow_html=True)
        if show_ratio:
            # TE Ratio
            fig_te = go.Figure()
            fig_te.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['transfer_efficiency_ratio'], name='Daily Transfer Efficiency', line=dict(color='#3b82f6', width=1), opacity=0.5))
            fig_te.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['rolling_30d_transfer_efficiency'], name='30D Rolling Avg', line=dict(color='#eab308', width=3)))
            fig_te.update_layout(
                title="Transfer Efficiency Ratio (CBP → HHS)",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                height=350
            )
            st.plotly_chart(fig_te, use_container_width=True)

            # DE Index
            fig_de = go.Figure()
            fig_de.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharge_effectiveness_index'], name='Daily Discharge Effectiveness', line=dict(color='#22c55e', width=1), opacity=0.5))
            fig_de.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['rolling_30d_discharge_effectiveness'], name='30D Rolling Avg', line=dict(color='#eab308', width=3)))
            fig_de.add_hline(y=0.3, line_dash="dash", line_color="#ef4444", annotation_text="Critical Threshold", annotation_position="bottom right")
            fig_de.update_layout(
                title="Discharge Effectiveness Index",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified",
                height=350
            )
            st.plotly_chart(fig_de, use_container_width=True)
        else:
            # Raw counts
            fig_raw = go.Figure()
            fig_raw.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['transferred'], name='Transferred to HHS', line=dict(color='#3b82f6')))
            fig_raw.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['discharged'], name='Discharged to Sponsor', line=dict(color='#f97316')))
            fig_raw.update_layout(
                title="Raw Counts: Transferred vs Discharged",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode="x unified"
            )
            st.plotly_chart(fig_raw, use_container_width=True)

        st.markdown('<div class="section-header">Performance Comparison</div>', unsafe_allow_html=True)
        weekday_de = filtered_df.groupby('is_weekend')['discharge_effectiveness_index'].mean().reset_index()
        weekday_val = weekday_de[weekday_de['is_weekend'] == False]['discharge_effectiveness_index'].values[0] * 100
        weekend_val = weekday_de[weekday_de['is_weekend'] == True]['discharge_effectiveness_index'].values[0] * 100

        diff = weekend_val - weekday_val
        badge_color = "#22c55e" if diff >= 0 else "#ef4444"
        badge_text = f"+{diff:.1f}% Better" if diff >= 0 else f"{diff:.1f}% Worse"

        st.markdown(f"""
        <div class="comparison-card">
            <h3 style="margin-top:0; color:#e2e8f0;">Weekday vs Weekend Discharge Effectiveness</h3>
            <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: #3b82f6;">{weekday_val:.1f}%</div>
                    <div style="color: #94a3b8;">Weekday Avg</div>
                </div>
                <div style="font-size: 2rem; color: #64748b;">VS</div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem; font-weight: bold; color: #a855f7;">{weekend_val:.1f}%</div>
                    <div style="color: #94a3b8;">Weekend Avg</div>
                </div>
                <div>
                    <div style="background-color: {badge_color}; color: white; padding: 0.5rem 1rem; border-radius: 9999px; font-weight: bold;">
                        {badge_text}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: BOTTLENECK ALERTS ---
    with tab3:
        st.markdown('<div class="section-header">Backlog Accumulation Rate</div>', unsafe_allow_html=True)

        monthly_backlog = filtered_df.groupby(['year', 'month', 'month_name'])['backlog_accumulation_rate'].mean().reset_index()
        monthly_backlog = monthly_backlog.sort_values(['year', 'month'])
        monthly_backlog['year_month'] = monthly_backlog['year'].astype(str) + "-" + monthly_backlog['month_name']
        monthly_backlog['color'] = np.where(monthly_backlog['backlog_accumulation_rate'] > 0, '#ef4444', '#22c55e')

        fig_mb = go.Figure(data=[
            go.Bar(
                x=monthly_backlog['year_month'],
                y=monthly_backlog['backlog_accumulation_rate'],
                marker_color=monthly_backlog['color']
            )
        ])
        fig_mb.update_layout(
            title="Monthly Average Backlog Accumulation Rate",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Month",
            yaxis_title="Avg Backlog Accumulation",
            hovermode="x"
        )
        st.plotly_chart(fig_mb, use_container_width=True)

        st.markdown('<div class="section-header">Anomaly Timeline</div>', unsafe_allow_html=True)
        fig_ba = go.Figure()
        fig_ba.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['backlog_accumulation_rate'], name='Backlog Accumulation', line=dict(color='#3b82f6')))
        anomalies = filtered_df[filtered_df['is_anomaly']]
        fig_ba.add_trace(go.Scatter(x=anomalies['date'], y=anomalies['backlog_accumulation_rate'], mode='markers', name='Anomalies', marker=dict(color='#ef4444', size=10, symbol='circle', line=dict(width=2, color='white'))))
        fig_ba.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig_ba, use_container_width=True)

        st.markdown('<div class="section-header">Top Worst Bottleneck Periods</div>', unsafe_allow_html=True)
        if not df_bottlenecks.empty and len(df_bottlenecks.columns) > 0:
            mask_bn = (pd.to_datetime(df_bottlenecks['end_date']) >= start_date) & (pd.to_datetime(df_bottlenecks['start_date']) <= end_date)
            filtered_bn = df_bottlenecks[mask_bn].copy()
            if not filtered_bn.empty:
                # Add severity badge column
                filtered_bn['Severity'] = filtered_bn['avg_backlog_accumulation_rate'].apply(
                    lambda x: '🔴 Critical' if x > 1500 else ('🟠 High' if x > 1000 else '🟡 Moderate')
                )
                display_cols = ['start_date', 'end_date', 'duration_days', 'avg_backlog_accumulation_rate', 'Severity']

                # Format for display
                disp_df = filtered_bn[display_cols].copy()
                disp_df.columns = ['Start Date', 'End Date', 'Duration (days)', 'Avg Backlog', 'Severity']
                disp_df['Avg Backlog'] = disp_df['Avg Backlog'].round(1)

                st.dataframe(
                    disp_df.head(10).style.applymap(lambda x: f"color: {'#ef4444' if 'Critical' in x else ('#f97316' if 'High' in x else '#eab308')}", subset=['Severity']),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No bottleneck periods found in this date range.")
        else:
            st.info("No bottleneck periods found.")

    # --- TAB 4: OUTCOME TRENDS ---
    with tab4:
        st.markdown('<div class="section-header">Outcome Stability</div>', unsafe_allow_html=True)
        fig_stb = go.Figure()
        fig_stb.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['outcome_stability_score'], name='Stability Score', line=dict(color='#a855f7', width=2), fill='tozeroy', fillcolor='rgba(168, 85, 247, 0.2)'))
        fig_stb.update_layout(
            title="Outcome Stability Score (7-Day Rolling Std)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig_stb, use_container_width=True)

        st.markdown('<div class="section-header">Month-over-Month KPI Trends</div>', unsafe_allow_html=True)

        if not filtered_trends.empty:
            def color_mom(val):
                if pd.isna(val): return ''
                if isinstance(val, (int, float)):
                    color = '#22c55e' if val > 0 else '#ef4444' if val < 0 else '#94a3b8'
                    return f'color: {color}; font-weight: bold;'
                return ''

            def format_arrows(val):
                if pd.isna(val): return val
                if isinstance(val, (int, float)):
                    return f"↑ {val:.2f}%" if val > 0 else (f"↓ {abs(val):.2f}%" if val < 0 else f"{val:.2f}%")
                return val

            mom_cols = [c for c in filtered_trends.columns if 'mom_change' in c]

            disp_trends = filtered_trends[['year', 'month_name'] + mom_cols].copy()
            disp_trends.columns = ['Year', 'Month'] + [c.replace('_mom_change', '').replace('_', ' ').title() for c in mom_cols]

            # Apply arrow formatting
            for col in disp_trends.columns[2:]:
                disp_trends[col] = disp_trends[col].apply(format_arrows)


            def style_arrows(val):
                if isinstance(val, str):
                    if val.startswith('↑'):
                        return 'color: #22c55e; font-weight: bold;'
                    elif val.startswith('↓'):
                        return 'color: #ef4444; font-weight: bold;'
                return ''

            st.dataframe(disp_trends.style.map(style_arrows), use_container_width=True, hide_index=True)


            # Bottom Summary Box
            if 'discharge_effectiveness_index_mom_change' in filtered_trends.columns:
                best_idx = filtered_trends['discharge_effectiveness_index_mom_change'].idxmax()
                worst_idx = filtered_trends['discharge_effectiveness_index_mom_change'].idxmin()

                best_month = f"{filtered_trends.loc[best_idx, 'month_name']} {filtered_trends.loc[best_idx, 'year']}"
                worst_month = f"{filtered_trends.loc[worst_idx, 'month_name']} {filtered_trends.loc[worst_idx, 'year']}"
                best_val = filtered_trends.loc[best_idx, 'discharge_effectiveness_index_mom_change']
                worst_val = filtered_trends.loc[worst_idx, 'discharge_effectiveness_index_mom_change']

                st.markdown(f"""
                <div class="summary-box">
                    <h3 style="margin-top:0; color:#e2e8f0; text-align:center;">Discharge Effectiveness MoM Performance</h3>
                    <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
                        <div style="text-align: center;">
                            <div style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase;">Best Month</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff;">{best_month}</div>
                            <div style="color: #22c55e; font-weight: bold; font-size: 1.2rem;">↑ {best_val:.1f}%</div>
                        </div>
                        <div style="border-left: 1px solid #334155;"></div>
                        <div style="text-align: center;">
                            <div style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase;">Worst Month</div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: #ffffff;">{worst_month}</div>
                            <div style="color: #ef4444; font-weight: bold; font-size: 1.2rem;">↓ {abs(worst_val):.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
