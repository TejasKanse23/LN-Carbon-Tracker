import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .emissions import calculate_emissions
import os

LANES = [
    ("Mumbai", "Delhi", 1421),
    ("Pune", "Bangalore", 840),
    ("Chennai", "Hyderabad", 630),
    ("Ahmedabad", "Jaipur", 680),
    ("Nagpur", "Mumbai", 810),
    ("Delhi", "Lucknow", 550),
    ("Surat", "Indore", 450),
    ("Bangalore", "Chennai", 350)
]

VEHICLES = ["Heavy Truck", "Medium Truck", "Light Truck"]
FUELS = ["Diesel", "CNG", "EV"]

def generate_mock_data(num_records=100, output_dir="data"):
    np.random.seed(42)
    os.makedirs(output_dir, exist_ok=True)
    
    records = []
    base_date = datetime.now()
    
    for i in range(num_records):
        lane = LANES[np.random.randint(0, len(LANES))]
        vehicle = VEHICLES[np.random.randint(0, len(VEHICLES))]
        fuel = "Diesel" if vehicle == "Heavy Truck" else FUELS[np.random.randint(0, len(FUELS))]
        
        weight = np.random.uniform(5.0, 25.0) if vehicle == "Heavy Truck" else np.random.uniform(1.0, 10.0)
        utilization = np.random.uniform(40.0, 100.0)
        distance = lane[2] * np.random.uniform(0.95, 1.05) # Add some variance
        
        date = base_date - timedelta(days=np.random.randint(0, 30))
        
        emissions = calculate_emissions(distance, weight, vehicle, utilization)
        if fuel == "CNG":
            emissions *= 0.85
        elif fuel == "EV":
            emissions *= 0.1
            
        records.append({
            "shipment_id": f"SHP{str(i+1000).zfill(5)}",
            "origin": lane[0],
            "destination": lane[1],
            "lane": f"{lane[0]} - {lane[1]}",
            "date": date.strftime("%Y-%m-%d"),
            "distance_km": round(distance, 1),
            "weight_ton": round(weight, 1),
            "vehicle_type": vehicle,
            "fuel_type": fuel,
            "utilization_percent": round(utilization, 1),
            "estimated_emissions_kg_co2e": round(emissions, 1)
        })
        
    df = pd.DataFrame(records)
    df.to_csv(f"{output_dir}/carbon_tracker_shipments.csv", index=False)
    
    # Generate Lane Summaries
    lane_summary = df.groupby("lane").agg(
        shipment_count=("shipment_id", "count"),
        total_emissions=("estimated_emissions_kg_co2e", "sum"),
        average_emissions=("estimated_emissions_kg_co2e", "mean"),
        average_utilization=("utilization_percent", "mean")
    ).reset_index()
    
    # Tag hotspots
    q75 = lane_summary["total_emissions"].quantile(0.75)
    lane_summary["hotspot_tag"] = lane_summary["total_emissions"].apply(lambda x: "High Risk" if x > q75 else "Monitor")
    
    def get_rec(row):
        if row["average_utilization"] < 60:
            return "Consolidate loads to improve utilization."
        elif row["hotspot_tag"] == "High Risk":
            return "Shift to EV/CNG or optimize routing."
        return "Maintain current efficiency."
        
    lane_summary["recommendation_summary"] = lane_summary.apply(get_rec, axis=1)
    lane_summary.to_csv(f"{output_dir}/carbon_tracker_lane_summary.csv", index=False)
    
    return df, lane_summary
