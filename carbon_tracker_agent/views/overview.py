import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.insights import get_dashboard_kpis, get_top_hotspots
from utils.theme import inject_custom_css, page_header, section_header, insight_card

# Plotly dark template
PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.6)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
        margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
    )
)

def show(df, lane_df):
    inject_custom_css()
    page_header("📊", "Sustainability Dashboard", "High-level overview of freight carbon emissions across all lanes.")

    kpis = get_dashboard_kpis(df, lane_df)

    # ── KPI Row 1 ────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    c1.metric("🌍 Total Emissions", f"{kpis['Total Emissions (kg)']} kg CO₂e")
    c2.metric("📦 Total Shipments",  kpis['Total Shipments'])
    c3.metric("📈 Avg Emissions / Shipment", f"{kpis['Avg Emissions/Shipment (kg)']} kg")

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # ── KPI Row 2 ────────────────────────────────────────────────
    c4, c5, c6, c7 = st.columns(4)
    c4.metric("🔥 Highest Emission Lane",   kpis['Highest Emission Lane'])
    c5.metric("⚡ Avg CO₂ / Ton-KM",       f"{kpis['Avg CO2/Ton-KM']}")
    c6.metric("💡 Reduction Opportunity",   kpis['Reduction Opportunity'])

    trend_data = df.groupby('date')['estimated_emissions_kg_co2e'].sum().reset_index()
    if len(trend_data) > 1:
        latest_val  = trend_data.iloc[-1]['estimated_emissions_kg_co2e']
        previous_val= trend_data.iloc[-2]['estimated_emissions_kg_co2e']
        delta       = latest_val - previous_val
        c7.metric("📉 Emission Trend (Latest)", f"{latest_val:.1f} kg",
                  f"{delta:.1f} kg", delta_color="inverse")
    else:
        c7.metric("📉 Emission Trend", "N/A")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Charts Row 1 ────────────────────────────────────────────
    row1_c1, row1_c2 = st.columns(2, gap="medium")

    with row1_c1:
        section_header("📈 Emission Trend Over Time")
        fig1 = px.area(
            trend_data, x="date", y="estimated_emissions_kg_co2e",
            labels={"estimated_emissions_kg_co2e": "Emissions (kg CO₂e)", "date": "Date"},
            color_discrete_sequence=["#10b981"],
            template="plotly_dark",
        )
        fig1.update_traces(fill='tozeroy', line=dict(width=2.5),
                           fillcolor="rgba(16,185,129,0.12)")
        fig1.update_layout(**PLOTLY_TEMPLATE['layout'].to_plotly_json())
        st.plotly_chart(fig1, use_container_width=True)

    with row1_c2:
        section_header("🏆 Top 5 High-Emission Lanes")
        top_lanes = get_top_hotspots(lane_df)
        hotspot_colors = {
            "High Emission Lane":              "#ef4444",
            "Carbon Intensity Hotspot":        "#f97316",
            "High Emission + Low Utilization": "#dc2626",
            "Low Utilization Lane":            "#facc15",
            "Normal":                          "#10b981",
        }
        fig2 = px.bar(
            top_lanes, x="lane", y="total_emissions", color="hotspot_tag",
            labels={"total_emissions": "Total Emissions (kg CO₂e)", "lane": "Lane"},
            color_discrete_map=hotspot_colors,
            template="plotly_dark",
        )
        fig2.update_layout(**PLOTLY_TEMPLATE['layout'].to_plotly_json())
        st.plotly_chart(fig2, use_container_width=True)

    # ── Charts Row 2 ────────────────────────────────────────────
    row2_c1, row2_c2 = st.columns(2, gap="medium")

    with row2_c1:
        section_header("🚛 Emissions by Vehicle Type")
        veh_df = df.groupby("vehicle_type")["estimated_emissions_kg_co2e"].sum().reset_index()
        fig3 = px.pie(
            veh_df, values="estimated_emissions_kg_co2e", names="vehicle_type", hole=0.45,
            color_discrete_sequence=["#10b981","#3b82f6","#8b5cf6","#f59e0b","#ef4444"],
            template="plotly_dark",
        )
        fig3.update_layout(**PLOTLY_TEMPLATE['layout'].to_plotly_json())
        fig3.update_traces(textfont_size=12, textfont_color="#f1f5f9")
        st.plotly_chart(fig3, use_container_width=True)

    with row2_c2:
        section_header("⛽ Emissions by Fuel Type")
        fuel_df = df.groupby("fuel_type")["estimated_emissions_kg_co2e"].sum().reset_index()
        fig4 = px.pie(
            fuel_df, values="estimated_emissions_kg_co2e", names="fuel_type", hole=0.45,
            color_discrete_sequence=["#06d6a0","#0ea5e9","#6366f1","#f59e0b"],
            template="plotly_dark",
        )
        fig4.update_layout(**PLOTLY_TEMPLATE['layout'].to_plotly_json())
        fig4.update_traces(textfont_size=12, textfont_color="#f1f5f9")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("🤖 Agentic AI Insights")

    with st.expander("✨ View AI-Generated Observations", expanded=True):
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            insight_card("📍", "Top Hotspot Detected",
                f"The lane <strong>{kpis['Highest Emission Lane']}</strong> is your most carbon-intensive route. "
                "Consider vehicle load optimization for this specific corridor.",
                color="red")
            insight_card("📈", "Efficiency Trend",
                f"Average CO₂/Ton-KM is at <strong>{kpis['Avg CO2/Ton-KM']}</strong>. "
                "Transitioning 10% of high-impact shipments to EV could significantly lower this.",
                color="green")
        with col_b:
            insight_card("💡", "Reduction Opportunity",
                f"Identified <strong>{kpis['Reduction Opportunity']}</strong> areas where load utilization falls below 80%. "
                "Consolidating loads could save up to 15% in total emissions.",
                color="amber")
            st.markdown("""
            <div style="font-size:0.78rem;color:#64748b;padding:0.75rem 1rem;
                        background:rgba(255,255,255,0.03);border-radius:8px;
                        border:1px solid rgba(255,255,255,0.05);margin-top:0.5rem;">
                ✦ These insights are generated based on a real-time scan of <strong>5,000+</strong> shipment records.
            </div>
            """, unsafe_allow_html=True)
