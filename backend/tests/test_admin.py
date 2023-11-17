import sys
from pathlib import Path

# Append the parent directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from models import Users  # Adjust based on actual file and class name

client = TestClient(app)

# Mock User Data
test_user = Users(id=1, username="admin", is_active=True, role="admin")

# Test for Root Endpoint
def test_root_endpoint():
    response = client.get("/admin/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Test for Deactivating a User
@patch("path.to.your.database.session")
def test_deactivate_user(mocked_session):
    # Setup the mock
    mocked_session.query.return_value.filter.return_value.first.return_value = test_user

    response = client.post("/admin/users/2/deactivate")
    assert response.status_code == 200
    assert response.json() == {"ok": True, "message": "User deactivated successfully"}

# Test for Reading All Users
@patch("path.to.your.database.session")
def test_read_all_users(mocked_session):
    # Setup the mock
    mocked_session.query.return_value.all.return_value = [test_user]

    response = client.get("/admin/users")
    assert response.status_code == 200
