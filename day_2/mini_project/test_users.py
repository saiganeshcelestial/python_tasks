import pytest
from fastapi.testclient import TestClient
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import app

client = TestClient(app)

import time

def unique_user(prefix="testuser"):
    return f"{prefix}_{int(time.time() * 1000)}"


def test_register_user():
    username = unique_user("alice")
    r = client.post("/users/register", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "strongpass123",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["username"] == username
    assert "password" not in data   # password must be excluded


def test_register_duplicate_user():
    username = unique_user("dup")
    payload = {"username": username, "email": f"{username}@mail.com", "password": "pass1234"}
    client.post("/users/register", json=payload)
    r = client.post("/users/register", json=payload)
    assert r.status_code == 409
    assert r.json()["error"] == "DuplicateUserError"


def test_register_invalid_email():
    r = client.post("/users/register", json={
        "username": unique_user("bad"),
        "email": "notanemail",
        "password": "pass1234",
    })
    assert r.status_code == 422


def test_register_short_password():
    r = client.post("/users/register", json={
        "username": unique_user("shortpass"),
        "email": "x@x.com",
        "password": "abc",    # < 8 chars
    })
    assert r.status_code == 422


def test_login_success():
    username = unique_user("loginok")
    client.post("/users/register", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "mypassword",
    })
    r = client.post("/users/login", json={"username": username, "password": "mypassword"})
    assert r.status_code == 200
    assert r.json()["username"] == username


def test_login_wrong_password():
    username = unique_user("badlogin")
    client.post("/users/register", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "correctpass",
    })
    r = client.post("/users/login", json={"username": username, "password": "wrongpass"})
    assert r.status_code == 401
    assert r.json()["error"] == "InvalidCredentialsError"


def test_list_users():
    r = client.get("/users")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    for u in r.json():
        assert "password" not in u


def test_delete_user():
    username = unique_user("todelete")
    created = client.post("/users/register", json={
        "username": username,
        "email": f"{username}@mail.com",
        "password": "deletepass",
    }).json()
    r = client.delete(f"/users/{created['id']}")
    assert r.status_code == 200


def test_delete_user_not_found():
    r = client.delete("/users/999999")
    assert r.status_code == 404
    assert r.json()["error"] == "UserNotFoundError"
