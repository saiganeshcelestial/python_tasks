from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Boolean, Enum as SAEnum,
    DateTime, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from database import Base
from models.enums import UserRole, LoanPurpose, EmploymentStatus, LoanStatus


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "loanhub"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    monthly_income = Column(Integer, nullable=False)
    role = Column(SAEnum(UserRole), nullable=False, default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utcnow)

    loans = relationship("Loan", back_populates="applicant")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"


class Loan(Base):
    __tablename__ = "loans"
    __table_args__ = {"schema": "loanhub"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("loanhub.users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    purpose = Column(SAEnum(LoanPurpose), nullable=False)
    tenure_months = Column(Integer, nullable=False)
    employment_status = Column(SAEnum(EmploymentStatus), nullable=False)
    status = Column(SAEnum(LoanStatus), nullable=False, default=LoanStatus.pending)
    admin_remarks = Column(Text, nullable=True)
    reviewed_by = Column(String(50), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    applied_at = Column(DateTime(timezone=True), default=utcnow)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    credit_score = Column(Integer, nullable=True)

    applicant = relationship("User", back_populates="loans")

    def __repr__(self):
        return f"<Loan id={self.id} user_id={self.user_id} amount={self.amount} status={self.status}>"
