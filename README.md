# 🏥 Healthcare AI/ML Capstone Project
## Hospital Intelligence System - IITM Weekend Certification

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Project Overview

This capstone project develops an **AI-powered hospital intelligence system** that leverages machine learning to enhance operational efficiency and financial decision-making in healthcare settings. The system consists of two production-ready predictive models deployed via a scalable REST API.

### 🎯 Problem Statement
Hospitals face challenges in:
- **Operational Planning**: Predicting patient visit risk levels for resource allocation
- **Financial Optimization**: Forecasting claim outcomes to reduce revenue leakage and improve cash flow

### 💡 Solution
A machine learning-based decision support system that provides real-time predictions to enable:
- Proactive operational planning and resource management
- Reduced financial uncertainty and improved revenue forecasting

---

## 🔬 Technical Architecture

### Models Deployed

| Model | Purpose | Output | Use Case |
|-------|---------|--------|----------|
| **Visit Risk Classifier** | Predict patient visit risk level | Low / Medium / High | Hospital capacity planning |
| **Claim Outcome Predictor** | Forecast claim approval status | Paid / Pending / Rejected | Revenue cycle management |

### Technology Stack

```
Backend:        FastAPI, Uvicorn
ML Framework:   scikit-learn, pandas
Validation:     Pydantic
Model Serving:  joblib (pickle format)
Logging:        JSONL (structured logs)
```

---

## 📁 Project Structure

```
IITM_Capstone-AI_ML-Project/
│
├── 📓 capstone_phase1.ipynb          # Phase 1: Problem Definition & EDA
├── 📓 capstone_phase2.ipynb          # Phase 2: Feature Engineering
├── 📓 capstone_phase3.ipynb          # Phase 3: Model Development & Selection
├── 📓 capstone_phase4.ipynb          # Phase 4: Model Evaluation & Optimization
├── 📓 Healthcare_Capstone.ipynb      # Comprehensive Project Notebook
│
├── phase5_deployment/
│   └── hospital_api/                 # Production FastAPI Application
│       ├── app.py                    # API endpoints & server logic
│       ├── requirements.txt          # Python dependencies
│       ├── README.md                 # API documentation
│       ├── models/                   # Trained ML models (v1)
│       ├── utils/                    # Validation schemas
│       └── logs/                     # Prediction audit trail
│
├── README.md                         # This file
└── .gitignore                        # Git configuration
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- 2GB RAM minimum (for model loading)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/IITM-Capstone-AI_ML-Project.git
   cd IITM-Capstone-AI_ML-Project
   ```

2. **Navigate to deployment folder**
   ```bash
   cd phase5_deployment/hospital_api
   ```

3. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the API server**
   ```bash
   python -m uvicorn app:app --reload
   ```

6. **Access the API**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

---

## 📊 API Endpoints

### 1. Health Check
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

### 2. Risk Prediction
```
POST /predict-risk
```
**Request Body:**
```json
{
  "age": 45,
  "length_of_stay_hours": 12,
  "patient_visit_count": 3,
  "department": "Cardiology",
  "gender": "Male"
}
```
**Response:**
```json
{
  "prediction": "Low",
  "probability": 0.4979,
  "model_version": "v1.0"
}
```

### 3. Claim Prediction
```
POST /predict-claim
```
**Request Body:**
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
**Response:**
```json
{
  "prediction": "Paid",
  "probability": 0.5974,
  "model_version": "v1.0"
}
```

---

## 📈 Project Phases

| Phase | Focus | Deliverable |
|-------|-------|-------------|
| **Phase 1** | Problem Definition, EDA | Dataset analysis, insights |
| **Phase 2** | Feature Engineering | Feature transformations, selection |
| **Phase 3** | Model Development | Multiple model prototypes |
| **Phase 4** | Evaluation & Optimization | Best-performing models, tuning |
| **Phase 5** | Production Deployment | FastAPI service, REST endpoints |

---

## 🔍 Key Features

✅ **Production-Ready API**
- Type-safe input validation using Pydantic
- Comprehensive error handling
- JSONL audit trail for predictions

✅ **Scalable Architecture**
- RESTful API design
- Model versioning capability
- Structured logging for monitoring

✅ **ML Best Practices**
- Feature engineering pipeline
- Train/test split validation
- Cross-validation for model selection
- Probability scores for decision thresholds

✅ **Security**
- No hardcoded secrets or credentials
- Input validation and schema enforcement
- Clean logging without PII exposure

---

## 📚 Documentation

- [API Documentation](phase5_deployment/hospital_api/README.md) - Detailed API setup and usage
- [Architecture](ARCHITECTURE.md) - System design and components
- [Contributing Guidelines](CONTRIBUTING.md) - Contribution guidelines

---

## 💻 Usage Examples

### Python Example
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Risk Prediction
risk_payload = {
    "age": 45,
    "length_of_stay_hours": 12,
    "patient_visit_count": 3,
    "department": "Cardiology",
    "gender": "Male"
}

response = requests.post(f"{BASE_URL}/predict-risk", json=risk_payload)
print(json.dumps(response.json(), indent=2))
```

### cURL Example
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

---

## 🎓 Learning Outcomes

This project demonstrates expertise in:

- **Data Science**: EDA, feature engineering, model selection
- **Machine Learning**: Classification algorithms, model evaluation
- **Software Engineering**: API design, deployment, logging
- **DevOps**: Environment setup, dependency management, version control

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Certificate

Completed as part of **IITM Weekend Certification Course** - AI/ML Specialization (11 months)

---

## ✉️ Contact & Social

- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- **GitHub**: [Your GitHub Profile](https://github.com/yourusername)

---

## 📝 Notes

- All data in this project is **synthetic test data** suitable for demonstration
- Models are provided as pickled scikit-learn objects for quick deployment
- Prediction logs are stored in JSONL format for easy parsing and monitoring

---

**Built with ❤️ as an IITM Capstone Project**
