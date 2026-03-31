"""
Tests for task endpoints.
Uses an in-memory SQLite DB so no real Supabase connection is needed.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# ── In-memory SQLite test engine ───────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Helpers ────────────────────────────────────────────────────────────────────
def create_test_user():
    resp = client.post("/users/", json={
        "username": "testuser",
        "email": "test@mail.com",
        "password": "secret",
    })
    assert resp.status_code == 201
    return resp.json()["id"]


# ── Tests ──────────────────────────────────────────────────────────────────────
def test_create_task():
    user_id = create_test_user()
    resp = client.post("/tasks/", json={
        "title": "Write tests",
        "status": "pending",
        "priority": "high",
        "owner_id": user_id,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Write tests"
    assert data["status"] == "pending"


def test_list_tasks():
    user_id = create_test_user()
    client.post("/tasks/", json={"title": "Task 1", "owner_id": user_id, "status": "pending", "priority": "low"})
    client.post("/tasks/", json={"title": "Task 2", "owner_id": user_id, "status": "completed", "priority": "medium"})
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_tasks_by_status():
    user_id = create_test_user()
    client.post("/tasks/", json={"title": "T1", "owner_id": user_id, "status": "pending", "priority": "low"})
    client.post("/tasks/", json={"title": "T2", "owner_id": user_id, "status": "completed", "priority": "low"})
    resp = client.get("/tasks/?status=pending")
    assert resp.status_code == 200
    assert all(t["status"] == "pending" for t in resp.json())


def test_update_task():
    user_id = create_test_user()
    task = client.post("/tasks/", json={"title": "Old title", "owner_id": user_id, "status": "pending", "priority": "low"}).json()
    resp = client.patch(f"/tasks/{task['id']}", json={"title": "New title", "status": "completed"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "New title"
    assert resp.json()["status"] == "completed"


def test_delete_task():
    user_id = create_test_user()
    task = client.post("/tasks/", json={"title": "To delete", "owner_id": user_id, "status": "pending", "priority": "low"}).json()
    resp = client.delete(f"/tasks/{task['id']}")
    assert resp.status_code == 200
    assert client.get(f"/tasks/{task['id']}").status_code == 404


def test_task_not_found():
    resp = client.get("/tasks/99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
