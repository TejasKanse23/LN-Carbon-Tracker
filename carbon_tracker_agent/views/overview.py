import streamlit as st
import plotly.express as px
import pandas as pd
from utils.insights import get_dashboard_kpis, get_top_hotspots

def show(df, lane_df):
    st.title("📊 Sustainability Dashboard")
    st.markdown("High-level overview of freight carbon emissions.")
    
    kpis = get_dashboard_kpis(df, lane_df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Emissions", f"{kpis['Total Emissions (kg)']} kg CO₂e")
    col2.metric("Total Shipments", kpis['Total Shipments'])
    col3.metric("Avg Emissions / Shipment", f"{kpis['Avg Emissions/Shipment (kg)']} kg")
    
    col4, col5, col6, col7 = st.columns(4)
    col4.metric("Highest Emission Lane", kpis['Highest Emission Lane'])
    col5.metric("Avg CO2 / Ton-KM", f"{kpis['Avg CO2/Ton-KM']}")
    col6.metric("Reduction Opportunity", kpis['Reduction Opportunity'])
    
    # Calculate daily trend
    trend_data = df.groupby('date')['estimated_emissions_kg_co2e'].sum().reset_index()
    if len(trend_data) > 1:
        latest_val = trend_data.iloc[-1]['estimated_emissions_kg_co2e']
        previous_val = trend_data.iloc[-2]['estimated_emissions_kg_co2e']
        delta = latest_val - previous_val
        col7.metric("Emission Trend (Latest)", f"{latest_val:.1f} kg", f"{delta:.1f} kg", delta_color="inverse")
    else:
        col7.metric("Emission Trend", "N/A")
    
    st.markdown("---")
    
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.subheader("Emission Trend Over Time")
        fig1 = px.line(trend_data, x="date", y="estimated_emissions_kg_co2e", markers=True, 
                       labels={"estimated_emissions_kg_co2e": "Emissions (kg CO₂e)", "date": "Date"},
                       color_discrete_sequence=["#10b981"])
        st.plotly_chart(fig1, use_container_width=True)
        
    with row1_c2:
        st.subheader("Top 5 High-Emission Lanes")
        top_lanes = get_top_hotspots(lane_df)
        
        # Define color map for various hotspot tags in the new dataset
        hotspot_colors = {
            "High Emission Lane": "#ef4444",
            "Carbon Intensity Hotspot": "#f97316",
            "High Emission + Low Utilization": "#dc2626",
            "Low Utilization Lane": "#facc15",
            "Normal": "#10b981"
        }
        
        fig2 = px.bar(top_lanes, x="lane", y="total_emissions", color="hotspot_tag",
                      labels={"total_emissions": "Total Emissions (kg CO₂e)", "lane": "Lane"},
                      color_discrete_map=hotspot_colors)
        st.plotly_chart(fig2, use_container_width=True)
        
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.subheader("Emissions by Vehicle Type")
        veh_df = df.groupby("vehicle_type")["estimated_emissions_kg_co2e"].sum().reset_index()
        fig3 = px.pie(veh_df, values="estimated_emissions_kg_co2e", names="vehicle_type", hole=0.4,
                      color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig3, use_container_width=True)
        
    with row2_c2:
        st.subheader("Emissions by Fuel Type")
        fuel_df = df.groupby("fuel_type")["estimated_emissions_kg_co2e"].sum().reset_index()
        fig4 = px.pie(fuel_df, values="estimated_emissions_kg_co2e", names="fuel_type", hole=0.4,
                      color_discrete_sequence=px.colors.sequential.YlGnBu)
        st.plotly_chart(fig4, use_container_width=True)
