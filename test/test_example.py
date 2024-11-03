import sys
import os

# add app module to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_wrong_email_referral():
    email = "test@example.com"
    response = client.get(f"/referral/referral_code?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"