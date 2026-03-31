import pytest


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_apply_loan_success(client, user_token):
    resp = client.post(
        "/loans",
        json={
            "amount": 200000,
            "purpose": "education",
            "tenure_months": 60,
            "employment_status": "employed",
        },
        headers=auth_headers(user_token),
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "pending"
    assert data["amount"] == 200000
    assert data["purpose"] == "education"


def test_apply_loan_amount_exceeds_limit(client, user_token):
    resp = client.post(
        "/loans",
        json={
            "amount": 2000000,
            "purpose": "personal",
            "tenure_months": 60,
            "employment_status": "employed",
        },
        headers=auth_headers(user_token),
    )
    assert resp.status_code == 422


def test_apply_loan_amount_zero(client, user_token):
    resp = client.post(
        "/loans",
        json={
            "amount": 0,
            "purpose": "personal",
            "tenure_months": 60,
            "employment_status": "employed",
        },
        headers=auth_headers(user_token),
    )
    assert resp.status_code == 422


def test_apply_max_pending_loans(client, user_token):
    loan_payload = {
        "amount": 50000,
        "purpose": "personal",
        "tenure_months": 24,
        "employment_status": "employed",
    }
    # Fill up to 3 pending loans (1 already applied in test above)
    for _ in range(2):
        client.post("/loans", json=loan_payload, headers=auth_headers(user_token))

    # 4th attempt should be blocked
    resp = client.post("/loans", json=loan_payload, headers=auth_headers(user_token))
    assert resp.status_code == 422
    assert resp.json()["error"] == "MaxPendingLoansError"


def test_get_my_loans(client, user_token):
    resp = client.get("/loans/my", headers=auth_headers(user_token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) > 0


def test_get_single_loan_detail(client, user_token):
    loans = client.get("/loans/my", headers=auth_headers(user_token)).json()
    loan_id = loans[0]["id"]
    resp = client.get(f"/loans/my/{loan_id}", headers=auth_headers(user_token))
    assert resp.status_code == 200
    assert resp.json()["id"] == loan_id


def test_get_loan_not_belonging_to_user(client, user_token):
    resp = client.get("/loans/my/99999", headers=auth_headers(user_token))
    assert resp.status_code == 404
    assert resp.json()["error"] == "LoanNotFoundError"
