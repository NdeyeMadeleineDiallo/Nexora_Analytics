from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="Nexora Analytics API",
    description="API de prédiction pour la segmentation client",
    version="1.0"
)

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "kmeans_customer_segmentation_v1.pkl"

kmeans_model = joblib.load(MODEL_PATH)


@app.get("/")
def home():
    return {
        "message": "Bienvenue sur l'API Nexora Analytics",
        "status": "API opérationnelle"
    }


@app.post("/predict-segment")
def predict_segment(data: dict):
    input_df = pd.DataFrame([data])

    prediction = kmeans_model.predict(input_df)

    return {
        "segment_cluster": int(prediction[0])
    }