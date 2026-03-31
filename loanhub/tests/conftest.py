import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Use an in-memory SQLite DB for tests
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


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def registered_user(client):
    payload = {
        "username": "testuser",
        "email": "testuser@mail.com",
        "password": "password123",
        "phone": "9876543210",
        "monthly_income": 50000,
    }
    client.post("/auth/register", json=payload)
    return payload


@pytest.fixture(scope="module")
def user_token(client, registered_user):
    resp = client.post("/auth/login", json={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    return resp.json()["access_token"]


@pytest.fixture(scope="module")
def admin_token(client):
    resp = client.post("/auth/login", json={
        "username": "admin",
        "password": "admin1234",
    })
    return resp.json()["access_token"]
