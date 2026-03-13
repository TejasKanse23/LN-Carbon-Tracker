import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


# -------------------------
# Load Dataset
# -------------------------

df = pd.read_csv("data/raw/carbon_tracker_shipments.csv")


# -------------------------
# Feature Engineering
# -------------------------

df["ton_km"] = df["distance_km"] * df["weight_ton"]


# -------------------------
# Target
# -------------------------

y = df["estimated_emissions_kg_co2e"]


# -------------------------
# Features
# -------------------------

feature_cols = [
    "origin",
    "destination",
    "lane",
    "distance_km",
    "vehicle_type",
    "fuel_type",
    "weight_ton",
    "utilization_percent",
    "average_speed_kmph",
    "transit_time_hrs",
    "fuel_consumption_L",
    "co2_per_ton_km",
    "traffic congestion",
    "Age of vehicle",
    "Engine size ( Capacity of liters of fuel)",
    "ton_km"
]

X = df[feature_cols]


# -------------------------
# Column Types
# -------------------------

categorical_cols = [
    "origin",
    "destination",
    "lane",
    "vehicle_type",
    "fuel_type",
    "traffic congestion"
]

numeric_cols = [
    "distance_km",
    "weight_ton",
    "utilization_percent",
    "average_speed_kmph",
    "transit_time_hrs",
    "fuel_consumption_L",
    "co2_per_ton_km",
    "Age of vehicle",
    "Engine size ( Capacity of liters of fuel)",
    "ton_km"
]


# -------------------------
# Preprocessing
# -------------------------

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numeric_cols)
])


# -------------------------
# Model
# -------------------------

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", model)
])


# -------------------------
# Train/Test Split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -------------------------
# Train
# -------------------------

pipeline.fit(X_train, y_train)


# -------------------------
# Predictions
# -------------------------

pred = pipeline.predict(X_test)


# -------------------------
# Metrics
# -------------------------

mae = mean_absolute_error(y_test, pred)
rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)

# tolerance accuracy (within 10%)
tolerance = 0.10
accuracy = np.mean(np.abs((y_test - pred) / y_test) <= tolerance)


print("\nModel Evaluation")
print("----------------------------")
print("MAE:", mae)
print("RMSE:", rmse)
print("R2 Score:", r2)
print("Accuracy (within 10% error):", accuracy)


# -------------------------
# Save Model
# -------------------------

joblib.dump(pipeline, "models/carbon_emission_model2.pkl")

print("\nModel saved to models/carbon_emission_model2.pkl")