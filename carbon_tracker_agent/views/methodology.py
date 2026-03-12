import streamlit as st

def show():
    st.title("📖 Assessment Methodology")
    st.markdown("Transparency on how carbon emissions are calculated within this prototype.")
    
    st.info("ℹ️ **Prototype Disclaimer**: The emission factors and formulas used in this application are simplified estimates designed for hackathon demonstration. They do not replace certified carbon accounting frameworks (like GLEC).")
    
    st.header("Core Formula")
    st.latex(r"E = D \times W \times EF \times UF \times FF")
    
    st.markdown("""
    Where:
    - **E**: Estimated Emissions in kg CO₂e
    - **D**: Distance in kilometers
    - **W**: Cargo weight in metric tons
    - **EF**: Base Emission Factor (by vehicle type)
    - **UF**: Utilization Penalty Factor
    - **FF**: Fuel Type Adjustment Factor
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vehicle Base Factors (EF)")
        st.markdown("- Heavy Truck: **0.08** kg CO₂/t-km")
        st.markdown("- Medium Truck: **0.12** kg CO₂/t-km")
        st.markdown("- Light Truck: **0.18** kg CO₂/t-km")
        
        st.subheader("Fuel Adjustments (FF)")
        st.markdown("- Diesel: **1.0** (Base)")
        st.markdown("- CNG: **0.85** (15% reduction)")
        st.markdown("- EV: **0.10** (90% reduction at tailpipe)")
        
    with col2:
        st.subheader("Utilization Penalties (UF)")
        st.markdown("Low utilization means burning fuel for empty space. We penalize shipments as follows:")
        st.markdown("- Utilization $\\geq$ 80%: **1.0x** penalty (Optimal)")
        st.markdown("- Utilization 50% - 79%: **1.05x** penalty")
        st.markdown("- Utilization < 50%: **1.2x** penalty (Highly inefficient)")
        
    st.header("Generative AI Assistant")
    st.markdown("""
    The AI assistant runs on **Google Gemini 1.5 Flash**. 
    Every time you ask a question, the application builds a **data context payload** containing:
    1. Overall KPIs and totals
    2. Lane rankings
    3. The formula above
    
    Gemini uses this explicit context to give grounded, quantitative, and relevant answers rather than generic advice.
    """)
