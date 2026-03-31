# ============================================================
# Day-2 | Section D — Pydantic (Q12)
# Run: pip install pydantic
# ============================================================
from pydantic import BaseModel, field_validator, Field
from typing import Optional


class Address(BaseModel):
    street: str
    city: str
    zip_code: str

    @field_validator("zip_code")
    @classmethod
    def zip_must_be_6_digits(cls, v):
        if not v.isdigit() or len(v) != 6:
            raise ValueError("zip_code must be exactly 6 digits")
        return v


class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=8)
    age: int = Field(ge=18, le=120)
    address: Address

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v


class UserResponse(BaseModel):
    username: str
    email: str
    age: int
    address: Address
    # password is intentionally excluded


# Test Q12
data = {
    "username": "alice",
    "email": "alice@mail.com",
    "password": "securepass",
    "age": 25,
    "address": {"street": "MG Road", "city": "Bangalore", "zip_code": "560001"}
}

user = UserCreate(**data)
response = UserResponse(**user.model_dump())
print(response)
