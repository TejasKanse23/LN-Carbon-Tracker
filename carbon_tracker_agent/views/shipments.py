import streamlit as st
import pandas as pd

def show(df):
    st.title("🚚 Shipment Analytics")
    st.markdown("Understand granular carbon footprints for individual shipments.")
    
    st.markdown("### Filters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Just use a search box for simplicity instead of date range to avoid date picker complex state
        search_id = st.text_input("Search Shipment ID", "")
    with col2:
        lanes = ["All"] + list(df['lane'].unique())
        selected_lane = st.selectbox("Filter by Lane", lanes)
    with col3:
        vehicles = ["All"] + list(df['vehicle_type'].unique())
        selected_vehicle = st.selectbox("Filter by Vehicle Type", vehicles)
    with col4:
        fuels = ["All"] + list(df['fuel_type'].unique())
        selected_fuel = st.selectbox("Filter by Fuel Type", fuels)
        
    # Apply filters
    filtered_df = df.copy()
    if search_id:
        filtered_df = filtered_df[filtered_df['shipment_id'].str.contains(search_id, case=False)]
    if selected_lane != "All":
        filtered_df = filtered_df[filtered_df['lane'] == selected_lane]
    if selected_vehicle != "All":
        filtered_df = filtered_df[filtered_df['vehicle_type'] == selected_vehicle]
    if selected_fuel != "All":
        filtered_df = filtered_df[filtered_df['fuel_type'] == selected_fuel]
        
    st.markdown(f"**Found {len(filtered_df)} shipments**")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("### Inspect Shipment Details")
    options = ["None"] + list(filtered_df['shipment_id'].head(50))
    shipment_to_inspect = st.selectbox("Select Shipment ID to inspect calculation:", options)
    
    if shipment_to_inspect != "None":
        row = df[df['shipment_id'] == shipment_to_inspect].iloc[0]
        st.info("💡 **Prototype Calculation Trace**")
        st.markdown(f"**Shipment ID:** {row['shipment_id']} ({row['lane']})")
        st.markdown(f"- **Distance:** {row['distance_km']} km")
        st.markdown(f"- **Weight:** {row['weight_ton']} tons")
        st.markdown(f"- **Vehicle Type:** {row['vehicle_type']}")
        st.markdown(f"- **Fuel Type:** {row['fuel_type']}")
        st.markdown(f"- **Utilization:** {row['utilization_percent']}%")
        
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
            
        st.markdown(f"**Formula**: `{row['distance_km']} km * {row['weight_ton']} tons * {factor} (factor) * {util_penalty} (utilization) * {fuel_adj} (fuel)`")
        st.success(f"**Estimated Emissions**: {row['estimated_emissions_kg_co2e']} kg CO₂e")
