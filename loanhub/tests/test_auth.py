import pytest


def test_register_user_success(client):
    resp = client.post("/auth/register", json={
        "username": "rahul",
        "email": "rahul@mail.com",
        "password": "secure1234",
        "phone": "9876543211",
        "monthly_income": 55000,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "rahul"
    assert data["role"] == "user"
    assert "password" not in data


def test_register_duplicate_username(client):
    payload = {
        "username": "rahul",
        "email": "rahul2@mail.com",
        "password": "secure1234",
        "phone": "9876543212",
        "monthly_income": 55000,
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 409
    assert resp.json()["error"] == "DuplicateUserError"


def test_register_invalid_email(client):
    resp = client.post("/auth/register", json={
        "username": "badmail",
        "email": "notanemail",
        "password": "secure1234",
        "phone": "9876543213",
        "monthly_income": 30000,
    })
    assert resp.status_code == 422


def test_login_success(client):
    resp = client.post("/auth/login", json={
        "username": "rahul",
        "password": "secure1234",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "rahul"


def test_login_wrong_password(client):
    resp = client.post("/auth/login", json={
        "username": "rahul",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401
    assert resp.json()["error"] == "InvalidCredentialsError"


def test_login_returns_jwt_token(client):
    resp = client.post("/auth/login", json={
        "username": "rahul",
        "password": "secure1234",
    })
    assert resp.status_code == 200
    token = resp.json().get("access_token")
    assert isinstance(token, str)
    assert len(token) > 20


def test_protected_endpoint_rejects_no_token(client):
    resp = client.get("/loans/my")
    assert resp.status_code == 401


def test_protected_endpoint_rejects_wrong_role(client, user_token):
    resp = client.get(
        "/admin/loans",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403
    assert resp.json()["error"] == "ForbiddenError"
