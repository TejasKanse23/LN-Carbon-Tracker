from fastapi import FastAPI

from src.inference.predict import predict
from src.services.vehicle_service import get_vehicle_details
from src.services.route_service import get_route
from src.services.feature_builder import build_model_input

app = FastAPI()

@app.post("/predict-emission")
def predict_emission(data: dict):

    origin = data["origin"]
    destination = data["destination"]
    vehicle_number = data["vehicle_number"]

    # Clean vehicle number (remove spaces, convert to uppercase)
    vehicle_number = vehicle_number.replace(" ", "").upper()
    vehicle_number = vehicle_number.replace("-", "")

    vehicle = get_vehicle_details(vehicle_number)

    route = get_route(origin, destination)

    model_input = build_model_input(
        vehicle,
        route,
        origin,
        destination
    )

    emission = predict(model_input)

    return {
        "predicted_emission_kg_co2e": emission
    }

# from fastapi import FastAPI, HTTPException
# from ..inference.predict import predict
# import pandas as pd
# from datetime import datetime

# app = FastAPI()

# # load vehicle dataset
# vehicle_df = pd.read_excel("data/raw/vehicle_dataset_20_rows.xlsx")

# def compute_vehicle_age(registration_date):
#     year = pd.to_datetime(registration_date).year
#     return datetime.now().year - year

# def get_vehicle_details(vehicle_number):

#     vehicle = vehicle_df[
#         vehicle_df["VEHICLE NUMBER"] == vehicle_number
#     ]

#     if vehicle.empty:
#         raise HTTPException(status_code=404, detail="Vehicle not found")

#     vehicle = vehicle.iloc[0]

#     return {
#         "fuel_type": vehicle["FUEL TYPE"],
#         "vehicle_type": vehicle["TRUCK TYPE"],
#         "Age of vehicle": vehicle["REGISTRATION DATE - AGE"],
#         "fuel_consumption_L": vehicle["AVG FUEL CONSUMPTION"]
#     }


# @app.post("/predict-emission")
# def predict_emission(data: dict):

#     vehicle_number = data["vehicle_number"]
#     origin = data["origin"]
#     destination = data["destination"]
#     traffic_congestion = data["traffic_congestion"]

#     vehicle_details = get_vehicle_details(vehicle_number)

#     # build full feature payload
#     model_input = {
#         "origin": origin,
#         "destination": destination,
#         "lane": f"{origin} - {destination}",
#         "distance_km": 150,
#         "vehicle_type": vehicle_details["vehicle_type"],
#         "fuel_type": vehicle_details["fuel_type"],
#         "weight_ton": 12,
#         "utilization_percent": 85,
#         "average_speed_kmph": 55,
#         "transit_time_hrs": 4,
#         "fuel_consumption_L": vehicle_details["fuel_consumption_L"],
#         "co2_per_ton_km": 0.85,
#         "traffic congestion": traffic_congestion,
#         "Age of vehicle": vehicle_details["Age of vehicle"],
#         "Engine size ( Capacity of liters of fuel)": 6.5
#     }

#     emission = predict(model_input)

#     return {
#         "predicted_emission_kg_co2e": emission
#     }
