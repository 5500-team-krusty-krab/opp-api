from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_user_signup_success():
    response = client.post("/auth/signup", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 200
    assert response.json() == {"success": True}

def test_user_signup_existing_email():
    # Assuming 'test@example.com' already exists in the database
    response = client.post("/auth/signup", json={
        "name": "Another User",
        "email": "test@example.com",
        "password": "anotherpassword"
    })
    assert response.status_code == 400
    assert response.json().get("detail") == "Email already in use."

def test_user_login_success():
    # Assuming the user with these credentials exists
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 200
    assert "Successfully logged in" in response.json().get("message")

def test_user_login_incorrect_details():
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect login details" in response.json().get("detail")
