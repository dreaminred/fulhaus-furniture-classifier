from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import predict_pipeline
from app.model.model import __version__ as model_version

app = FastAPI()

class ImageIn(BaseModel):
    image: list

class PredictionOut(BaseModel):
    prediction: str

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}

@app.post("/predict", response_model=PredictionOut)
def predict(payload: ImageIn):
    prediction = predict_pipeline(payload.image)
    return {"prediction" : prediction}
