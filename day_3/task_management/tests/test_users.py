"""
Tests for user endpoints.
Uses the same in-memory SQLite override as test_tasks.py.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

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


def test_create_user():
    resp = client.post("/users/", json={
        "username": "alice",
        "email": "alice@mail.com",
        "password": "pass123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "alice"
    assert "password" not in data  # never expose password in response


def test_duplicate_user():
    payload = {"username": "bob", "email": "bob@mail.com", "password": "pass"}
    client.post("/users/", json=payload)
    resp = client.post("/users/", json=payload)
    assert resp.status_code == 409


def test_list_users():
    client.post("/users/", json={"username": "u1", "email": "u1@mail.com", "password": "p"})
    client.post("/users/", json={"username": "u2", "email": "u2@mail.com", "password": "p"})
    resp = client.get("/users/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_user_by_id():
    user = client.post("/users/", json={"username": "carol", "email": "carol@mail.com", "password": "p"}).json()
    resp = client.get(f"/users/{user['id']}")
    assert resp.status_code == 200
    assert resp.json()["username"] == "carol"


def test_user_not_found():
    resp = client.get("/users/99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_delete_user():
    user = client.post("/users/", json={"username": "dave", "email": "dave@mail.com", "password": "p"}).json()
    resp = client.delete(f"/users/{user['id']}")
    assert resp.status_code == 200
    assert client.get(f"/users/{user['id']}").status_code == 404
