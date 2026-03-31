import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, Field
from models.enums import UserRole, LoanPurpose, EmploymentStatus, LoanStatus


# ─── User Schemas ────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=8)
    phone: str
    monthly_income: int = Field(..., ge=0)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must contain only letters, numbers, and underscores.")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("Email must contain '@' and '.'")
        return v

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: str) -> str:
        if not re.match(r"^\d{10,15}$", v):
            raise ValueError("Phone must be 10–15 digits only.")
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone: str
    monthly_income: int
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Auth / Token Schemas ─────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    role: str


# ─── Loan Schemas ─────────────────────────────────────────────────────────────

class LoanCreate(BaseModel):
    amount: int = Field(..., gt=0, le=1_000_000)
    purpose: LoanPurpose
    tenure_months: int = Field(..., ge=6, le=360)
    employment_status: EmploymentStatus


class LoanReview(BaseModel):
    status: LoanStatus
    admin_remarks: str = Field(..., min_length=5, max_length=500)

    @field_validator("status")
    @classmethod
    def status_not_pending(cls, v: LoanStatus) -> LoanStatus:
        if v == LoanStatus.pending:
            raise ValueError("Review status must be 'approved' or 'rejected', not 'pending'.")
        return v


class LoanResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    purpose: LoanPurpose
    tenure_months: int
    employment_status: EmploymentStatus
    status: LoanStatus
    admin_remarks: Optional[str]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    applied_at: datetime
    updated_at: datetime
    credit_score: Optional[int]

    model_config = {"from_attributes": True}
