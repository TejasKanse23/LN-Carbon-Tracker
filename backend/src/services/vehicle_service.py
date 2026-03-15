import pandas as pd

def get_vehicle_details(vehicle_number):

    df = pd.read_excel("data/raw/vehicle_dataset_20_rows.xlsx")
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