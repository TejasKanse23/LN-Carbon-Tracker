from fastapi import FastAPI
from ..inference.predict import predict

app = FastAPI()

@app.post("/predict-emission")
def predict_emission(data: dict):

    emission = predict(data)

    return {
        "predicted_emission_kg_co2e": emission
    }