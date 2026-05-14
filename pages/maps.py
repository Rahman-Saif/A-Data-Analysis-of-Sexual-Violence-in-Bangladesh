# pages/maps.py

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# =====================================================
# TITLE
# =====================================================

st.title("Bangladesh Geo-Spatial Crime Map")

# =====================================================
# LOAD DATASET
# =====================================================

df = pd.read_csv("sexual violence.csv", encoding="latin1")
df.columns = df.columns.str.strip()

# =====================================================
# CLEAN INCIDENT UPAZILA
# =====================================================

df['incident_upazila_clean'] = (
    df['incident_upazila']
    .astype(str)
    .str.lower()
    .str.strip()
)

# =====================================================
# AGGREGATION
# =====================================================

upazila_counts = (
    df['incident_upazila_clean']
    .value_counts()
    .reset_index()
)

upazila_counts.columns = ['incident_name', 'incident_count']

st.subheader("Top Incident Locations")
st.dataframe(upazila_counts.head(10))

# =====================================================
# LOAD GEOJSON
# =====================================================

geojson_path = "shapfiles/bgd_admin2.geojson"

try:

    gdf = gpd.read_file(geojson_path)

    st.subheader("GeoJSON Columns")
    st.write(gdf.columns.tolist())

    # =================================================
    # FIX GEO COLUMN
    # =================================================

    if 'adm2_name' not in gdf.columns:
        st.error("adm2_name column not found in GeoJSON")
        st.stop()

    gdf['geo_name'] = (
        gdf['adm2_name']
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # =================================================
    # CLEAN INCIDENT DATA
    # =================================================

    upazila_counts['incident_name'] = (
        upazila_counts['incident_name']
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # manual fix
    name_fix = {
        'chattogram sadar': 'chattogram',
        'gazipur sadar': 'gazipur',
        'sirajganj sadar': 'sirajganj',
        'brahmanbaria sadar': 'brahmanbaria',
        'manikganj sadar': 'manikganj'
    }

    upazila_counts['incident_name'] = (
        upazila_counts['incident_name'].replace(name_fix)
    )

    # =================================================
    # MERGE
    # =================================================

    merged = gdf.merge(
        upazila_counts,
        left_on='geo_name',
        right_on='incident_name',
        how='left'
    )

    merged['incident_count'] = merged['incident_count'].fillna(0)

    # =================================================
    # 🔥 CRITICAL FIX: REMOVE TIMESTAMP ISSUE
    # =================================================

    for col in merged.columns:
        if pd.api.types.is_datetime64_any_dtype(merged[col]):
            merged[col] = merged[col].astype(str)

    # extra safety: convert object columns with datetime inside
    for col in merged.columns:
        if merged[col].dtype == 'object':
            try:
                merged[col] = merged[col].astype(str)
            except:
                pass

    # =================================================
    # SHOW DATA
    # =================================================

    st.subheader("Merged Data")
    st.dataframe(merged[['geo_name', 'incident_count']].head())

    # =================================================
    # MAP
    # =================================================

    m = folium.Map(
        location=[23.685, 90.3563],
        zoom_start=7,
        tiles="cartodbpositron"
    )

    folium.Choropleth(
        geo_data=merged.to_json(),
        data=merged,
        columns=['geo_name', 'incident_count'],
        key_on='feature.properties.geo_name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Crime Incidents (ADM2 Level)'
    ).add_to(m)

    folium.GeoJson(
        merged,
        tooltip=folium.GeoJsonTooltip(
            fields=['geo_name', 'incident_count'],
            aliases=['Region:', 'Incidents:']
        )
    ).add_to(m)

    # =================================================
    # RENDER
    # =================================================

    st.subheader("Interactive Map")

    st_folium(m, width=1400, height=700)

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Check GeoJSON structure or file path.")