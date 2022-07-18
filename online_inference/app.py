from fastapi import FastAPI
from models.models import Item
from core.functions import get_file_from_s3
import numpy as np
import joblib
from pathlib import Path
from dataclasses import dataclass, astuple


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return 200


@app.post("/predict")
async def predict(row: Item):
    model_path = Path('tmp/estimator.pkl')
    if model_path.is_file():
        model = joblib.load(model_path)
        data = np.array([[
            row.age,
            row.sex,
            row.cp,
            row.trestbps,
            row.chol,
            row.fbs,
            row.restecg,
            row.thalach,
            row.exang,
            row.oldpeak,
            row.slope,
            row.ca,
            row.thal,
        ]])
        predict = model.predict(data)
        return {"message": f"result: {predict[0]}"}
    else:
        return {"message": f"error"}


@app.on_event('startup')
def load_model():
    try:
        get_file_from_s3('estimator.pkl')
    except:
        pass