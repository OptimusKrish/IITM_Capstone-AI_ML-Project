# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATIONS                      │
│         (Web, Mobile, Hospital Systems, Analytics)          │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP/REST
                         │
         ┌───────────────┴───────────────┐
         │                               │
    ┌────▼─────────────────────────────┐ │
    │    FastAPI Application Server    │ │
    │    (app.py - Uvicorn)            │ │
    │                                  │ │
    │  ┌──────────────────────────────┐│ │
    │  │  /predict-risk endpoint      ││ │
    │  │  - Input validation          ││ │
    │  │  - Feature preprocessing     ││ │
    │  │  - Model inference           ││ │
    │  │  - Response formatting       ││ │
    │  └──────────────────────────────┘│ │
    │                                  │ │
    │  ┌──────────────────────────────┐│ │
    │  │  /predict-claim endpoint     ││ │
    │  │  - Input validation          ││ │
    │  │  - Feature preprocessing     ││ │
    │  │  - Model inference           ││ │
    │  │  - Response formatting       ││ │
    │  └──────────────────────────────┘│ │
    │                                  │ │
    │  ┌──────────────────────────────┐│ │
    │  │  Logging Module              ││ │
    │  │  - Audit trail generation    ││ │
    │  │  - JSONL format logging      ││ │
    │  └──────────────────────────────┘│ │
    └────┬─────────────────────────────┘ │
         │                               │
         ├───────────────────────────────┘
         │
         ├──────────────────────────────────┐
         │                                  │
    ┌────▼──────────────┐  ┌──────────────┴────┐
    │   Models Module   │  │  Utils Module      │
    │                  │  │  (Validation)      │
    ├──────────────────┤  │                    │
    │• risk_model_v1   │  │• RiskInput schema  │
    │• claim_model_v1  │  │• ClaimInput schema │
    │• Feature schemas │  │• Error handling    │
    └────────┬─────────┘  └────────────────────┘
             │
        ┌────▼───────────────────────┐
        │   Trained ML Models        │
        │  (scikit-learn objects)    │
        │                            │
        │• Classification Classifier │
        │• Feature transformers      │
        │• Encoders/Scalers          │
        └────────────────────────────┘
```

---

## Component Details

### 1. **API Layer (FastAPI)**
- **Technology**: FastAPI + Uvicorn
- **Purpose**: RESTful interface for model predictions
- **Features**:
  - Automatic Swagger documentation
  - Async request handling
  - Type validation via Pydantic
  - Built-in CORS support

### 2. **Validation Layer (Pydantic)**
- **File**: `utils/schema_validation.py`
- **Components**:
  - `RiskInput`: Validates risk prediction requests
  - `ClaimInput`: Validates claim prediction requests
- **Purpose**: Type-safe input validation

### 3. **Model Layer**
- **Location**: `models/` directory
- **Models**:
  - `risk_model_v1.pkl`: Classification model for risk levels
  - `claim_model_v1.pkl`: Classification model for claim outcomes
- **Format**: Pickled scikit-learn estimators
- **Features**: Pre-trained on historical hospital data

### 4. **Feature Engineering**
- **Stored**: `risk_model_features.pkl` and `claim_model_features.pkl`
- **Process**:
  - Feature list from training set
  - One-hot encoding support via `pd.get_dummies()`
  - Column alignment with training schema

### 5. **Logging System**
- **Format**: JSONL (JSON Lines)
- **Location**: `logs/prediction_logs.jsonl`
- **Logged Data**:
  - Timestamp
  - Endpoint called
  - Input data
  - Prediction result
  - Confidence probability

---

## Data Flow

### Risk Prediction Flow
```
Client Request
    ↓
FastAPI Endpoint (/predict-risk)
    ↓
Input Validation (Pydantic)
    ↓
Convert to DataFrame
    ↓
One-Hot Encoding
    ↓
Feature Alignment
    ↓
Risk Model Inference
    ↓
Generate Probability
    ↓
Log Prediction (JSONL)
    ↓
Return JSON Response
```

### Claim Prediction Flow
```
Client Request
    ↓
FastAPI Endpoint (/predict-claim)
    ↓
Input Validation (Pydantic)
    ↓
Convert to DataFrame
    ↓
One-Hot Encoding
    ↓
Feature Alignment
    ↓
Claim Model Inference
    ↓
Generate Probability
    ↓
Log Prediction (JSONL)
    ↓
Return JSON Response
```

---

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | FastAPI | 0.95+ | API endpoints & routing |
| ASGI Server | Uvicorn | Latest | Server runtime |
| ML Framework | scikit-learn | 1.0+ | Model predictions |
| Data Processing | pandas | 1.3+ | Feature transformations |
| Validation | Pydantic | 2.0+ | Input/output schemas |
| Model Format | joblib | Latest | Model serialization |
| Python | Python | 3.8+ | Runtime |

---

## Scalability Considerations

### Current Architecture
- **Single Instance**: Suitable for development and small deployments
- **Model Loading**: Done once on startup
- **Request Handling**: Async processing via Uvicorn workers

### Production Scaling

#### Option 1: Docker Containerization
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

#### Option 2: Load Balancing
```
Load Balancer (nginx)
    ↓
Gunicorn (multiple workers)
    ↓
Uvicorn instances
```

#### Option 3: Kubernetes Deployment
- Container orchestration
- Auto-scaling based on load
- Health checks and monitoring

---

## Security Architecture

### Input Security
- ✅ Pydantic validation prevents injection attacks
- ✅ Type hints ensure data integrity
- ✅ Range validation on numeric inputs

### Model Security
- ✅ Models loaded from trusted local files
- ✅ No model downloading from untrusted sources
- ✅ Model versioning for auditability

### API Security
- ✅ No secrets in environment
- ✅ Error messages don't expose internal details
- ✅ Logging doesn't store sensitive PII

### Deployment Security
- ✅ Run as non-root user in containers
- ✅ Use environment variables for configuration
- ✅ Implement rate limiting in production
- ✅ Enable CORS only for trusted origins

---

## Monitoring & Observability

### Application Health
- **Endpoint**: `GET /health`
- **Purpose**: Load balancer health checks
- **Response**: JSON status object

### Prediction Logging
- **Format**: Structured JSON Lines
- **Usage**: Performance monitoring, auditing
- **Analytics**: Can be parsed for business intelligence

### Future Enhancements
- Prometheus metrics
- ELK Stack integration
- Distributed tracing
- Performance profiling

---

## Model Management

### Model Versioning Strategy
```
Phase 1: Models as v1
Phase 2: Retrain → v2
Phase 3: A/B Testing between versions
Phase 4: Production rollout
```

### Model Performance Tracking
```json
{
  "model_id": "risk_model_v1",
  "accuracy": 0.87,
  "precision": 0.85,
  "recall": 0.89,
  "f1_score": 0.87,
  "deployment_date": "2026-02-15"
}
```

---

## Error Handling

### Application-Level Errors
```python
# Handled by FastAPI
- 400: Bad Request (validation error)
- 404: Not Found (endpoint doesn't exist)
- 500: Internal Server Error (exception in model)
```

### Logging Errors
```python
# All exceptions logged with context
log_entry = {
    "timestamp": "...",
    "error_type": "ValueError",
    "error_message": "...",
    "endpoint": "/predict-risk",
    "status": "failed"
}
```

---

## Deployment Checklist

- [ ] Review code for secrets
- [ ] Update requirements.txt with versions
- [ ] Create `.env.example` template
- [ ] Set up logging directory permissions
- [ ] Configure CORS for production domain
- [ ] Set up monitoring/alerting
- [ ] Create Docker image
- [ ] Test with production data volume
- [ ] Document deployment procedure
- [ ] Set up backup/recovery procedures

---

## Future Enhancements

1. **Model Improvements**
   - Retrain with more recent data
   - Implement ensemble methods
   - Add feature importance explanations

2. **API Enhancements**
   - Batch prediction endpoint
   - Model explanation via SHAP
   - Confidence interval predictions

3. **Infrastructure**
   - Database for prediction history
   - Caching layer (Redis)
   - Message queue for async tasks

4. **Monitoring**
   - Real-time performance dashboards
   - Drift detection
   - Automated retraining triggers

---

**Last Updated**: February 2026  
**Architecture Version**: 1.0
