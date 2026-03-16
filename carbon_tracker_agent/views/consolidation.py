import streamlit as st
import pandas as pd
import numpy as np
import time
from utils.theme import section_header
from utils.chatbot import initialize_gemini

def show(df: pd.DataFrame):
    st.markdown(
        "<h2 style='color:#10b981;margin-bottom:0.2rem;'>📦 Automated Load Consolidation Agent</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#94a3b8;margin-top:0;'>"
        "The AI Agent scans your historical and active shipments, grouping them by Lane and Date to identify instances where under-utilized trucks can be merged to eliminate wasted trips and emissions.</p>",
        unsafe_allow_html=True,
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Find Consolidation Opportunities", type="primary", use_container_width=True):
        
        # 1. UI Loading State
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Agent is grouping 120,000+ shipments by Lane and Date...")
        time.sleep(1) # For UX effect
        progress_bar.progress(30)
        
        # 2. Mathematical Consolidation Logic (Vectorized)
        status_text.text("Agent is calculating perfect-fit packing by truck utilization...")
        
        # Group by lane and date
        agg_df = df.groupby(['lane', 'date']).agg(
            current_trucks=('shipment_id', 'count'),
            total_utilization=('utilization_percent', 'sum'),
            distance_km=('distance_km', 'first'),
            avg_co2_per_truck=('estimated_emissions_kg_co2e', 'mean'),
            total_weight=('weight_ton', 'sum')
        ).reset_index()
        
        # If total utilization is 150%, we need ceil(150 / 100) = 2 trucks instead of maybe 3 or 4.
        # We assume trucks on the same lane can carry up to 100% of theoretical capacity.
        agg_df['optimized_trucks'] = np.ceil(agg_df['total_utilization'] / 100.0).astype(int)
        # Ensure we don't accidentally "increase" trucks and clamp to minimum 1
        agg_df['optimized_trucks'] = agg_df[['optimized_trucks', 'current_trucks']].min(axis=1)
        agg_df['optimized_trucks'] = agg_df['optimized_trucks'].clip(lower=1)
        
        # Calculate Savings
        agg_df['trucks_saved'] = agg_df['current_trucks'] - agg_df['optimized_trucks']
        agg_df['distance_saved_km'] = agg_df['trucks_saved'] * agg_df['distance_km']
        agg_df['co2_saved_kg'] = agg_df['trucks_saved'] * agg_df['avg_co2_per_truck']
        
        progress_bar.progress(70)
        status_text.text("Generating Agentic Strategy Report using Gemini AI...")
        
        # Isolate the opportunities
        opportunities = agg_df[agg_df['trucks_saved'] > 0].copy()
        
        total_redundant = int(opportunities['trucks_saved'].sum())
        total_dist_saved = float(opportunities['distance_saved_km'].sum())
        total_co2_saved = float(opportunities['co2_saved_kg'].sum())
        
        # Lanewise summary for the datatable
        lane_opps = opportunities.groupby('lane').agg(
            trucks_saved=('trucks_saved', 'sum'),
            co2_saved_kg=('co2_saved_kg', 'sum'),
            distance_saved_km=('distance_saved_km', 'sum')
        ).reset_index().sort_values('co2_saved_kg', ascending=False)
        
        progress_bar.progress(95)
        
        # 3. Gemini Generative Report
        model = initialize_gemini()
        ai_message = ""
        
        core_message = f"Agent identified {total_redundant:,} redundant shipments. By combining these loads, you can eliminate {total_dist_saved:,.0f} km of driving and save {total_co2_saved:,.0f} kg of CO₂e immediately."
        
        if model:
            # We construct a prompt passing the calculated data
            prompt = f"""
            You are the CarbonTrack AI Agent. You have just completed a load consolidation analysis on a logistics dataset.
            Here are the hard numbers you found:
            - Redundant Shipments Identified: {total_redundant:,}
            - Distance That Can Be Eliminated: {total_dist_saved:,.0f} km
            - CO2e Emissions Saved: {total_co2_saved:,.0f} kg
            
            Write a professional, impactful, 2-paragraph executive summary for the Logistics Director expanding on this core message: "{core_message}".
            Paragraph 1: Focus on the root cause (under-utilized trucks leaving on the same origin for the same destination on the same day).
            Paragraph 2: Recommend an immediate operational change to capture these savings (e.g., dynamic hold policies, cross-docking).
            Use a confident, agentic tone.
            """
            try:
                response = model.generate_content(prompt)
                ai_message = f"**{core_message}**\n\n{response.text}"
            except Exception as e:
                ai_message = f"**{core_message}**"
        else:
            ai_message = f"**{core_message}**"
            
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        # 4. Render the Results Screen
        st.success("✅ Analysis Complete! Consolidation Opportunities Identified.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Redundant Shipments", f"{total_redundant:,} trips", delta="-100% Waste", delta_color="inverse")
        m2.metric("Distance Saved", f"{total_dist_saved:,.0f} km", delta="Fewer road miles", delta_color="normal")
        m3.metric("CO₂e Prevented", f"{total_co2_saved:,.0f} kg", delta="Carbon offset", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
<div style="background:#111827; border-left:4px solid #3b82f6; padding: 1.5rem; border-radius: 8px; font-size: 1rem; color: #e2e8f0; line-height: 1.6;">
    <div style="display:flex; align-items:center; gap: 0.5rem; margin-bottom: 0.75rem;">
        <span style="font-size: 1.5rem;">🤖</span>
        <strong style="color: #3b82f6; font-size: 1.1rem;">Agent Intelligence Report</strong>
    </div>
    {ai_message}
</div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("Top 20 Immediate Lane Consolidations")
        
        # Format the dataframe for display
        display_df = lane_opps.head(20).copy()
        display_df['co2_saved_kg'] = display_df['co2_saved_kg'].map(lambda x: f"{x:,.0f} kg")
        display_df['distance_saved_km'] = display_df['distance_saved_km'].map(lambda x: f"{x:,.0f} km")
        display_df.rename(columns={
            'lane': 'Shipping Lane',
            'trucks_saved': 'Trips Eliminated',
            'co2_saved_kg': 'CO₂e Prevented',
            'distance_saved_km': 'Distance Saved'
        }, inplace=True)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
