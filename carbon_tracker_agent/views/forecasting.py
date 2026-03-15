import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def forecast_emissions(df, origin, dest, horizon=6):
    # Filter lane
    lane_df = df[(df['origin'].str.lower() == origin.lower()) & (df['destination'].str.lower() == dest.lower())].copy()
    if lane_df.empty:
        return {"error": "No shipments found for this lane"}
        
    # Aggregate monthly
    lane_df['month'] = lane_df['date'].dt.to_period('M')
    monthly = lane_df.groupby('month')['estimated_emissions_kg_co2e'].sum().reset_index()
    monthly['month'] = monthly['month'].dt.to_timestamp()
    monthly = monthly.sort_values('month')
    monthly.set_index('month', inplace=True)
    
    # Resample to fill missing months with 0
    monthly = monthly.resample('MS').sum()
    
    if len(monthly) < 3:
        return {"error": "Not enough historical data to generate an accurate forecast (minimum 3 months required)."}

    # Use Holt-Winters or ARIMA
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        seasonal_periods = 12 if len(monthly) >= 24 else None
        trend = 'add'
        seasonal = 'add' if seasonal_periods else None
        
        model = ExponentialSmoothing(monthly['estimated_emissions_kg_co2e'], trend=trend, seasonal=seasonal, seasonal_periods=seasonal_periods, initialization_method="estimated")
        fit_model = model.fit()
        forecast = fit_model.forecast(horizon)
        
    except Exception as e:
        # Fallback to simple linear regression if statsmodels fails
        x = np.arange(len(monthly))
        y = monthly['estimated_emissions_kg_co2e'].values
        m, c = np.polyfit(x, y, 1)
        forecast_x = np.arange(len(monthly), len(monthly) + horizon)
        # Create future index
        future_idx = pd.date_range(start=monthly.index[-1] + pd.DateOffset(months=1), periods=horizon, freq='MS')
        forecast = pd.Series(m * forecast_x + c, index=future_idx)

    # Format output
    history_data = [{"date": ts.strftime('%b %Y'), "Historical": float(val), "Forecast": None} for ts, val in zip(monthly.index, monthly['estimated_emissions_kg_co2e'])]
    
    # Link point
    last_hist = history_data[-1]
    link_point = {"date": last_hist["date"], "Historical": None, "Forecast": last_hist["Historical"]}
    
    forecast_data = [{"date": ts.strftime('%b %Y'), "Historical": None, "Forecast": max(0, float(val))} for ts, val in zip(forecast.index, forecast)]
    
    chart_data = history_data + [link_point] + forecast_data
    
    # Compute Insights
    hist_avg = monthly['estimated_emissions_kg_co2e'].mean()
    fut_avg = max(0, forecast.mean())
    growth_pct = ((fut_avg - hist_avg) / hist_avg * 100) if hist_avg > 0 else 0
    
    direction = "stable"
    if growth_pct > 5:
         direction = "increasing"
    elif growth_pct < -5:
         direction = "decreasing"
         
    explanation = f"Emissions on the {origin.title()} → {dest.title()} lane are expected to be {direction}. "
    if direction == "increasing":
         explanation += f"We project an average {growth_pct:.1f}% growth over the next {horizon} months driven by historical shipment volume expansion."
    elif direction == "decreasing":
         explanation += f"We project an average {abs(growth_pct):.1f}% decline over the next {horizon} months."
    else:
         explanation += f"Historical trends show steady shipment volumes, predicting stable emissions around {hist_avg:,.0f} kg CO2/month."
         
    risk_insight = None
    if growth_pct > 5 and fut_avg > 500:
        risk_insight = f"🚨 Hotspot Warning: This lane is at risk of becoming a major carbon hotspot. Sustained {growth_pct:.1f}% emission growth detected. Load consolidation or EV adoption is highly recommended to stabilize trends."

    return {
        "lane": f"{origin.title()} → {dest.title()}",
        "chartData": chart_data,
        "summary": {
            "historical_mean": float(hist_avg),
            "forecast_mean": float(fut_avg),
            "growth_pct": float(growth_pct),
            "trend": direction
        },
        "explanation": explanation,
        "riskInsight": risk_insight
    }

def show(df):
    st.markdown("## 🧭 AI Emission Trend Forecasting")
    st.markdown("Predict future carbon emissions for a selected lane based on historical data patterns.")
    
    origins = sorted(df['origin'].dropna().unique())
    destinations = sorted(df['destination'].dropna().unique())
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        origin = st.selectbox("Origin", origins, index=origins.index("Mumbai") if "Mumbai" in origins else 0)
    with col2:
        dest = st.selectbox("Destination", destinations, index=destinations.index("Delhi") if "Delhi" in destinations else 0)
    with col3:
        horizon = st.selectbox("Horizon", [3, 6, 12], index=1)
    with col4:
        st.write("")
        st.write("")
        generate_btn = st.button("Generate Forecast", use_container_width=True, type="primary")
        
    if generate_btn:
        if origin == dest:
            st.warning("Origin and destination must be different.")
        else:
            with st.spinner("Analyzing Trends..."):
                result = forecast_emissions(df, origin, dest, horizon)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown("---")
                    
                    st.markdown(f"### Lane Forecast: {result['lane']}")
                    
                    # KPIs
                    kpi1, kpi2, kpi3 = st.columns(3)
                    
                    with kpi1:
                        st.markdown(f"""
                        <div class="glass-panel" style="padding:15px; border-radius:8px;">
                            <div style="color:var(--text-secondary); font-size:0.85rem;">Historical Avg (Monthly)</div>
                            <div style="font-size:1.5rem; color:#3b82f6; font-weight:bold;">{round(result['summary']['historical_mean']):,} kg CO₂</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with kpi2:
                        st.markdown(f"""
                        <div class="glass-panel" style="padding:15px; border-radius:8px;">
                            <div style="color:var(--text-secondary); font-size:0.85rem;">Predicted Avg (Monthly)</div>
                            <div style="font-size:1.5rem; color:#8b5cf6; font-weight:bold;">{round(result['summary']['forecast_mean']):,} kg CO₂</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with kpi3:
                        trend_color = "#fca5a5" if result['summary']['trend'] == 'increasing' else "#6ee7b7" if result['summary']['trend'] == 'decreasing' else "white"
                        st.markdown(f"""
                        <div class="glass-panel" style="padding:15px; border-radius:8px;">
                            <div style="color:var(--text-secondary); font-size:0.85rem;">Growth / Decline</div>
                            <div style="font-size:1.5rem; color:{trend_color}; font-weight:bold;">{abs(result['summary']['growth_pct']):.1f}%</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Insights
                    st.info(result['explanation'], icon="🤖")
                    
                    if result['riskInsight']:
                        st.error(result['riskInsight'])
                        
                    # Chart
                    chart_df = pd.DataFrame(result['chartData'])
                    
                    fig = go.Figure()
                    
                    # Historical Area
                    hist_mask = chart_df['Historical'].notna()
                    if hist_mask.any():
                        fig.add_trace(go.Scatter(
                            x=chart_df.loc[hist_mask, 'date'],
                            y=chart_df.loc[hist_mask, 'Historical'],
                            fill='tozeroy',
                            mode='lines+markers',
                            name='Historical',
                            line=dict(color='#3b82f6', width=2),
                            fillcolor='rgba(59, 130, 246, 0.2)',
                            marker=dict(size=6)
                        ))
                    
                    # Forecast Area
                    fore_mask = chart_df['Forecast'].notna()
                    if fore_mask.any():
                        fig.add_trace(go.Scatter(
                            x=chart_df.loc[fore_mask, 'date'],
                            y=chart_df.loc[fore_mask, 'Forecast'],
                            fill='tozeroy',
                            mode='lines+markers',
                            name='Forecast',
                            line=dict(color='#8b5cf6', width=2, dash='dash'),
                            fillcolor='rgba(139, 92, 246, 0.2)',
                            marker=dict(size=6)
                        ))
                        
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False, color='white'),
                        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='white'),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="white")),
                        margin=dict(l=0, r=0, b=0, t=30)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
