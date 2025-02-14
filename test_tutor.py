
import json
import pytest
import os
from main import app  # Import the Flask app from your main file


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_ai_tutor_valid_request(client):
    """Test AI tutor with a valid request."""
    api_key = os.environ.get("OPENAI_API_KEY")  # Get API key from environment variable
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    payload = {
        "category": "JSS",
        "subject": "Math",
        "query": "What is 2 + 2?"
    }
    response = client.post("/api/ai-tutor", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    data = response.get_json()
    assert "result" in data
    assert "explanation" in data


def test_ai_tutor_invalid_category(client):
    """Test API with an invalid category."""
    payload = {
        "category": "InvalidCategory",
        "subject": "Math",
        "query": "What is 2 + 2?"
    }
    response = client.post("/api/ai-tutor", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400  # Expecting a Bad Request error
    data = response.get_json()
    assert "error" in data


def test_ai_tutor_invalid_subject(client):
    """Test API with an invalid subject."""
    payload = {
        "category": "JSS",
        "subject": "InvalidSubject",
        "query": "What is 2 + 2?"
    }
    response = client.post("/api/ai-tutor", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400  # Expecting a Bad Request error
