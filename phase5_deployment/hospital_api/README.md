# 🏥 Hospital Intelligence API  
### FastAPI Deployment – Production-Ready ML Models

A RESTful API service that deploys two machine learning models for hospital operational and financial decision-making using **FastAPI** and **scikit-learn**.

---

## 🎯 Purpose

This API provides real-time predictions to support:
- **Operational Planning**: Visit risk assessment for resource allocation
- **Financial Management**: Claim outcome forecasting to reduce revenue leakage

---

## 🔹 Models Deployed

### 1. Visit Risk Classification Model
- **Input**: Patient demographics & visit characteristics
- **Output**: Risk Level (Low / Medium / High)
- **Features**: Age, length of stay, visit count, department, gender
- **Use Case**: Hospital capacity planning and resource allocation

### 2. Claim Outcome Prediction Model
- **Input**: Patient & claim characteristics
- **Output**: Claim Status (Paid / Pending / Rejected)
- **Features**: Age, LOS, department, insurance provider, risk category, visit count
- **Use Case**: Revenue cycle optimization and financial forecasting

---

## 📂 Project Structure

```
hospital_api/
│
├── app.py                          # FastAPI application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── models/                         # Pre-trained ML models
│   ├── risk_model_v1.pkl          # Risk classification model (joblib)
│   ├── risk_model_features.pkl    # Risk model feature schema
│   ├── claim_model_v1.pkl         # Claim prediction model (joblib)
│   └── claim_model_features.pkl   # Claim model feature schema
│
├── logs/                           # Audit trail
│   └── prediction_logs.jsonl      # Structured prediction logs
│
├── utils/                          # Utility modules
│   └── schema_validation.py       # Pydantic validation schemas
│
└── venv/                           # Python virtual environment (ignored in git)
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+
- pip or conda
- ~2GB disk space for models

### 1️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the API Server

```bash
python -m uvicorn app:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 4️⃣ Access API Documentation

- **Swagger UI (Interactive)**: http://localhost:8000/docs
- **ReDoc (Documentation)**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### ✅ Health Check
```
GET /health
```

**Response:**
```json
{
  "status": 200,
  "message": "Service is up and Running",
  "model_version": "v1.0"
}
```

---

### 🔴 Risk Prediction
```
POST /predict-risk
```

**Request Example:**
```json
{
  "age": 45,
  "length_of_stay_hours": 12,
  "patient_visit_count": 3,
  "department": "Cardiology",
  "gender": "Male"
}
```

**Response Example:**
```json
{
  "prediction": "Low",
  "probability": 0.4979,
  "model_version": "v1.0"
}
```

**Supported Departments:**
- Cardiology, Neurology, Orthopedics, Oncology, Emergency, ICU, etc.

---

### 💰 Claim Prediction
```
POST /predict-claim
```

**Request Example:**
```json
{
  "age": 50,
  "length_of_stay_hours": 20,
  "department": "Orthopedics",
  "insurance_provider": "Provider A",
  "risk_category": "High",
  "patient_visit_count": 2
}
```

**Response Example:**
```json
{
  "prediction": "Paid",
  "probability": 0.5974,
  "model_version": "v1.0"
}
```

---

## 💻 Usage Examples

### Python Requests
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Risk Prediction
risk_data = {
    "age": 45,
    "length_of_stay_hours": 12,
    "patient_visit_count": 3,
    "department": "Cardiology",
    "gender": "Male"
}

response = requests.post(f"{BASE_URL}/predict-risk", json=risk_data)
print(json.dumps(response.json(), indent=2))
```

### cURL
```bash
curl -X POST "http://localhost:8000/predict-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "length_of_stay_hours": 12,
    "patient_visit_count": 3,
    "department": "Cardiology",
    "gender": "Male"
  }'
```

### JavaScript/Fetch
```javascript
const BASE_URL = "http://localhost:8000";

const riskData = {
  age: 45,
  length_of_stay_hours: 12,
  patient_visit_count: 3,
  department: "Cardiology",
  gender: "Male"
};

fetch(`${BASE_URL}/predict-risk`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(riskData)
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 📊 Logging

All predictions are logged to `logs/prediction_logs.jsonl` in the following format:

```json
{
  "timestamp": "2026-02-19T14:35:00.570163",
  "endpoint": "claim",
  "model_version": "v1.0",
  "input": { ... },
  "prediction": "Paid",
  "probability": 0.4826585348558038
}
```

**Use Cases for Logs:**
- Audit trail for compliance
- Model performance monitoring
- Debugging and troubleshooting
- Business analytics

---

## 🔒 Security & Best Practices

✅ **Input Validation**: All requests validated with Pydantic  
✅ **Error Handling**: Graceful error messages  
✅ **No Secrets**: No API keys or credentials in code  
✅ **Structured Logging**: Non-sensitive data only  

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Use a different port
python -m uvicorn app:app --port 8001
```

### Model Loading Error
```bash
# Ensure models are in correct location
ls models/  # Verify models exist
pip install joblib scikit-learn pandas
```

### Module Import Error
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📈 Performance Notes

- **Prediction Latency**: ~50-100ms per request
- **Memory Usage**: ~500MB when fully loaded
- **Throughput**: ~100+ predictions/second on standard hardware

---

## 🔄 Model Versioning

Models follow semantic versioning:
- `risk_model_v1.pkl` - Production risk model v1
- `claim_model_v1.pkl` - Production claim model v1

Future versions will be `v2`, `v3`, etc.

---

## 📝 Environment Variables (Optional)

Create a `.env` file for production configuration:

```env
LOG_FILE=./logs/prediction_logs.jsonl
MODEL_VERSION=v1.0
```

See `.env.example` for all available options.

---

## 🚀 Production Deployment

For production, consider:
- Using `gunicorn` with multiple workers
- Running behind a reverse proxy (nginx)
- Implementing API authentication
- Setting up monitoring/alerting

Example with Gunicorn:
```bash
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 📞 Support

For issues or questions, refer to the main project [README](../../README.md) or open an issue on GitHub.

---

**Part of IITM AI/ML Capstone Project**
  "prediction": "Paid",
  "probability": 0.5975,
  "model_version": "v1.0"
}

### Monitoring & Logging
/logs/prediction_logs.jsonl

> Each log entry includes:
Timestamp
Endpoint used
Model version
Input payload
Prediction
Probability

### Model Information
##### Visit Risk Model

- Algorithm: Random Forest

- Primary Metric: High Risk Recall

- Objective: Improve ICU & resource planning

##### Claim Outcome Model

- Algorithm: Random Forest

- Primary Metric: Rejected Recall

- Objective: Protect hospital revenue

### Governance & Versioning

- Model version embedded in API response

- Feature schema saved with each model

- Time-based train/test split used

- Leakage prevention implemented

- Prediction logging enabled

### Retraining Strategy

- Retrain quarterly

- Retrain if recall drops >10%

- Retrain if feature drift exceeds 20%

- Monitor rejected claim recall monthly

### Troubleshooting

##### If uvicorn is not recognized:

python -m uvicorn app:app --reload


##### If dependency issues occur:

pip install --upgrade pip
pip install -r requirements.txt

### Production Recommendations

##### For production deployment:

- Use Gunicorn with Uvicorn workers

- Add authentication & API keys

- Containerize using Docker

- Deploy on AWS / Azure / GCP

- Implement centralized logging (e.g., ELK stack)

### Business Impact

##### This API enables:

✔ Proactive high-risk patient management
✔ Reduced claim rejection rates
✔ Improved cash flow stability
✔ Operational predictability

##### ✅ Current Status

✔ Fully functional locally
✔ Version-controlled models
✔ Logging enabled
✔ Monitoring-ready
✔ Deployment-ready

