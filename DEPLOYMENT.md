# 🚀 Deployment Guide

This guide provides instructions for deploying the Hospital Intelligence API to production.

---

## 📋 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed for security issues
- [ ] No `.env` files with secrets
- [ ] Dependencies updated and tested
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] Security scan completed (bandit, safety)
- [ ] Performance testing completed

---

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create .dockerignore

```
__pycache__
.git
.gitignore
.env
venv/
.venv/
.DS_Store
*.pyc
*.pyo
*.pyd
.pytest_cache
.coverage
dist/
build/
*.egg-info/
```

### 3. Build Docker Image

```bash
docker build -t hospital-api:1.0 .
```

### 4. Run Docker Container

```bash
docker run -d \
  --name hospital-api \
  -p 8000:8000 \
  -e MODEL_VERSION=v1.0 \
  -e ENVIRONMENT=production \
  -v /data/logs:/app/logs \
  hospital-api:1.0
```

### 5. Push to Registry

```bash
# Tag image
docker tag hospital-api:1.0 myregistry.azurecr.io/hospital-api:1.0

# Login to registry
docker login myregistry.azurecr.io

# Push image
docker push myregistry.azurecr.io/hospital-api:1.0
```

---

## ☸️ Kubernetes Deployment

### 1. Create Deployment YAML

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hospital-api
  labels:
    app: hospital-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hospital-api
  template:
    metadata:
      labels:
        app: hospital-api
    spec:
      containers:
      - name: hospital-api
        image: myregistry.azurecr.io/hospital-api:1.0
        ports:
        - containerPort: 8000
        env:
        - name: MODEL_VERSION
          value: "v1.0"
        - name: ENVIRONMENT
          value: "production"
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: hospital-api-service
spec:
  selector:
    app: hospital-api
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### 2. Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check status
kubectl get deployments

# View pods
kubectl get pods

# View service
kubectl get service hospital-api-service
```

---

## 🌐 Cloud Platform Deployments

### Azure App Service

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create App Service plan
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

# Create web app
az webapp create --resource-group myResourceGroup \
  --plan myAppServicePlan --name hospital-api \
  --deployment-container-image-name myregistry.azurecr.io/hospital-api:1.0

# Configure environment variables
az webapp config appsettings set --resource-group myResourceGroup \
  --name hospital-api \
  --settings MODEL_VERSION=v1.0 ENVIRONMENT=production
```

### AWS Elastic Beanstalk

```bash
# Create application
eb init -p "Python 3.9" hospital-api

# Create environment
eb create hospital-api-prod

# Deploy
eb deploy

# View logs
eb logs
```

### Google Cloud Run

```bash
# Build image
gcloud builds submit --tag gcr.io/MY_PROJECT/hospital-api

# Deploy to Cloud Run
gcloud run deploy hospital-api \
  --image gcr.io/MY_PROJECT/hospital-api \
  --platform managed \
  --region us-central1
```

---

## 🔄 Continuous Integration/Deployment (CI/CD)

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest safety bandit
    
    - name: Run security checks
      run: |
        bandit -r app.py
        safety check
    
    - name: Run tests
      run: pytest tests/ -v
    
    - name: Build Docker image
      run: docker build -t hospital-api:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }}
        docker push myregistry/hospital-api:${{ github.sha }}
    
    - name: Deploy to production
      run: |
        # Your deployment command
        kubectl set image deployment/hospital-api \
          hospital-api=myregistry/hospital-api:${{ github.sha }}
```

---

## 🔒 Production Configuration

### Environment Variables

```bash
# Create .env file (DO NOT COMMIT)
MODEL_VERSION=v1.0
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
LOG_FILE=/var/log/hospital-api/predictions.jsonl
LOG_LEVEL=ERROR
CORS_ORIGINS=https://yourdomain.com
```

### Reverse Proxy (nginx)

```nginx
# /etc/nginx/sites-available/hospital-api
upstream hospital_api {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name api.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://hospital_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting
        limit_req zone=api burst=10 nodelay;
    }
    
    # Rate limiting zone
    limit_req_zone $binary_remote_addr zone=api:10m rate=5r/s;
}
```

---

## 📊 Monitoring & Logging

### Application Monitoring

```bash
# Monitor logs
tail -f /var/log/hospital-api/predictions.jsonl | jq .

# Count predictions per hour
jq 'select(.timestamp > "2026-02-19T00:00:00") | .endpoint' \
  /var/log/hospital-api/predictions.jsonl | sort | uniq -c
```

### Prometheus Metrics (Optional)

```python
from prometheus_client import Counter, Histogram, generate_latest
import time

prediction_counter = Counter(
    'predictions_total', 
    'Total predictions',
    ['endpoint', 'prediction']
)

prediction_duration = Histogram(
    'prediction_duration_seconds',
    'Prediction duration'
)

@app.post("/predict-risk")
def predict_risk(data: RiskInput):
    start = time.time()
    # ... prediction logic ...
    duration = time.time() - start
    
    prediction_counter.labels(endpoint='risk', prediction=prediction).inc()
    prediction_duration.observe(duration)
```

---

## 🆘 Rollback Procedures

### Docker/Kubernetes

```bash
# View deployment history
kubectl rollout history deployment/hospital-api

# Rollback to previous version
kubectl rollout undo deployment/hospital-api

# Rollback to specific revision
kubectl rollout undo deployment/hospital-api --to-revision=2
```

### Blue-Green Deployment

```bash
# Deploy new version alongside old (green)
kubectl create deployment hospital-api-green \
  --image=myregistry/hospital-api:new-version

# Test green deployment
# If successful, switch traffic
kubectl patch service hospital-api-service \
  -p '{"spec":{"selector":{"version":"green"}}}'

# If issues, switch back (blue)
kubectl patch service hospital-api-service \
  -p '{"spec":{"selector":{"version":"blue"}}}'
```

---

## 📈 Performance Tuning

### Gunicorn Workers

```bash
# Calculate optimal worker count: 2 x CPU cores + 1
# For 4 cores: 2 x 4 + 1 = 9 workers

gunicorn app:app \
  --workers 9 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Load Testing

```bash
# Using Apache Bench
ab -n 10000 -c 100 http://localhost:8000/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health
```

---

## 📝 Deployment Verification

```bash
# Health check
curl -X GET http://localhost:8000/health

# Test risk prediction
curl -X POST http://localhost:8000/predict-risk \
  -H "Content-Type: application/json" \
  -d '{"age":45,"length_of_stay_hours":12,"patient_visit_count":3,"department":"Cardiology","gender":"Male"}'

# Check logs
tail -f logs/prediction_logs.jsonl | jq .
```

---

## 🔔 Post-Deployment

1. **Monitoring**: Set up alerts for errors, latency
2. **Backup**: Schedule regular backups of models and logs
3. **Documentation**: Update deployment runbook
4. **Communication**: Notify stakeholders of deployment
5. **Analytics**: Track usage and performance metrics

---

**Last Updated**: February 2026
