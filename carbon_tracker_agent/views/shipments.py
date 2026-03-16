import streamlit as st
import pandas as pd
from utils.theme import inject_custom_css, page_header, section_header

def show(df):
    inject_custom_css()
    page_header("🚚", "Shipment Analytics",
                "Granular carbon footprint view for individual shipments.")

    # ── Filters ──────────────────────────────────────────────────
    section_header("🔍 Filters")

    col1, col2, col3, col4 = st.columns(4, gap="small")
    with col1:
        search_id = st.text_input("Search Shipment ID", "", placeholder="e.g. SH-001")
    with col2:
        lanes = ["All"] + sorted(df['lane'].unique().tolist())
        selected_lane = st.selectbox("Lane", lanes)
    with col3:
        vehicles = ["All"] + sorted(df['vehicle_type'].unique().tolist())
        selected_vehicle = st.selectbox("Vehicle Type", vehicles)
    with col4:
        fuels = ["All"] + sorted(df['fuel_type'].unique().tolist())
        selected_fuel = st.selectbox("Fuel Type", fuels)

    # ── Apply filters ────────────────────────────────────────────
    filtered_df = df.copy()
    if search_id:
        filtered_df = filtered_df[filtered_df['shipment_id'].str.contains(search_id, case=False)]
    if selected_lane    != "All": filtered_df = filtered_df[filtered_df['lane']         == selected_lane]
    if selected_vehicle != "All": filtered_df = filtered_df[filtered_df['vehicle_type'] == selected_vehicle]
    if selected_fuel    != "All": filtered_df = filtered_df[filtered_df['fuel_type']    == selected_fuel]

    # Result badge
    st.markdown(f"""
    <div style="margin:0.5rem 0 1rem;">
        <span class="stat-badge">📦 {len(filtered_df):,} shipments found</span>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(filtered_df, use_container_width=True, height=380)

    st.markdown("<hr>", unsafe_allow_html=True)
    section_header("🔬 Inspect Shipment Details")

    options = ["— Select a shipment —"] + list(filtered_df['shipment_id'].head(50))
    shipment_to_inspect = st.selectbox("Select Shipment ID to trace calculation:", options)

    if shipment_to_inspect != "— Select a shipment —":
        row = df[df['shipment_id'] == shipment_to_inspect].iloc[0]

        col_a, col_b = st.columns([1, 1], gap="medium")

        with col_a:
            st.markdown(f"""
            <div class="insight-card blue">
                <div class="ic-title">📋 Shipment Profile</div>
                <div class="ic-body">
                    <strong>ID:</strong> {row['shipment_id']}<br>
                    <strong>Lane:</strong> {row['lane']}<br>
                    <strong>Distance:</strong> {row['distance_km']} km<br>
                    <strong>Weight:</strong> {row['weight_ton']} tons<br>
                    <strong>Vehicle:</strong> {row['vehicle_type']}<br>
                    <strong>Fuel:</strong> {row['fuel_type']}<br>
                    <strong>Utilization:</strong> {row['utilization_percent']}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            # Recalculate factors
            v_type_lower = str(row['vehicle_type']).lower()
            if 'heavy' in v_type_lower or '18mt' in v_type_lower or '20mt' in v_type_lower:
                factor = 0.08
            elif 'medium' in v_type_lower or '17mt' in v_type_lower or '15mt' in v_type_lower:
                factor = 0.12
            else:
                factor = 0.18

            utilization = float(row['utilization_percent'])
            util_penalty = 1.0
            if utilization < 50:
                util_penalty = 1.2
            elif utilization < 80:
                util_penalty = 1.05

            fuel_adj = 1.0
            f_type_lower = str(row['fuel_type']).lower()
            if f_type_lower == 'cng':
                fuel_adj = 0.85
            elif f_type_lower == 'ev':
                fuel_adj = 0.1

            st.markdown(f"""
            <div class="insight-card green">
                <div class="ic-title">⚗️ Emission Calculation Trace</div>
                <div class="ic-body">
                    <strong>Formula:</strong><br>
                    <code style="background:rgba(16,185,129,0.1);padding:0.3rem 0.5rem;
                                 border-radius:6px;font-size:0.82rem;display:block;margin:0.5rem 0;">
                        {row['distance_km']} km × {row['weight_ton']} t × {factor} (EF) × {util_penalty} (UF) × {fuel_adj} (FF)
                    </code>
                    <div style="margin-top:0.75rem;font-size:1rem;">
                        <span style="color:#10b981;font-weight:800;">
                            ✅ {row['estimated_emissions_kg_co2e']} kg CO₂e
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
