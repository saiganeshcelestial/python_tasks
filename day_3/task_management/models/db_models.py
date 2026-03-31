from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "task_management"}
    id         = Column(Integer, primary_key=True, autoincrement=True)
    username   = Column(String(100), unique=True, nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active  = Column(Integer, default=1)  # 1 for active, 0 for inactive
    # One-to-many: a user owns many tasks
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        # Intentionally omits password
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": "task_management"}
    id          = Column(Integer, primary_key=True, autoincrement=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(String(50), default="pending")
    priority    = Column(String(50), default="medium")
    owner_id    = Column(Integer, ForeignKey("task_management.users.id"), nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return (
            f"<Task(id={self.id}, title='{self.title}', "
            f"status='{self.status}', priority='{self.priority}')>"
        )
