from unittest import mock

from fastapi.testclient import TestClient
from app.main import app




@mock.patch('app.web.routes.health.check_database')
def test_health_check_response(mock_check_database):
    client = TestClient(app)

    # Test when the database is up
    mock_check_database.return_value = True

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'api': True, 'database': True}

    # Test when the database is down
    mock_check_database.return_value = False

    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'api': True, 'database': False}
