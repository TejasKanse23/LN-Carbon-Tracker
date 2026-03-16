import os
import pandas as pd
from datetime import datetime

# Resolve path relative to this file so it works on Vercel & locally
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DATA_PATH = os.path.join(_BACKEND_DIR, "data", "raw", "carbon_tracker_shipments.csv")
dataset = pd.read_csv(_DATA_PATH)

engine_size_median = dataset["Engine size ( Capacity of liters of fuel)"].median()
weight_median = dataset["weight_ton"].median()
fuel_consumption_mean = dataset["fuel_consumption_L"].mean()
co2_mean = dataset["co2_per_ton_km"].mean()


def compute_vehicle_age(registration_date):
    year = pd.to_datetime(registration_date).year
    return datetime.now().year - year


def estimate_traffic(avg_speed):

    if avg_speed > 50:
        return "Low"
    elif avg_speed > 35:
        return "Medium"
    else:
        return "High"


def build_model_input(vehicle, route, origin, destination):

    distance = route["distance_km"]
    transit_time = route["duration_hrs"]

    avg_speed = distance / transit_time

    age = compute_vehicle_age(vehicle["registration_date"])

    model_input = {
        "origin": origin,
        "destination": destination,
        "lane": f"{origin}-{destination}",
        "distance_km": distance,
        "vehicle_type": "Truck",
        "fuel_type": vehicle["fuel_type"],
        "weight_ton": weight_median,
        "utilization_percent": 85,
        "average_speed_kmph": avg_speed,
        "transit_time_hrs": transit_time,
        "fuel_consumption_L": fuel_consumption_mean,
        "co2_per_ton_km": co2_mean,
        "traffic congestion": estimate_traffic(avg_speed),
        "Age of vehicle": age,
        "Engine size ( Capacity of liters of fuel)": engine_size_median
    }

    return model_input