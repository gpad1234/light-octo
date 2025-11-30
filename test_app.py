import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test the home page endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['message'] == 'Hello, Flask!'


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_invalid_route(client):
    """Test an invalid route returns 404."""
    response = client.get('/invalid')
    assert response.status_code == 404
