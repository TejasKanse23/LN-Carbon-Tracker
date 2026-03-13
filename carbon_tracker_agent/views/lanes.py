import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_custom_css, page_header, section_header

PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,24,39,0.6)",
    font=dict(family="Inter, sans-serif", color="#94a3b8"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    margin=dict(l=12, r=12, t=36, b=12),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
)

HOTSPOT_COLORS = {
    "High Emission Lane":              "#ef4444",
    "Carbon Intensity Hotspot":        "#f97316",
    "High Emission + Low Utilization": "#dc2626",
    "Low Utilization Lane":            "#facc15",
    "Normal":                          "#10b981",
}

def show(lane_df):
    inject_custom_css()
    page_header("🛣️", "Lane Analytics",
                "Aggregate insights identifying high-emission and low-utilization routes.")

    # ── Hotspot Alert ────────────────────────────────────────────
    section_header("🚨 Route Hotspots")

    critical_tags = ['High Emission Lane', 'Carbon Intensity Hotspot', 'High Emission + Low Utilization']
    high_risks = lane_df[lane_df['hotspot_tag'].isin(critical_tags)]

    if not high_risks.empty:
        st.markdown(f"""
        <div style="background:rgba(239,68,68,0.10);border:1px solid rgba(239,68,68,0.35);
                    border-radius:10px;padding:0.9rem 1.25rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:0.6rem;">
            <span style="font-size:1.3rem;">🚨</span>
            <div>
                <span style="color:#f87171;font-weight:700;">
                    {len(high_risks)} high-priority hotspot lanes
                </span>
                <span style="color:#94a3b8;font-size:0.88rem;">
                    &nbsp;— Immediate optimization recommended
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(
        lane_df.style
            .map(lambda x: 'background-color: rgba(239,68,68,0.18); color: #f87171;'
                 if x in critical_tags else '', subset=['hotspot_tag'])
            .map(lambda x: 'background-color: rgba(250,204,21,0.14); color: #fde047;'
                 if x == 'Low Utilization Lane' else '', subset=['hotspot_tag'])
            .format({
                'total_emissions':          '{:.1f}',
                'average_emissions':        '{:.1f}',
                'average_utilization':      '{:.1f}%',
                'average_transit_time_hrs': '{:.1f}',
                'average_speed_kmph':       '{:.1f}',
                'average_co2_per_ton_km':   '{:.4f}',
            }, na_rep='-'),
        use_container_width=True,
        height=360,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        section_header("⚖️ Emissions vs Utilization")
        fig1 = px.scatter(
            lane_df,
            x="average_utilization", y="total_emissions",
            size="shipment_count", color="hotspot_tag",
            hover_name="lane",
            labels={"average_utilization": "Avg Utilization (%)",
                    "total_emissions":      "Total Emissions (kg)"},
            color_discrete_map=HOTSPOT_COLORS,
            template="plotly_dark",
        )
        fig1.update_layout(**PLOTLY_TEMPLATE)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        section_header("🛠️ Top Lane Decarbonization Actions")
        top8 = lane_df.sort_values("total_emissions", ascending=False).head(8)
        for _, row in top8.iterrows():
            tag = row['hotspot_tag']
            dot_color = HOTSPOT_COLORS.get(tag, "#10b981")
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:0.55rem;
                        margin-bottom:0.7rem;padding:0.6rem 0.8rem;
                        background:rgba(255,255,255,0.03);border-radius:8px;
                        border:1px solid rgba(255,255,255,0.06);">
                <span style="color:{dot_color};margin-top:2px;font-size:0.7rem;">⬤</span>
                <div>
                    <div style="font-weight:600;font-size:0.83rem;color:#f1f5f9;">
                        {row['lane']}
                    </div>
                    <div style="font-size:0.78rem;color:#94a3b8;margin-top:2px;">
                        {row['recommendation_summary']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("🏎️ Speed vs. Emission Intensity Correlation")

    fig2 = px.scatter(
        lane_df,
        x="average_speed_kmph", y="average_co2_per_ton_km",
        size="shipment_count", color="hotspot_tag",
        hover_name="lane",
        trendline="ols",
        labels={"average_speed_kmph":    "Avg Speed (km/h)",
                "average_co2_per_ton_km": "CO₂ per Ton-KM"},
        color_discrete_map=HOTSPOT_COLORS,
        template="plotly_dark",
    )
    fig2.update_layout(**PLOTLY_TEMPLATE)
    st.plotly_chart(fig2, use_container_width=True)
