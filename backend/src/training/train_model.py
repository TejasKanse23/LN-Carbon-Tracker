import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load data
df = pd.read_excel("data/raw/5000 lanes shipments.xlsx")

# Target
y = df["estimated_emissions_kg_co2e"]

# Features
X = df.drop(columns=["estimated_emissions_kg_co2e", "shipment_id", "date"])

categorical_cols = [
    "origin",
    "destination",
    "lane",
    "vehicle_type",
    "fuel_type",
    "traffic congestion"
]

numeric_cols = [c for c in X.columns if c not in categorical_cols]

# Preprocessing
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
    ("num", "passthrough", numeric_cols)
])

# Model
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

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
pred = pipeline.predict(X_test)

print("MAE:", mean_absolute_error(y_test, pred))
print("R2:", r2_score(y_test, pred))

# Save model
joblib.dump(pipeline, "carbon_emission_model.pkl")

print("Model saved as carbon_emission_model.pkl")