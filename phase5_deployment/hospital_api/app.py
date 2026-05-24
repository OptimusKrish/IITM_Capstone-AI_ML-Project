from fastapi import FastAPI, HTTPException
from utils.schema_validation import RiskInput, ClaimInput
import joblib
import pandas as pd
import json
from datetime import datetime

# -----------------------------
# Logging Setup
# -----------------------------

LOG_FILE = "./logs/prediction_logs.jsonl"

def log_prediction(endpoint, input_data, prediction, probability):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "model_version": MODEL_VERSION,
        "input": input_data,
        "prediction": prediction,
        "probability": probability
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(
    title="Hospital Intelligence API - IITM Capstone",
    version="1.0"
)

# -----------------------------
# Load the pre-trained models
# -----------------------------
risk_model = joblib.load("./models/risk_model_v1.pkl")
risk_features = joblib.load("./models/risk_model_features.pkl")

claim_model = joblib.load("./models/claim_model_v1.pkl")
claim_features = joblib.load("./models/claim_model_features.pkl")

MODEL_VERSION = "v1.0"

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": 200,
        "message": "Service is up and Running",
        "model_version": MODEL_VERSION
    }

# -----------------------------
# Risk Prediction
# -----------------------------
@app.post("/predict-risk")
def predict_risk(data: RiskInput):
    try:
        df = pd.DataFrame([data.dict()])
        df = pd.get_dummies(df)
        df = df.reindex(columns=risk_features, fill_value=0)

        prediction = risk_model.predict(df)[0]
        probability = max(risk_model.predict_proba(df)[0])
        log_prediction("risk", data.dict(), prediction, float(probability))


        return {
            "prediction": prediction,
            "probability": round(float(probability), 4),
            "model_version": MODEL_VERSION
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# Claim Prediction
# -----------------------------
@app.post("/predict-claim")
def predict_claim(data: ClaimInput):
    try:
        df = pd.DataFrame([data.dict()])
        df = pd.get_dummies(df)
        df = df.reindex(columns=claim_features, fill_value=0)

        prediction = claim_model.predict(df)[0]
        probability = max(claim_model.predict_proba(df)[0])
        log_prediction("claim", data.dict(), prediction, float(probability))

        return {
            "prediction": prediction,
            "probability": round(float(probability), 4),
            "model_version": MODEL_VERSION
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
