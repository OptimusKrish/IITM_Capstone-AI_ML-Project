# Contributing Guidelines

Thank you for your interest in this IITM Capstone project! This document provides guidelines for contributing.

## 📋 Project Status

This is an **educational capstone project** showcasing:
- Machine Learning model development and deployment
- RESTful API design
- Production-ready code practices

## 🤝 How to Contribute

### Report Bugs or Issues
1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)

### Suggest Enhancements
- Open an issue labeled "enhancement"
- Describe the feature and use case
- Explain the expected impact

### Submit Code Changes
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make changes following the code style guide
4. Write or update tests if applicable
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request with detailed description

## 📝 Commit Message Format

```
[TYPE] Brief description (50 chars max)

Longer explanation if needed, wrapped at 72 characters.
Include references to related issues: Fixes #123

- Detail 1
- Detail 2
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

## 🎨 Code Style

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Type hints for clarity
- Max line length: 88 characters

```python
def predict_risk(data: RiskInput) -> dict:
    """
    Predict patient visit risk level.
    
    Args:
        data: RiskInput with patient information
        
    Returns:
        Dictionary with prediction and probability
    """
    # Implementation
```

### File Organization
```
app.py              # Main application
utils/
  ├── schema_validation.py
  └── helpers.py

models/
  ├── risk_model_v1.pkl
  └── claim_model_v1.pkl

logs/
  └── prediction_logs.jsonl

tests/
  ├── test_api.py
  └── test_validation.py
```

## 🧪 Testing

### Running Tests
```bash
# If tests are added
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov  # With coverage
```

### Test Coverage
- Aim for 80%+ coverage
- Test edge cases
- Test error conditions

### Example Test
```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == 200
```

## 📚 Documentation

### Update Documentation When
- Adding new endpoints
- Changing input/output formats
- Adding new features
- Fixing bugs
- Improving clarity

### Documentation Locations
- **API**: `phase5_deployment/hospital_api/README.md`
- **Architecture**: `ARCHITECTURE.md`
- **Project Overview**: Root `README.md`

## 🔒 Security Considerations

### Before Submitting
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] No PII or sensitive data in files
- [ ] No credentials in `.env` files (use `.env.example`)
- [ ] Review dependencies for vulnerabilities

### Secure Coding
```python
# ❌ DON'T
API_KEY = "sk-1234567890abcdef"
PASSWORD = "mypassword123"

# ✅ DO
import os
API_KEY = os.getenv("API_KEY")
PASSWORD = os.getenv("PASSWORD")
```

## 🚀 Deployment

### Prerequisites for Merging
1. Code passes all tests
2. Documentation is updated
3. No security issues
4. Clear commit history

### After Merge
- Changes will be reflected in main branch
- For production deployment, create a release tag

## 📞 Communication

- **Questions**: Open an issue with `[question]` label
- **Discussions**: Use GitHub Discussions
- **Code Review**: Be respectful and constructive

## 🏆 Recognition

Contributors will be recognized in the project README under the "Contributors" section.

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 📖 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

---

**Questions?** Open an issue or start a discussion!

Thank you for contributing! 🙏
