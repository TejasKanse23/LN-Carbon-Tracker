import joblib
import pandas as pd

import os

# Get path relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "carbon_emission_model.pkl")

# Load model once
model = joblib.load(MODEL_PATH)

def predict(data: dict):

    # create ton_km feature
    data["ton_km"] = data["distance_km"] * data["weight_ton"]

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return float(prediction[0])


# local testing
if __name__ == "__main__":
    sample_data = {
        "origin": "Mumbai",
        "destination": "Pune",
        "lane": "Mumbai - Pune",
        "distance_km": 150,
        "vehicle_type": "Truck",
        "fuel_type": "Diesel",
        "weight_ton": 12,
        "utilization_percent": 85,
        "average_speed_kmph": 55,
        "transit_time_hrs": 4,
        "fuel_consumption_L": 40,
        "co2_per_ton_km": 0.85,
        "traffic congestion": "Medium",
        "Age of vehicle": 4,
        "Engine size ( Capacity of liters of fuel)": 6.5
    }

    result = predict(sample_data)

    print("Predicted Emission:", result)