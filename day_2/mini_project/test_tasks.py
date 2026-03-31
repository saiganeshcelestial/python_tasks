import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import app

client = TestClient(app)

# ─── Helpers ─────────────────────────────────────────────────
def create_sample_task(title="Test Task", priority="medium", owner="alice"):
    return client.post("/tasks", json={
        "title": title,
        "description": "A test task",
        "priority": priority,
        "status": "pending",
        "owner": owner,
    })


# ─── Tests ───────────────────────────────────────────────────
def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_create_task():
    r = create_sample_task("Write unit tests")
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Write unit tests"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


def test_create_task_invalid_status():
    r = client.post("/tasks", json={
        "title": "Bad Task",
        "status": "flying",   # invalid enum
        "priority": "high",
        "owner": "alice",
    })
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "ValidationError"


def test_create_task_title_too_short():
    r = client.post("/tasks", json={
        "title": "Hi",          # min_length=3 fails
        "priority": "low",
        "owner": "alice",
    })
    assert r.status_code == 422


def test_get_tasks():
    create_sample_task("List test task")
    r = client.get("/tasks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_get_tasks_filter_by_status():
    r = client.get("/tasks?task_status=pending")
    assert r.status_code == 200
    for task in r.json():
        assert task["status"] == "pending"


def test_get_tasks_filter_by_owner():
    create_sample_task(title="Alice task", owner="alice")
    r = client.get("/tasks?owner=alice")
    assert r.status_code == 200
    for task in r.json():
        assert task["owner"] == "alice"


def test_get_tasks_pagination():
    r = client.get("/tasks?page=1&limit=2")
    assert r.status_code == 200
    assert len(r.json()) <= 2


def test_get_task_by_id():
    created = create_sample_task("Get by ID").json()
    r = client.get(f"/tasks/{created['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created["id"]


def test_get_task_not_found():
    r = client.get("/tasks/999999")
    assert r.status_code == 404
    body = r.json()
    assert body["error"] == "TaskNotFoundError"
    assert body["status_code"] == 404
    assert "999999" in body["message"]


def test_update_task():
    created = create_sample_task("Update me").json()
    r = client.put(f"/tasks/{created['id']}", json={
        "title": "Updated Title",
        "status": "in_progress",
        "priority": "high",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "in_progress"


def test_partial_update_task():
    created = create_sample_task("Patch me").json()
    r = client.patch(f"/tasks/{created['id']}", json={"status": "completed"})
    assert r.status_code == 200
    assert r.json()["status"] == "completed"
    assert r.json()["title"] == "Patch me"   # unchanged


def test_delete_task():
    created = create_sample_task("Delete me").json()
    r = client.delete(f"/tasks/{created['id']}")
    assert r.status_code == 200

    # Confirm it's gone
    r2 = client.get(f"/tasks/{created['id']}")
    assert r2.status_code == 404


def test_delete_task_not_found():
    r = client.delete("/tasks/999999")
    assert r.status_code == 404
    assert r.json()["error"] == "TaskNotFoundError"
