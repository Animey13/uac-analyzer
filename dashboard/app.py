import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="UAC Program Analytics Dashboard", layout="wide", page_icon="🏛️")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, '../HHS_Unaccompanied_Alien_Children_Program.csv')
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Handle commas and conversion
    if df['Children in HHS Care'].dtype == 'object':
        df['Children in HHS Care'] = df['Children in HHS Care'].str.replace(',', '').astype(float)

    df = df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)
    return df

df = load_data()

st.title("UAC Program Analytics Dashboard")
st.markdown("This dashboard visualizes data from the HHS Unaccompanied Alien Children Program.")

# Sidebar Filters
st.sidebar.header("Filters")
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
    filtered_df = df.loc[mask]
else:
    filtered_df = df.copy()

# Mock Multi-selects for columns that don't exist
country = st.sidebar.multiselect("Country of Origin", options=[], default=[])
state = st.sidebar.multiselect("US State", options=[], default=[])

st.sidebar.info("Country and State filters are disabled as the dataset does not contain demographic columns.")

# KPIs
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_children = filtered_df['Children apprehended and placed in CBP custody*'].sum()
date_range_str = f"{start_date} to {end_date}" if len(date_range) == 2 else "All Time"

col1.metric("Total Children Apprehended", f"{total_children:,.0f}")
col2.metric("Date Range of Data", date_range_str)
col3.metric("Top Country of Origin", "N/A (No Data)")
col4.metric("Most Common Placement State", "N/A (No Data)")

# Charts
st.subheader("Visualizations")

# 1. Line chart — intake trend over time
st.markdown("#### Intake Trend Over Time")
fig1 = px.line(filtered_df, x='Date', y='Children apprehended and placed in CBP custody*',
               title='Apprehensions Over Time', template='plotly_dark')
st.plotly_chart(fig1, use_container_width=True)

# 2. Bar chart — top 15 countries of origin
st.markdown("#### Top 15 Countries of Origin")
st.info("Chart skipped gracefully: The dataset does not contain country of origin data.")

# 3. Choropleth or bar chart — distribution by US state
st.markdown("#### Geographic Distribution by US State")
st.info("Chart skipped gracefully: The dataset does not contain US state distribution data.")

# 4. Pie or bar chart — age group or gender breakdown
st.markdown("#### Age Group and Gender Breakdown")
st.info("Chart skipped gracefully: The dataset does not contain age or gender data.")

# 5. One additional chart based on what the data supports
st.markdown("#### Children in CBP vs HHS Care Over Time")
fig_add = go.Figure()
fig_add.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Children in CBP custody'],
                             mode='lines', name='CBP Custody'))
fig_add.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Children in HHS Care'],
                             mode='lines', name='HHS Care'))
fig_add.update_layout(title="Custody Populations Over Time", template='plotly_dark',
                      xaxis_title="Date", yaxis_title="Number of Children")
st.plotly_chart(fig_add, use_container_width=True)

# 6. Another additional chart to replace the missing ones
st.markdown("#### Transfers vs Discharges")
fig_add2 = go.Figure()
fig_add2.add_trace(go.Bar(x=filtered_df['Date'], y=filtered_df['Children transferred out of CBP custody'],
                          name='Transferred out of CBP'))
fig_add2.add_trace(go.Bar(x=filtered_df['Date'], y=filtered_df['Children discharged from HHS Care'],
                          name='Discharged from HHS'))
fig_add2.update_layout(title="Daily Transfers and Discharges", barmode='group', template='plotly_dark',
                       xaxis_title="Date", yaxis_title="Number of Children")
st.plotly_chart(fig_add2, use_container_width=True)
