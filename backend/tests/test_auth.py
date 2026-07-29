import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import sessionLocal
from app.models.user import UserManager

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up test database before and after each test"""
    # Before test: Clean up
    db = sessionLocal()
    try:
        # Delete test users (emails ending with @test.com)
        db.query(UserManager).filter(UserManager.email.like("%@test.com")).delete()
        db.commit()
    finally:
        db.close()
    
    yield
    
    # After test: Clean up again
    db = sessionLocal()
    try:
        db.query(UserManager).filter(UserManager.email.like("%@test.com")).delete()
        db.commit()
    finally:
        db.close()


def registration_test():
    response = client.post(
        "/auth/register",
        json={
            "name": "Nien Technician",
            "email": "nien@gmail.com",
            "password": "technician123",
            "role": "Technician",
            "area": "Laguna"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "nien@gmail.com"
    assert data["name"] == "Nien Technician"
    assert "id" in data

def test_duplicate_registration():
    # First registration
    client.post(
        "/auth/register",
        json={
            "name": "Yubin Technician",
            "email": "yubin@gmail.com",
            "password": "technician123",
            "role": "Technician",
            "area": "Cavite"
        }
    )
    
    # Second registration with same email
    response = client.post(
        "/auth/register",
        json={
            "name": "Yubin 2",
            "email": "yubin@gmail.com",
            "password": "yubin123",
            "role": "Supervisor",
            "area": "Laguna"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login():
    # Register first
    client.post(
        "/auth/register",
        json={
            "name": "Naky Technician",
            "email": "nakytechnician@gmail.com",
            "password": "technician123",
            "role": "Technician",
            "area": "Laguna"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={
            "username": "nakytechnician@gmail.com",
            "password": "technician123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_invalid_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "kotine@gmail.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_get_current_user():
    # Register a test user
    register_response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "testpass123",
            "role": "Supervisor",
            "area": "Cavite"
        }
    )
    assert register_response.status_code == 200
    
    # Login with the test user
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "testpass123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Note: Your model uses uppercase field names
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "Supervisor"

def test_get_current_user_invalid_token():
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_get_current_user_missing_token():
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"