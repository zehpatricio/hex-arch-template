from fastapi.testclient import TestClient
from app.main import app


def test_health():
    test_client = TestClient(app)
    response = test_client.get('/health')

    assert response.status_code == 200
