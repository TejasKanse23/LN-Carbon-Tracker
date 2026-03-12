import pandas as pd
from .insights import get_dashboard_kpis

def build_context(df: pd.DataFrame, lane_df: pd.DataFrame) -> str:
    kpis = get_dashboard_kpis(df, lane_df)
    
    context_lines = []
    context_lines.append("--- DASHBOARD SUMMARY ---")
    for k, v in kpis.items():
        context_lines.append(f"{k}: {v}")
        
    context_lines.append("\n--- LANE SUMMARIES (Top 5 by Emissions) ---")
    top_lanes = lane_df.sort_values("total_emissions", ascending=False).head(5)
    for _, row in top_lanes.iterrows():
        context_lines.append(f"Lane: {row['lane']} | Shipments: {row['shipment_count']} | Total Emissions: {row['total_emissions']}kg | Avg Util: {row['average_utilization']:.1f}% | Rec: {row['recommendation_summary']}")
        
    context_lines.append("\n--- EMISSION LOGIC ---")
    context_lines.append("Formula: distance_km * weight_ton * emission_factor * utilization_penalty")
    context_lines.append("Factors: Heavy Truck=0.08, Medium Truck=0.12, Light Truck=0.18")
    context_lines.append("CNG reduces by 15%, EV reduces by 90%. Utilization penalty applied if utilization < 80%.")
    
    return "\n".join(context_lines)
