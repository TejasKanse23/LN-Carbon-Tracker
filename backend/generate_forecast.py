import pandas as pd
import numpy as np
import argparse
import json
import os
import sys

def forecast_emissions(origin, dest, horizon=6):
    data_path = os.path.join(os.path.dirname(__file__), "..", "carbon_tracker_agent", "data", "carbon_tracker_shipments.csv")
    if not os.path.exists(data_path):
        return {"error": "Dataset not found"}
        
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
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
    history_data = [{"date": ts.strftime('%b %Y'), "value": float(val)} for ts, val in zip(monthly.index, monthly['estimated_emissions_kg_co2e'])]
    forecast_data = [{"date": ts.strftime('%b %Y'), "value": max(0, float(val))} for ts, val in zip(forecast.index, forecast)]
    
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
        "historical": history_data,
        "forecast": forecast_data,
        "summary": {
            "historical_mean": float(hist_avg),
            "forecast_mean": float(fut_avg),
            "growth_pct": float(growth_pct),
            "trend": direction
        },
        "explanation": explanation,
        "riskInsight": risk_insight
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--horizon", type=int, default=6)
    args = parser.parse_args()
    
    try:
        result = forecast_emissions(args.origin, args.dest, args.horizon)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
