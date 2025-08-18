from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import pytest
import uuid

load_dotenv()

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL"
)

# Create a new engine instance specifically for testing
test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="function")
def setup_database():
    """
    A pytest fixture that sets up and tears down the database for each test function.
    This ensures each test has a clean, isolated database.
    """
    # Use the test engine to drop and create tables
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_root():
    """Tests the root endpoint."""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Hello AI Directory Application!"}

def test_signup_login(setup_database):
    """
    Tests the user signup and login flow.
    """
    # Generate a unique username and email for this test run to prevent conflicts
    unique_id = str(uuid.uuid4())
    test_username = f"testuser_{unique_id}"
    test_email = f"test_{unique_id}@example.com"

    # Test Signup
    signup_data = {
        "username": test_username,
        "full_name": "Test User",
        "email": test_email,
        "password": "password123"
    }
    
    # Send a POST request to the signup endpoint
    res = client.post("/users/signup", json=signup_data)
    
    # Print the status code and response content for debugging
    print(f"Signup response status code: {res.status_code}")
    print(f"Signup response content: {res.text}")
    
    # Assert a successful signup response
    assert res.status_code == 200
    # The signup endpoint returns a token.
    assert "access_token" in res.json()
    assert "token_type" in res.json()

    # Test Login
    login_data = {
        # Use the unique username from the signup test
        "username": test_username,
        "password": "password123"
    }
    # Send a POST request to the login endpoint to get a token
    res_login = client.post("/users/login", data=login_data)
    
    # Assert a successful login response
    assert res_login.status_code == 200
    
    # Assert that the access token is present in the login response
    token_data = res_login.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"

    protected_res = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token_data['access_token']}"}
    )
    assert protected_res.status_code == 200
    assert protected_res.json()["username"] == test_username
