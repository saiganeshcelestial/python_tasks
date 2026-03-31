import pytest


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _get_first_pending_loan_id(client, admin_token) -> int:
    resp = client.get(
        "/admin/loans?status=pending",
        headers=auth_headers(admin_token),
    )
    loans = resp.json()
    assert len(loans) > 0, "No pending loans found for admin tests — run test_loans first."
    return loans[0]["id"]


def test_admin_views_all_loans(client, admin_token):
    resp = client.get("/admin/loans", headers=auth_headers(admin_token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_admin_approves_loan(client, admin_token):
    loan_id = _get_first_pending_loan_id(client, admin_token)
    resp = client.patch(
        f"/admin/loans/{loan_id}/review",
        json={
            "status": "approved",
            "admin_remarks": "Income verified. Approved for the full amount.",
        },
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "approved"
    assert data["reviewed_by"] == "admin"
    assert data["admin_remarks"] is not None


def test_admin_rejects_loan_with_reason(client, admin_token):
    loan_id = _get_first_pending_loan_id(client, admin_token)
    resp = client.patch(
        f"/admin/loans/{loan_id}/review",
        json={
            "status": "rejected",
            "admin_remarks": "Insufficient income for requested amount.",
        },
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "rejected"
    assert "income" in data["admin_remarks"].lower()


def test_admin_cannot_re_review_loan(client, admin_token):
    # Get any already-reviewed loan
    all_loans = client.get("/admin/loans", headers=auth_headers(admin_token)).json()
    reviewed = next((l for l in all_loans if l["status"] != "pending"), None)
    assert reviewed is not None, "No reviewed loan found."

    resp = client.patch(
        f"/admin/loans/{reviewed['id']}/review",
        json={"status": "approved", "admin_remarks": "Trying to re-review this loan."},
        headers=auth_headers(admin_token),
    )
    assert resp.status_code == 422
    assert resp.json()["error"] == "InvalidLoanReviewError"


def test_non_admin_cannot_access_admin_endpoint(client, user_token):
    resp = client.get("/admin/loans", headers=auth_headers(user_token))
    assert resp.status_code == 403
    assert resp.json()["error"] == "ForbiddenError"


def test_analytics_summary(client, admin_token):
    resp = client.get("/analytics/summary", headers=auth_headers(admin_token))
    assert resp.status_code == 200
    data = resp.json()
    assert "total_loans" in data
    assert "approved_loans" in data
    assert "loans_by_purpose" in data
    assert "avg_loan_amount" in data
