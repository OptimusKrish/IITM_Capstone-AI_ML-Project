# Security Policy

## Security Overview

This project implements security best practices for a production-ready API:

### ✅ What's Implemented

1. **Input Validation**
   - All requests validated with Pydantic
   - Type checking prevents injection attacks
   - Numeric ranges enforced

2. **No Secrets in Code**
   - No API keys or credentials hardcoded
   - Use `.env` files for configuration (not committed)
   - `.env.example` provided as template

3. **Error Handling**
   - Graceful error messages
   - No internal details exposed
   - HTTP status codes properly set

4. **Logging Security**
   - No sensitive PII in logs
   - Structured JSON for parseability
   - Audit trail for compliance

### 🔒 Deployment Security

#### Environment Variables
```bash
# Use environment variables for configuration
export MODEL_VERSION=v1.0
export API_PORT=8000
export LOG_FILE=./logs/prediction_logs.jsonl
```

#### Docker Security
```dockerfile
# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser
```

#### Network Security
- Run behind reverse proxy (nginx/Apache)
- Enable HTTPS/TLS in production
- Configure CORS properly
- Implement rate limiting

#### API Authentication (Recommended)
For production, implement:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/predict-risk")
async def predict_risk(data: RiskInput, credentials: HTTPAuthCredentials = Depends(security)):
    # Validate token/credentials
    # Process request
```

### 🛡️ Dependency Security

#### Checking for Vulnerabilities
```bash
# Install safety
pip install safety

# Check dependencies
safety check

# Or use bandit for code analysis
pip install bandit
bandit -r .
```

#### Keeping Dependencies Updated
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all (cautiously)
pip install --upgrade -r requirements.txt
```

### 📋 Pre-Deployment Checklist

- [ ] Remove all `.env` files with secrets
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Review code for hardcoded credentials
- [ ] Run security scanners (bandit, safety)
- [ ] Enable CORS only for trusted origins
- [ ] Set `DEBUG = False` in production
- [ ] Enable HTTPS/TLS
- [ ] Set up rate limiting
- [ ] Configure logging appropriately
- [ ] Review model sources for tampering
- [ ] Set up monitoring and alerting
- [ ] Document security procedures

### 🚨 Incident Response

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. **DO NOT** commit a fix to public branch
3. **Email** the maintainers with details:
   - Vulnerability description
   - Impact assessment
   - Suggested fix (optional)

4. Allow time for patch development
5. Coordinate timing of public disclosure

### 📚 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [scikit-learn Model Security](https://scikit-learn.org/stable/modules/model_persistence.html)

### 🔐 Data Privacy

#### Input Data
- No PII storage in logs (use anonymized IDs)
- Minimize input field collection
- Clear data retention policy

#### Model Data
- Use synthetic data for testing
- Anonymize training data
- Document data lineage

#### GDPR Compliance (if applicable)
- Implement data deletion procedures
- Document data processing
- Obtain necessary consents
- Provide data export capability

### 📊 Security Audit Trail

All predictions are logged in `logs/prediction_logs.jsonl`:

```json
{
  "timestamp": "2026-02-19T14:35:00.570163",
  "endpoint": "/predict-claim",
  "model_version": "v1.0",
  "input": { /* anonymized data */ },
  "prediction": "Paid",
  "probability": 0.4826
}
```

**Use Cases:**
- Audit trail for compliance
- Detect anomalous patterns
- Performance monitoring
- Model debugging

### 🤝 Security Contributions

Found a security issue? Thank you!

1. Check existing [Security Advisories](../../security/advisories)
2. Review [Contributing Guidelines](../CONTRIBUTING.md)
3. Follow responsible disclosure practices
4. Contact maintainers privately

### 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-20 | Initial security policy |

---

**Last Updated**: February 2026  
**Policy Version**: 1.0
