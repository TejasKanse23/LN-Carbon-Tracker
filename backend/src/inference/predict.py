import joblib
import pandas as pd

# Load model once
model = joblib.load("models/carbon_emission_model.pkl")

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