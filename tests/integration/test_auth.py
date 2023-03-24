import pytest
from unittest import mock
from fastapi.testclient import TestClient

from app.main import app


credentials = {'username': 'testuser', 'password': 'testpassword'}


@pytest.fixture
def test_client():
    return TestClient(app)


@mock.patch('app.web.routes.auth.authenticate_user', return_value=True)
def test_successful_login(_, test_client):

    response = test_client.post('/login', json=credentials)

    assert response.status_code == 200
    assert 'Authorization' in response.headers
    assert response.headers['Authorization'].startswith('Bearer ')


@mock.patch('app.web.routes.auth.authenticate_user', return_value=False)
def test_failed_login(_, test_client):

    response = test_client.post('/login', json=credentials)

    assert response.status_code == 401
    assert 'Authorization' not in response.headers
