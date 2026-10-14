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
        "Live At:": "",
        "Interactive UI:": "",
        "Test Inputs:": "",
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
