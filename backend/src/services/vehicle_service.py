import os
import pandas as pd

# Resolve path relative to this file so it works on Vercel & locally
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_VEHICLE_DATA = os.path.join(_BACKEND_DIR, "data", "raw", "vehicle_dataset_20_rows.xlsx")

def get_vehicle_details(vehicle_number):

    df = pd.read_excel(_VEHICLE_DATA)
    vehicle = df[
        df["VEHICLE NUMBER"] == vehicle_number
    ]
    if vehicle.empty:
        raise ValueError("Vehicle not found")
    vehicle = vehicle.iloc[0]

    return {
        "fuel_type": vehicle["FUEL TYPE"],
        "registration_date": vehicle["REGISTRATION DATE"]
    }