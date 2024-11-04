from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_wrong_email_referral():
    email = "test@example.com"
    response = client.get(f"/referral/referral_code?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_unauthorized_request():
    referral_data = {
        "code": "string",
        "expiration": "2024-11-04T09:04:28.895Z"
    }
    response = client.post("/referral/create", json=referral_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
