import streamlit as st
import plotly.express as px

def show(lane_df):
    st.title("🛣️ Lane Analytics")
    st.markdown("Aggregate insights identifying high-emission and low-utilization routes.")
    
    st.markdown("### Route Hotspots")
    
    # Grid of warnings for high risk
    critical_tags = ['High Emission Lane', 'Carbon Intensity Hotspot', 'High Emission + Low Utilization']
    high_risks = lane_df[lane_df['hotspot_tag'].isin(critical_tags)]
    if not high_risks.empty:
        st.error(f"🚨 Identified {len(high_risks)} high-priority hotspot lanes requiring optimization.")
        
    st.dataframe(
        lane_df.style.map(lambda x: 'background-color: #fca5a5; color: black;' if x in critical_tags else '', subset=['hotspot_tag'])
                     .map(lambda x: 'background-color: #fef08a; color: black;' if x == 'Low Utilization Lane' else '', subset=['hotspot_tag'])
                     .format({
                         'total_emissions': '{:.1f}', 
                         'average_emissions': '{:.1f}', 
                         'average_utilization': '{:.1f}%',
                         'average_transit_time_hrs': '{:.1f}',
                         'average_speed_kmph': '{:.1f}',
                         'average_co2_per_ton_km': '{:.4f}'
                     }, na_rep='-'),
        use_container_width=True
    )
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Emissions vs Utilization")
        
        hotspot_colors = {
            "High Emission Lane": "#ef4444",
            "Carbon Intensity Hotspot": "#f97316",
            "High Emission + Low Utilization": "#dc2626",
            "Low Utilization Lane": "#facc15",
            "Normal": "#10b981"
        }
        
        fig1 = px.scatter(lane_df, x="average_utilization", y="total_emissions", size="shipment_count", color="hotspot_tag", hover_name="lane",
                          labels={"average_utilization": "Avg Utilization (%)", "total_emissions": "Total Emissions (kg)"},
                          color_discrete_map=hotspot_colors)
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.subheader("Top Lane Decarbonization Actions")
        for _, row in lane_df.sort_values(by="total_emissions", ascending=False).head(8).iterrows():
            st.markdown(f"- **{row['lane']}**: {row['recommendation_summary']}")

    st.markdown("---")
    st.subheader("Speed vs. Emission Intensity Correlation")
    fig2 = px.scatter(lane_df, x="average_speed_kmph", y="average_co2_per_ton_km", size="shipment_count", color="hotspot_tag", hover_name="lane",
                      trendline="ols",
                      labels={"average_speed_kmph": "Avg Speed (km/h)", "average_co2_per_ton_km": "CO2 per Ton-KM"},
                      color_discrete_map=hotspot_colors)
    st.plotly_chart(fig2, use_container_width=True)
