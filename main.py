from fastapi import FastAPI
from pydantic import BaseModel, field_validator
import joblib
import pandas as pd
import numpy as np


app = FastAPI()

model = joblib.load('XGBR.pkl')

class data(BaseModel):
    lag_1: float
    lag_7: float
    rolling_mean: float
    day_of_week: int
    month: int


@app.get("/")
def home():
    return {
        "System MSG:": "Retail Inventory Demand Forcasting API is Online",
        "Live At:": "https://ridf-api.onrender.com/",
        "Interactive UI:": "https://ridf-api.onrender.com/docs",
        "Test Inputs:": "https://docs.google.com/document/d/1nhm9JuDhZflT4w7vevUUQeOuSgHNpMAn38iXIr8bxM0/edit?usp=sharing",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}



@app.post("/predict")
def predict(payload: data):
    features = pd.DataFrame([payload.model_dump()])

    pred = model.predict(features)[0]
    pred_original = np.expm1(pred)
    return {
        "Predicted Quantity: ": float(pred_original),
        "Status" : "Success"
    }
