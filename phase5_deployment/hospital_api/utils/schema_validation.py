from pydantic import BaseModel

# -----------------------------
# Input Schemas
# -----------------------------
class RiskInput(BaseModel):
    age: int
    length_of_stay_hours: float
    patient_visit_count: int
    department: str
    gender: str

class ClaimInput(BaseModel):
    age: int
    length_of_stay_hours: float
    department: str
    insurance_provider: str
    risk_category: str
    patient_visit_count: int