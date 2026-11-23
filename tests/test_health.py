"""Health and root route tests."""
import pytest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    GEMINI_API_KEY = ""

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client

def test_root_endpoint_serves_html(client):
    """Verify GET / returns 200 and loads HTML page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI CareerPilot" in response.data
    assert b"Navigate Your Career" in response.data

def test_health_check_endpoint(client):
    """Verify GET /api/health returns operational status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI CareerPilot"
    assert "version" in data
    assert "uptime_seconds" in data
    assert "ai_integration" in data
    assert data["ai_integration"]["provider"] == "Google AI (Gemma/Gemini)"
    assert data["ai_integration"]["api_key_configured"] is False
    assert "Demo" in data["ai_integration"]["mode"]

def test_serverless_entrypoint_returns_ok(client):
    """Verify GET /api/index (Vercel entrypoint) responds with 200 instead of 404."""
    response = client.get("/api/index")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["status"] == "healthy"
    assert data["endpoints"]["health"] == "/api/health"

def test_404_api_not_found(client):
    """Verify unknown API route returns 404 JSON."""
    response = client.get("/api/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()
