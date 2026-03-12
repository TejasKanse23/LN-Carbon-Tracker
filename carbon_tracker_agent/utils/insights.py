import pandas as pd

def get_dashboard_kpis(df: pd.DataFrame, lane_df: pd.DataFrame):
    total_emissions = df["estimated_emissions_kg_co2e"].sum()
    total_shipments = len(df)
    avg_emissions = total_emissions / total_shipments if total_shipments > 0 else 0
    highest_lane = lane_df.sort_values(by="total_emissions", ascending=False).iloc[0]["lane"] if not lane_df.empty else "N/A"
    
    avg_co2_ton_km = lane_df["average_co2_per_ton_km"].mean() if "average_co2_per_ton_km" in lane_df.columns else 0
    potential_reduction_pct = 15.0 
    
    return {
        "Total Emissions (kg)": round(total_emissions, 1),
        "Total Shipments": total_shipments,
        "Avg Emissions/Shipment (kg)": round(avg_emissions, 1),
        "Highest Emission Lane": highest_lane,
        "Avg CO2/Ton-KM": round(avg_co2_ton_km, 4),
        "Reduction Opportunity": f"{potential_reduction_pct}%"
    }

def get_top_hotspots(lane_df: pd.DataFrame, top_n=5):
    return lane_df.sort_values(by="total_emissions", ascending=False).head(top_n)
