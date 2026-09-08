from pydantic import BaseModel, Field
from typing import Literal


class LoanApplication(BaseModel):
    person_age: int = Field(..., ge=18, le=100)
    person_income: float = Field(..., gt=0)
    person_home_ownership: Literal["RENT", "OWN", "MORTGAGE", "OTHER"]
    person_emp_length: float = Field(..., ge=0, le=60)
    loan_intent: Literal["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
    loan_amnt: float = Field(..., gt=0)
    cb_person_default_on_file: Literal["Y", "N"]
    cb_person_cred_hist_length: int = Field(..., ge=0, le=60)


class UnderwritingResponse(BaseModel):
    default_probability: float
    risk_band: str
    assessment: str