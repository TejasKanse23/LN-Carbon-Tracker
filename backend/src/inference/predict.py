import joblib
import pandas as pd

import os

# Get path relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "carbon_emission_model.pkl")

# Load model once
model = joblib.load(MODEL_PATH)

def predict(data: dict):

    df = pd.DataFrame([data])

    prediction = model.predict(df)

    return float(prediction[0])


# Local test
if __name__ == "__main__":

    sample_data = {
        "origin": "Mumbai",
        "destination": "Pune",
        "lane": "Mumbai - Pune",
        "distance_km": 150,
        "weight_ton": 12,
        "vehicle_type": "Truck",
        "fuel_type": "Diesel",
        "utilization_percent": 85,
        "traffic congestion": "Medium",
        "Age of vehicle": 4,
        "Engine size ( Capacity of liters of fuel)": 6.5
    }

    result = predict(sample_data)

    print("Predicted Emission (kg CO2e):", round(result, 2))