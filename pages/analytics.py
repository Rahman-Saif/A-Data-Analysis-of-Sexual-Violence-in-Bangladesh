import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# PAGE CONFIG
# ============================================


st.title("Analytics Dashboard")

# ============================================
# LOAD DATA
# ============================================

df = pd.read_csv(
    "sexual violence.csv",
    encoding='latin1'
)
# ============================================
# KPIs
# ============================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Incidents",
    len(df)
)

col2.metric(
    "Total Districts",
    df['incident_district'].nunique()
)

col3.metric(
    "Most Common Type",
    df['sexual_violence_type'].mode()[0]
)

# ============================================
# DIVISION GRAPH
# ============================================

st.subheader("Division-wise Incidents")

division_counts = (
    df['incident_divison']
    .value_counts()
    .reset_index()
)

division_counts.columns = [
    'division',
    'count'
]

fig1 = px.bar(
    division_counts,
    x='division',
    y='count',
    color='count',
    title='Division-wise Incident Count'
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ============================================
# DISTRICT GRAPH
# ============================================

st.subheader("Top Affected Districts")

district_counts = (
    df['incident_district']
    .value_counts()
    .head(10)
    .reset_index()
)

district_counts.columns = [
    'district',
    'count'
]

fig2 = px.bar(
    district_counts,
    x='district',
    y='count',
    color='count',
    title='Top 10 Districts'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ============================================
# SEASON ANALYSIS
# ============================================

st.subheader("Season-wise Incidents")

season_counts = (
    df['season']
    .value_counts()
    .reset_index()
)

season_counts.columns = [
    'season',
    'count'
]

fig3 = px.pie(
    season_counts,
    names='season',
    values='count',
    title='Season Distribution'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ============================================
# PART OF DAY ANALYSIS
# ============================================

st.subheader("Part of Day Analysis")

time_counts = (
    df['part_of_the_day']
    .value_counts()
    .reset_index()
)

time_counts.columns = [
    'time',
    'count'
]

fig4 = px.histogram(
    time_counts,
    x='time',
    y='count',
    color='count',
    title='Incident Timing'
)

st.plotly_chart(
    fig4,
    use_container_width=True
)